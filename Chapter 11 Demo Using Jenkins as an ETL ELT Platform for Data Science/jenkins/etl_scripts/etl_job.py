import pandas as pd
import boto3
from google.cloud import storage
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
import argparse

# === Config ===
CREDENTIALS_PATH = Path('../config/lb-cloud-project-65885ec00848.json')
AWS_BUCKET_NAME = 'book-project-54641'
GCP_BUCKET_NAME = 'book-etl-project'

# === Extraction Functions ===

def extract_from_s3(bucket_name, file_name):
    print(f"Extracting {file_name} from AWS S3 bucket {bucket_name}")
    s3 = boto3.Session(profile_name='book-etl').client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    data = response['Body'].read()
    return pd.read_csv(BytesIO(data))


def extract_from_gcp(bucket_name, file_name, credentials_path):
    print(f"Extracting {file_name} from GCP bucket {bucket_name}")
    client = storage.Client.from_service_account_json(credentials_path)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    data = blob.download_as_bytes()
    return pd.read_csv(BytesIO(data))


# === Upload Functions ===

def upload_to_s3(df, bucket_name, file_name):
    print(f"Uploading {file_name} to AWS S3 bucket {bucket_name}")
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    s3 = boto3.Session(profile_name='book-etl').client('s3')
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=buffer.getvalue())
    print("Upload to S3 completed.")


def upload_to_gcp(df, bucket_name, file_name, credentials_path):
    print(f"Uploading {file_name} to GCP bucket {bucket_name}")
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    client = storage.Client.from_service_account_json(credentials_path)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_file(buffer, content_type='text/csv')
    print("Upload to GCP completed.")


# === Transformation Function ===

def transform_data(df):
    print("Transforming data...")

    df.drop_duplicates(subset=['user_id', 'amount', 'currency', 'date', 'status', 'payment_gateway'], inplace=True)
    df.dropna(subset=['amount'], inplace=True)

    conversion_rates = {'EUR': 1.1, 'USD': 1.0}
    df['amount_usd'] = df.apply(lambda x: round(x['amount'] * conversion_rates[x['currency']], 2), axis=1)

    # Success count rate
    success_counts = df[df['status'] == 'completed'].groupby(['date', 'payment_gateway']).size()
    total_counts = df.groupby(['date', 'payment_gateway']).size()

    success_rate_df = pd.DataFrame({
        'date': total_counts.index.get_level_values('date'),
        'payment_gateway': total_counts.index.get_level_values('payment_gateway'),
        'total_transactions': total_counts.values,
        'successful_transactions': success_counts.reindex(total_counts.index, fill_value=0).values
    })
    success_rate_df['success_rate_percent'] = round(
        (success_rate_df['successful_transactions'] / success_rate_df['total_transactions']) * 100, 2
    )

    # Success amount rate
    total_amount = df.groupby(['date', 'payment_gateway'])['amount_usd'].sum()
    successful_amount = df[df['status'] == 'completed'].groupby(['date', 'payment_gateway'])['amount_usd'].sum()

    amount_success_rate_df = pd.DataFrame({
        'date': total_amount.index.get_level_values('date'),
        'payment_gateway': total_amount.index.get_level_values('payment_gateway'),
        'total_amount_usd': total_amount.values,
        'successful_amount_usd': successful_amount.reindex(total_amount.index, fill_value=0).values
    })
    amount_success_rate_df['amount_success_rate_percent'] = round(
        (amount_success_rate_df['successful_amount_usd'] / amount_success_rate_df['total_amount_usd']) * 100, 2
    )

    return success_rate_df, amount_success_rate_df


# === Main ETL Logic ===

def run_etl(source, today, credentials_path):
    ### 1. Extract (E) data
    today_minus_1 = (today - timedelta(days=1)).strftime('%Y_%m_%d')
    date_list = [(today - timedelta(days=i)).strftime('%Y_%m_%d') for i in range(1, 4)]
    file_names = [f"raw_transactions_{date}.csv" for date in date_list]

    df_ls = []
    for file in file_names:
        if source == 'aws':
            df_ls.append(extract_from_s3(AWS_BUCKET_NAME, file))
        elif source == 'gcp':
            df_ls.append(extract_from_gcp(GCP_BUCKET_NAME, file, credentials_path))

    df = pd.concat(df_ls, ignore_index=True)

    ### 2. Transform (T) data
    success_rate_df, amount_success_rate_df = transform_data(df)

    ### 3. Load (L) transformed data to bucket
    folder = 'output'
    if source == 'aws':
        upload_to_s3(success_rate_df, AWS_BUCKET_NAME, f"{folder}/success_rate_df_{today_minus_1}.csv")
        upload_to_s3(amount_success_rate_df, AWS_BUCKET_NAME, f"{folder}/amount_success_rate_df_{today_minus_1}.csv")
    elif source == 'gcp':
        upload_to_gcp(success_rate_df, GCP_BUCKET_NAME, f"{folder}/success_rate_df_{today_minus_1}.csv", credentials_path)
        upload_to_gcp(amount_success_rate_df, GCP_BUCKET_NAME, f"{folder}/amount_success_rate_df_{today_minus_1}.csv", credentials_path)


# === CLI Parser ===

def parse_args():
    parser = argparse.ArgumentParser(description="ETL pipeline to extract, transform, and load transaction data.")
    parser.add_argument("--source", choices=["aws", "gcp"], default="gcp", help="Cloud source. Default is gcp.")
    parser.add_argument("--date", type=str, help="Base date in YYYY-MM-DD format. Defaults to today.")
    return parser.parse_args()


# === Entry Point ===

if __name__ == "__main__":
    args = parse_args()

    source = args.source
    if args.date:
        today = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        today = datetime.today()

    run_etl(source, today, CREDENTIALS_PATH)

# python etl_job.py --source gcp --date 2025-05-18