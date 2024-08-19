import requests
from io import BytesIO
from typing import List

import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def ingest_files(**kwargs) -> pd.DataFrame:

    response = requests.get(
        f'https://data.insideairbnb.com/united-states/ny/albany/2024-05-06/visualisations/listings.csv'
    )

    if response.status_code != 200:
        raise Exception(response.text)

    df = pd.read_csv(BytesIO(response.content))

    return df