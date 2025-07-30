# Deploying Secure Data Science Applications in the Cloud

**Companion Repository for the Apress Book:**  
*"Deploying Secure Data Science Applications in the Cloud: From VMs to Serverless with AWS and Google Cloud"*

## 📚 Get the Book

📖 **Official Book Page**: [Springer/Apress](https://link.springer.com/book/9798868817144)  
🛒 **Purchase on Amazon**: [Amazon Store](https://www.amazon.com/Deploying-Secure-Science-Applications-Cloud/dp/B0FCKTNL3W)  
👤 **Connect with the Author**: [LinkedIn](https://www.linkedin.com/in/lucasbraga461/)

---

## 📖 About This Repository

This repository contains all the practical code examples, configurations, and deployment scripts from the book "Deploying Secure Data Science Applications in the Cloud." Each chapter folder provides hands-on implementations demonstrating how to securely deploy data science applications using modern cloud platforms and containerization technologies.

## 🛠️ Technologies Covered

- **Cloud Platforms**: AWS, Google Cloud Platform (GCP)
- **Containerization**: Docker, Docker Compose
- **Web Frameworks**: Flask, Streamlit
- **ML Deployment**: Scikit-learn model serving, Pickle serialization
- **Infrastructure**: Nginx reverse proxy, SSL/TLS certificates
- **CI/CD**: Jenkins for ETL/ELT pipelines
- **Security**: HTTP Basic Authentication, Domain security, Subdomains
- **Serverless**: AWS ECS Fargate, Google Cloud Run

## 📚 Chapter Overview

### Chapter 02: SSH to the EC2 Instance with VSCode and Necessary Setup
- Initial cloud setup and development environment configuration
- Streamlit example application

### Chapter 04: Domain Name and SSL Certificates
- SSL certificate configuration
- Nginx setup for HTTPS
- Docker Compose orchestration

### Chapter 05: Deploying More Robust Applications
- Multi-service deployment with Docker Compose
- Jenkins integration for CI/CD
- Flask and Streamlit application orchestration
- Nginx reverse proxy configuration

### Chapter 06: Create and Secure Your Subdomains
- Subdomain security implementation
- Advanced Nginx configuration
- Multi-service routing

### Chapter 07: Google Cloud Platform Infrastructure Setup
- GCP-specific deployment configurations
- Cloud-native service orchestration
- Platform comparison examples

### Chapter 09: Serverless Deployment with Google Cloud Run
- **Flask Application**: Secure ML model serving API
- **Streamlit Dashboard**: Interactive data science applications
- Containerized serverless deployment

### Chapter 10: Serverless Deployment with AWS
- **Flask Application**: Transaction scoring API with authentication
- **Streamlit Application**: Sample size calculator
- AWS ECS Fargate and container-based serverless options

### Chapter 11: Jenkins as ETL/ELT Platform for Data Science
- **ETL Scripts**: Multi-cloud data processing (AWS S3 ↔ GCP Storage)
- **Jenkins Configuration**: Automated data pipeline execution
- **Jupyter Notebooks**: Interactive ETL development

### Chapter 12: Streamlit Dashboard Demo
- **Multi-cloud Dashboard**: Connects to both AWS S3 and GCP Storage
- **Data Visualization**: Interactive charts and data exploration
- **Cloud Storage Integration**: Seamless data access across platforms

### Chapter 13: Flask Application Demo
- **ML Model API**: Random Forest model serving
- **Authentication**: HTTP Basic Auth implementation
- **Logging**: Comprehensive request/response logging
- **Error Handling**: Robust exception management

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- AWS CLI (configured with appropriate credentials)
- Google Cloud SDK (with service account JSON)
- Python 3.8+

### Basic Setup
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd deploy-secure-ds-apps-book
   ```

2. Navigate to any chapter directory:
   ```bash
   cd "Chapter 10 Serverless Deployment with AWS"
   ```

3. Follow the specific setup instructions in each chapter's README or configuration files.

### Example: Running Chapter 05 Multi-Service Application
```bash
cd "Chapter 05 Deploying More Robust Applications (Jenkins, Flask, and Streamlit)"
export JENKINS_UID=$(id -u)
export JENKINS_GID=$(id -g)
docker-compose up -d
```

## 🔧 Key Features Demonstrated

### Security Best Practices
- SSL/TLS certificate management
- HTTP Basic Authentication
- Secure subdomain configuration
- Environment variable management
- Service isolation with Docker

### ML Model Deployment
- Pickle model serialization/deserialization
- REST API endpoints for model inference
- Error handling and logging
- Authentication for production APIs

### Multi-Cloud Architecture
- AWS S3 and GCP Storage integration
- Platform-agnostic deployment strategies
- Cloud-specific optimizations
- Serverless vs. container trade-offs

### Data Pipeline Automation
- Jenkins-based ETL/ELT workflows
- Multi-cloud data synchronization
- Automated data processing schedules
- Interactive development with Jupyter

### Production-Ready Deployments
- Nginx reverse proxy configuration
- Docker container orchestration
- Health checks and monitoring
- Scalable architecture patterns

## 📁 Repository Structure

```
deploy-secure-ds-apps-book/
├── Chapter 02 SSH to the EC2 Instance with VSCode and Necessary Setup/
├── Chapter 04 Domain Name and SSL Certificates/
├── Chapter 05 Deploying More Robust Applications (Jenkins, Flask, and Streamlit)/
├── Chapter 06 Create and Secure your Subdomains/
├── Chapter 07 How to Setup This Infrastructure On Google Cloud Platform (GCP)/
├── Chapter 09 Serverless Deployment with Google Cloud Run/
├── Chapter 10 Serverless Deployment with AWS/
├── Chapter 11 Demo Using Jenkins as an ETL ELT Platform for Data Science/
├── Chapter 12 Demo Streamlit/
└── Chapter 13 Demo Flask/
```

## 🔒 Security Considerations

This repository demonstrates production-ready security practices:
- Never commit credentials or API keys
- Use environment variables for sensitive configuration
- Implement proper authentication mechanisms
- Configure SSL/TLS for all public-facing services
- Follow principle of least privilege for cloud permissions

## 📝 Prerequisites for Each Chapter

Each chapter may require specific setup:
- **AWS Chapters**: AWS CLI configured with appropriate IAM permissions
- **GCP Chapters**: Service account JSON file and appropriate GCP project setup
- **Jenkins Chapters**: Docker and sufficient system resources
- **SSL Chapters**: Valid domain name and certificate files

## 🤝 Contributing

This repository serves as companion code for the Apress book. For errata, improvements, or questions:

1. Check the book's official errata page
2. Create an issue for technical problems
3. Submit pull requests for bug fixes

## 📄 License

Code examples are provided for educational purposes as companion material to the Apress book. Please refer to the book's licensing terms for usage guidelines.

## 📖 About the Book

"Deploying Secure Data Science Applications in the Cloud: From VMs to Serverless with AWS and Google Cloud" is a comprehensive guide for Data Scientists, ML engineers, and DevOps practitioners who need to turn prototypes into secure, scalable production services. This step-by-step book bridges the gap between building Data Science applications and Machine Learning models, and deploying them effectively in real-world scenarios.

### What You'll Learn:
- Deploy end-to-end data science applications with cloud infrastructure setup
- Use industry-standard tools like Docker, Nginx, Flask, Streamlit, and Jenkins
- Structure and expose machine learning models via APIs for production use
- Explore modern serverless architectures with AWS ECS Fargate and Google Cloud Run
- Develop secure cloud deployment practices from the ground up

### Target Audience:
Beginning to intermediate professionals with Python knowledge, including Data Scientists, ML Engineers, Data Engineers, and Data Analysts looking to securely deploy projects in production environments.

**Release Date**: September 2025  
**Publisher**: Apress (Springer Nature)  
**Author**: Lucas Henrique Benevides e Braga

---

*For detailed instructions on each chapter, navigate to the respective chapter directory and refer to the specific configuration files and documentation.*