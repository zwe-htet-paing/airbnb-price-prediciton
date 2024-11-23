# Airbnb Price Prediction - MLOps Project

## Overview
This project is designed to practice MLOps (Machine Learning Operations) by implementing a pipeline to predict the price of Airbnb listings in New York City. The goal is to create an end-to-end solution that integrates data ingestion, model training, evaluation, and deployment while adhering to best practices in version control, automation, and monitoring.

## Dataset
The dataset used in this project contains information about [Airbnb listings](https://insideairbnb.com/get-the-data/) in New York City, with the following key columns:

- id: Listing ID
- name: Name of the listing
- host_id: Host ID
- host_name: Name of the host
- neighbourhood_group: Location (e.g., Manhattan, Brooklyn)
- neighbourhood: Area within the location
- latitude: Latitude coordinates
- longitude: Longitude coordinates
- room_type: Type of room being listed (e.g., entire home, private room)
- price: Price per night in dollars
- minimum_nights: Minimum number of nights required for booking
- number_of_reviews: Total number of reviews for the listing
- last_review: Date of the last review
- reviews_per_month: Average number of reviews per month
- calculated_host_listings_count: Number of listings the host has
- availability_365: Number of days the listing is available for booking in a year


## Pipeline
This project includes an MLOps pipeline that automates the process of data ingestion, model training, evaluation, deployment, and monitoring.

### Steps in the Pipeline:
1. Data Ingestion: Fetches and preprocesses the raw data.
2. Feature Engineering: Generates new features to improve model performance.
3. Model Training: Trains the machine learning model using the processed data.
4. Model Evaluation: Evaluates the model using validation metrics.
5. Deployment: Deploys the model to a cloud or on-premise server.
6. Monitoring & Logging: Monitors model performance and logs key metrics.

### Modeling
Various machine learning models were tested to predict the price of Airbnb listings:

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor
- XGBoost

The models were trained and evaluated using metrics like Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and R-squared.