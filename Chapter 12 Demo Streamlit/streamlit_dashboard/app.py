import streamlit as st
import pandas as pd
from io import BytesIO
from pathlib import Path
import boto3
from google.cloud import storage
import re

# === CONFIG ===
AWS_BUCKET_NAME = 'book-project-54641'
GCP_BUCKET_NAME = 'book-etl-project'
GCP_CREDENTIALS_PATH = Path("config/lb-cloud-project-65885ec00848.json")
DATA_FOLDER = "output"
SOURCE = 'aws' # Change to 'gcp' for Google Cloud Storage or to 'aws' for AWS S3

# === Utility: List S3 files ===
def list_files_s3(bucket_name, prefix):
    s3 = boto3.Session(profile_name='book-etl').client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files = [obj['Key'] for obj in response.get('Contents', [])]
    return files

# === Utility: List GCP files ===
def list_files_gcp(bucket_name, prefix, credentials_path):
    client = storage.Client.from_service_account_json(str(credentials_path))
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    return [blob.name for blob in blobs]

# === Extract dates from files available ===
def extract_dates_from_filenames(file_list, pattern=r"_(\d{4}_\d{2}_\d{2})\.csv$"):
    # Extract the last 10 characters before '.csv'
    dates = []
    for filename in file_list:
        m = re.search(pattern, filename)
        if m:
            dates.append(m.group(1))
    return sorted(list(set(dates)), reverse=True)

# === Utility: Load from S3 ===
def load_csv_from_s3(bucket_name, file_key):
    s3 = boto3.Session(profile_name='book-etl').client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    return pd.read_csv(BytesIO(response['Body'].read()), parse_dates=["date"])

# === Utility: Load from GCP ===
def load_csv_from_gcp(bucket_name, file_key, credentials_path):
    client = storage.Client.from_service_account_json(str(credentials_path))
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_key)
    return pd.read_csv(BytesIO(blob.download_as_bytes()), parse_dates=["date"])

# === Load data from cloud ===
@st.cache_data
def load_data(source, date_str):
    success_file = f"{DATA_FOLDER}/success_rate_df_{date_str}.csv"
    amount_file = f"{DATA_FOLDER}/amount_success_rate_df_{date_str}.csv"

    if source == "aws":
        success_df = load_csv_from_s3(AWS_BUCKET_NAME, success_file)
        amount_df = load_csv_from_s3(AWS_BUCKET_NAME, amount_file)
    else:
        success_df = load_csv_from_gcp(GCP_BUCKET_NAME, success_file, GCP_CREDENTIALS_PATH)
        amount_df = load_csv_from_gcp(GCP_BUCKET_NAME, amount_file, GCP_CREDENTIALS_PATH)

    return success_df, amount_df

# === Sidebar Filters ===
st.sidebar.title("File (by available date)")
# List available dates in the bucket
if SOURCE == 'aws':
    all_files = list_files_s3(AWS_BUCKET_NAME, f"{DATA_FOLDER}/success_rate_df_")
else:
    all_files = list_files_gcp(GCP_BUCKET_NAME, f"{DATA_FOLDER}/success_rate_df_", GCP_CREDENTIALS_PATH)

all_dates_str = extract_dates_from_filenames(all_files)
# Convert to datetime.date objects for display/selection
all_file_dates = [pd.to_datetime(date, format="%Y_%m_%d").date() for date in all_dates_str]

selected_file_from_date = st.sidebar.selectbox("Select File from Date", options=all_file_dates)
selected_date_str = selected_file_from_date.strftime("%Y_%m_%d")

success_df, amount_df = load_data(SOURCE, selected_date_str)

st.sidebar.title("Filters")

all_dates = pd.concat([success_df["date"], amount_df["date"]]).drop_duplicates().sort_values(ascending=False)
selected_date = st.sidebar.selectbox("Select Date", options=all_dates.dt.date)

all_psps = sorted(set(success_df["payment_gateway"]) | set(amount_df["payment_gateway"]))
selected_psps = st.sidebar.multiselect("Select PSP(s)", options=all_psps, default=all_psps)

metric = st.sidebar.radio("Metric to Plot", options=["Success Rate (%)", "Amount Success Rate (%)"])

# === Filter data ===
filtered_success_df = success_df[
    (success_df["date"].dt.date == selected_date) & 
    (success_df["payment_gateway"].isin(selected_psps))
]

filtered_amount_df = amount_df[
    (amount_df["date"].dt.date == selected_date) & 
    (amount_df["payment_gateway"].isin(selected_psps))
]

# === Display Tables ===
if SOURCE == "aws":
    st.title("📊 ETL Dashboard (from AWS S3)")
else:
    st.title("📊 ETL Dashboard (from Google Cloud Storage)")

st.header(f"📅 Success Rates for {selected_date}")

# Format date for display in tables
filtered_success_df["date"] = filtered_success_df["date"].dt.strftime('%Y-%m-%d')
filtered_amount_df["date"] = filtered_amount_df["date"].dt.strftime('%Y-%m-%d')

filtered_success_df.rename(columns={
    "success_rate_percent": "success_rate_pct",
}, inplace=True)
filtered_amount_df.rename(columns={
    "amount_success_rate_percent": "amt_success_rate_pct"
}, inplace=True)

st.subheader("✔️ Count-Based Success Rate")
st.dataframe(filtered_success_df.sort_values("payment_gateway"))

st.subheader("💵 Amount-Based Success Rate")
st.dataframe(filtered_amount_df.sort_values("payment_gateway"))

# === Line Chart ===
st.header("📈 Trend Over Time")

merged_df = pd.merge(
    success_df[["date", "payment_gateway", "success_rate_percent"]],
    amount_df[["date", "payment_gateway", "amount_success_rate_percent"]],
    on=["date", "payment_gateway"],
    how="outer"
)

merged_filtered = merged_df[merged_df["payment_gateway"].isin(selected_psps)]

if metric == "Success Rate (%)":
    st.line_chart(
        merged_filtered.pivot_table(index="date", columns="payment_gateway", values="success_rate_percent")
    )
else:
    st.line_chart(
        merged_filtered.pivot_table(index="date", columns="payment_gateway", values="amount_success_rate_percent")
    )
