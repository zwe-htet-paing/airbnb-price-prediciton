import os
import uuid
import pickle
import sys
from datetime import datetime

import pandas as pd
import numpy as np

from prefect import task, flow, get_run_logger
from prefect.context import get_run_context

from dateutil.relativedelta import relativedelta

import mlflow

TRACKING_URL = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(TRACKING_URL)
print(f"Tracking URI: '{mlflow.get_tracking_uri()}'")


RUN_ID = os.getenv('RUN_ID', '7b5744464f544451aee4a9308d1971ad')

def generate_uuids(n):
    ride_ids = []
    for i in range(n):
        ride_ids.append(str(uuid.uuid4()))
    return ride_ids

def read_dataframe(filename):
    df = pd.read_csv(filename)
    
    # Handle missing values
    df = df.dropna(subset=['price'])
    df['reviews_per_month'] = df['reviews_per_month'].fillna(0)
    df['last_review'] = pd.to_datetime(df['last_review'])
    
    df['request_id'] = generate_uuids(len(df))

    return df


def preprocess(df):
    # Calculate IQR
    Q1 = df['price'].quantile(0.25)  # First quartile (25th percentile)
    Q3 = df['price'].quantile(0.75)  # Third quartile (75th percentile)
    IQR = Q3 - Q1  # Interquartile range

    # Define outlier boundaries
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Remove outliers
    df = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)].reset_index(drop=True)
    
    return df

def prepare_dictionaries(df: pd.DataFrame):    
    # Feature selection
    numerical = ['latitude', 'longitude', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'availability_365']
    categorical = ['room_type', 'neighbourhood']
    df[categorical] = df[categorical].astype(str)

    dicts = df[categorical + numerical].to_dict(orient='records')
    return dicts


def load_models(run_id):
    with open('../web-service-mlflow/preprocessor.b', 'rb') as f_in:
        loaded_dv = pickle.load(f_in)
    
    logged_model = f'runs:/{run_id}/models'
    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    return loaded_dv, loaded_model


def save_results(df, y_pred, run_id, output_file):
    df_result = pd.DataFrame()
    df_result['request_id'] = df['request_id']
    df_result['room_type'] = df['room_type']
    df_result['neighbourhood'] = df['neighbourhood']
    df_result['latitude'] = df['latitude']
    df_result['longitude'] = df['longitude']
    df_result['minimum_nights'] = df['minimum_nights']
    df_result['number_of_reviews'] = df['number_of_reviews']
    df_result['reviews_per_month'] = df['reviews_per_month']
    df_result['availability_365'] = df['availability_365']
    df_result['actual_price'] = df['price']
    df_result['predicted_price'] = y_pred
    df_result['diff'] = df_result['actual_price'] - df_result['predicted_price']
    df_result['model_version'] = run_id
    
    df_result.to_csv(output_file, index=False)


@task
def apply_model(input_file, run_id, output_file):
    logger = get_run_logger()

    logger.info(f'reading the data from {input_file}...')
    df = read_dataframe(input_file)
    dicts = prepare_dictionaries(df)

    logger.info(f'loading the model with RUN_ID={run_id}...')
    dv, model = load_models(run_id)

    logger.info(f'applying the model...')
    
    X = dv.transform(dicts)
    y_pred = model.predict(X)
    y_pred = np.round(np.power(10, y_pred), 2)

    logger.info(f'saving the result to {output_file}...')

    save_results(df, y_pred, run_id, output_file)
    return output_file


def get_paths(run_date, city, run_id):
    prev_month = run_date - relativedelta(months=0)
    year = prev_month.year
    month = prev_month.month
    day = prev_month.day

    input_file = f'https://data.insideairbnb.com/united-states/ny/{city}/{year:04d}-{month:02d}-{day:02d}/visualisations/listings.csv'
    output_file = f'output/{city}/{year:04d}-{month:02d}-listings.csv'
   
    return input_file, output_file


@flow
def airbnb_price_prediction(
        city: str,
        run_id: str,
        run_date: datetime = None):
    if run_date is None:
        ctx = get_run_context()
        run_date = ctx.flow_run.expected_start_time
    
    input_file, output_file = get_paths(run_date, city, run_id)

    apply_model(
        input_file=input_file,
        run_id=run_id,
        output_file=output_file
    )


def run():
    city = sys.argv[1] # 'albany'
    year = int(sys.argv[2]) # 2024
    month = int(sys.argv[3]) # 9
    day = int(sys.argv[4]) # 5

    run_id = sys.argv[5] # '7b5744464f544451aee4a9308d1971ad'

    airbnb_price_prediction(
        city=city,
        run_id=run_id,
        run_date=datetime(year=year, month=month, day=day)
    )


if __name__ == '__main__':
    run()
    
# Example Usge:
# python score.py albany 2024 9 5 7b5744464f544451aee4a9308d1971ad