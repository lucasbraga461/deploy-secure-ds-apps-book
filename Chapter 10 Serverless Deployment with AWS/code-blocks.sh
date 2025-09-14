# Code-block 10-1. Install AWS CLI
# Install on macOS
brew install awscli

# Install on Linux (Ubuntu/Debian/RHEL/etc.)
# Download the installer, unzip it and install it:
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Install on Windows
# Download the latest installer for Windows, run it and follow the prompts
# https://awscli.amazonaws.com/AWSCLIV2.msi

# Verify it
aws -–version


# Code-block 10-4. Create environment variables
export REGION=us-east-1
export AWS_ACCOUNT_ID=9161123123


# Code-block 10-5. Create two ECR repositories, one for each application
# Create an ECR Repository
aws ecr create-repository --repository-name flask-app --profile serverlessuser --region $REGION
aws ecr create-repository --repository-name streamlit-app --profile serverless-user --region $REGION


# Code-block 10-6. Authenticate Docker to AWS ECR
# Authenticate Docker to AWS ECR
aws ecr get-login-password --region $REGION --profile root-461 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com


# Code-block 10-7. Build the flask Docker image
# Build Docker image
cd ~/Documents/GitHub/my-web-server/flask-app/
docker buildx build --platform=linux/amd64 -t flask-app .


# Code-block 10-8. Tag the Docker image and push it to ECR
# Tag it
docker tag flask-app:latest $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/flask-app:latest

# Push to ECR
docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/flask-app:latest


# Code-block 10-9. Creating the Streamlit Docker image and pushing it to ECR
# 3. Build and Push the Docker Image
# Build Docker image
cd ~/Documents/GitHub/my-web-server/streamlit-app/
docker build -t streamlit-app .

# 4. Tag it
docker tag streamlit-app:latest $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/streamlit-app:latest

# 5. Push to ECR
docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/streamlitapp:latest
