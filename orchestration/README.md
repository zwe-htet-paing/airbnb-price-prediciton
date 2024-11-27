# Orchestration Pipeline using Mage

This folder contains the MLOps pipeline powered by Mage to automate the various stages of the machine learning lifecycle, including data ingestion, data preparation, model training, evaluation, deployment, monitoring, inference, and retraining.

# Pipeline Overview

The pipeline integrates various tasks to ensure smooth automation, model tracking, and monitoring. Mage is used to orchestrate the following stages:

1. **Data Ingestion**: Utilizes Mage’s ingestion blocks to fetch and preprocess raw data, converting it into a format suitable for model training.

2. **Data Preparation**: Cleans and transforms the ingested data, handling missing values and applying necessary transformations for optimal model performance.

3. **Model Training**: Trains sklearn and XGBoost models using the processed data, fine-tuning them for better predictive accuracy.

4. **Monitoring & Alerting**: Mage tracks model performance using metrics like MSE and RMSE, and integrates SHAP values for model explainability and monitoring.

5. **Inference and Retraining**: Mage executes the inference pipeline to generate predictions and establishes a retraining pipeline, ensuring that the models stay relevant as new data becomes available.


## Setup pipeline: Quick Start

1. Clone the following respository containing the complete code for this module:

    ```bash
    git clone https://github.com/zwe-htet-paing/mlops.git
    cd mlops
    ```

2. Launch Mage and the database service (PostgreSQL):

    ```bash
    ./scripts/start.sh
    ```

    If don't have bash in your enviroment, modify the following command and run it:

    ```bash
    PROJECT_NAME=mlops \
        MAGE_CODE_PATH=/home/src \
        SMTP_EMAIL=$SMTP_EMAIL \
        SMTP_PASSWORD=$SMTP_PASSWORD \
        docker compose up
    ```

    It is ok if you get this warning, you can ignore it
    `The "PYTHONPATH" variable is not set. Defaulting to a blank string.`

3. The subproject that contains all the pipelines and code is named `airbnb-price-prediction`.

## Run example pipeline

1. Open http://localhost:6789 in your browser.

2. In the top left corner of the screen next to the Mage logo and `mlops` project name, click the project selector dropdown and choose the `airbnb-price-prediction` option.

3. Click on the pipeline named `data_preparation`.

4. Click on the button labeled `Run @once`.