# Airbnb Price Prediction - MLOps Project

## Overview
This project is designed to practice MLOps (Machine Learning Operations) by implementing a pipeline to predict the price of Airbnb listings in New York City. The goal is to create an end-to-end solution that integrates data ingestion, model training, evaluation, and deployment while adhering to best practices in version control, automation, and monitoring. This project was created as part of the practice exercises from the **MLOps Zoomcamp** by [DataTalksClub](https://datatalks.club/), where we focus on implementing practical MLOps concepts.

## Dataset
The dataset used for this project contains information about [Airbnb listings](https://insideairbnb.com/get-the-data/) in New York City, with the following key columns:

- **id**: Listing ID
- **name**: Name of the listing
- **host_id**: Host ID
- **host_name**: Name of the host
- **neighbourhood_group**: Location (e.g., Manhattan, Brooklyn)
- **neighbourhood**: Area within the location
- **latitude**: Latitude coordinates
- **longitude**: Longitude coordinates
- **room_type**: Type of room being listed (e.g., entire home, private room)
- **price**: Price per night in dollars
- **minimum_nights**: Minimum number of nights required for booking
- **number_of_reviews**: Total number of reviews for the listing
- **last_review**: Date of the last review
- **reviews_per_month**: Average number of reviews per month
- **calculated_host_listings_count**: Number of listings the host has
- **availability_365**: Number of days the listing is available for booking in a year

## MLOps Practices and Tools
The project follows MLOps principles and uses the following tools and practices to implement a robust machine learning pipeline:

- **Experiment Tracking**: MLFlow for tracking experiments, logging metrics, and managing models.
- **Orchestration**: Mage for automating workflows and managing pipelines.
- **Deployment**: Deploying the model as a web service, with options for both streaming and batch processing.
- **Monitoring**: Using Evidently for monitoring the model's performance and data drift over time.
- **Best Practices**: 
  - Linter and formatting tools to ensure code quality.
  - Git pre-commit hooks to maintain code consistency.
  - Unit tests and integration tests for reliability.
  - Infrastructure as Code (IaC) using Terraform for provisioning the environment.

## Modeling
Several machine learning models were tested to predict the price of Airbnb listings:

- **Linear Regression**
- **Lasso**
- **XGBoost**
- **Random Forest Regressor**
- **Gradient Boosting Regressor**
- **ExtraTrees Regressor**
- **LinearSVR**

The models were evaluated using the following metrics:
- **Mean Absolute Error (MAE)**
- **Root Mean Squared Error (RMSE)**

## Acknowledgements
This project was created to practice the skills learned from the [**MLOps Zoomcamp**](https://github.com/DataTalksClub/mlops-zoomcamp) by [DataTalksClub](https://datatalks.club/), a comprehensive course focused on implementing MLOps workflows for machine learning projects.
