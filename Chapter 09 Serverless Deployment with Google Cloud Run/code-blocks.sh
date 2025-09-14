# Code-block 9-2. Initial commands
export GOOGLE_CLOUD_PROJECT=<YOUR_PROJECT> # e.g. export GOOGLE_CLOUD_PROJECT=lb-cloud-project
export LOCATION=<YOUR_REGION> # e.g. export LOCATION=us-west2, export LOCATION=us-central1
gcloud auth login


# Code-block 9-3. Deploy Flask application with Cloud Run
gcloud builds submit flask-app-gcp/ --tag gcr.io/$GOOGLE_CLOUD_PROJECT/flask_app --region=$LOCATION

gcloud run deploy flask-app \
    --image gcr.io/$GOOGLE_CLOUD_PROJECT/flask_app \
    --region=$LOCATION --allow-unauthenticated


# Code-block 9-4. Deploy Streamlit application with Cloud Run
gcloud builds submit streamlit-app-gcp/ --tag gcr.io/$GOOGLE_CLOUD_PROJECT/streamlit_app --region=$LOCATION

gcloud run deploy streamlit-app \
    --image gcr.io/$GOOGLE_CLOUD_PROJECT/streamlit_app \
    --region=$LOCATION --allow-unauthenticated


# Code-block 9-5. Creating Network Endpoint Group (NEG)
gcloud compute network-endpoint-groups create flask-neg \
    --region=$LOCATION \
    --network-endpoint-type=serverless \
    --cloud-run-service=flask-app

gcloud compute network-endpoint-groups create streamlit-neg \
    --region=$LOCATION \
    --network-endpoint-type=serverless \
    --cloud-run-service=streamlit-app


# Code-block 9-7. Block direct access to Cloud Run apps
gcloud run services update flask-app \
    --region=$LOCATION \
    --ingress internal-and-cloud-load-balancing

gcloud run services update streamlit-app \
    --region=$LOCATION \
    --ingress internal-and-cloud-load-balancing
