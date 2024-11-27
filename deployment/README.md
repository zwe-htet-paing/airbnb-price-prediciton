# Deployment

This folder contains methods for deploying machine learning models using web services, streaming, and batch processing.

## 1. Web-Services: Flask and Docker
* Goal: Serve models as APIs.
* Details: Uses Flask to expose models via HTTP, and Docker for containerization.
* Steps:
    1. Build a Flask API to serve the model.
    2. Containerize with Docker.
    3. Deploy on any server/cloud.

## 2. Web-Services: MLflow Model Registry
* Goal: Serve models fetched from MLflow’s model registry.
* Details: Fetches models from MLflow, and serves them via a Flask API.
* Steps:
    1. Store models in MLflow.
    2. Fetch model from registry.
    3. Serve via Flask API.

## 3. Streaming: Kinesis and Lambda
* Goal: Real-time inference on streaming data.
* Details: Uses AWS Kinesis for data streams and AWS Lambda for real-time inference.
* Steps:
    1. Stream data via Kinesis.
    2. Deploy model in Lambda for real-time predictions.

## 4. Batch: Scoring Script
* Goal: Run inference on batch data.
* Details: A scoring script processes large datasets and outputs predictions.
* Steps:
    1. Prepare scoring script.
    2. Run script on batch data.


## Folder Structure

* `web-service/`: Flask API and Docker setup for web services.
* `web-service-mlflow/`: Fetch models from MLflow model registry.
* `streaming/`: Streaming deployment with Kinesis and Lambda.
* `batch/`: Scoring script for batch inference.
