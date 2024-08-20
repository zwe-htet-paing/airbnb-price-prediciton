from typing import Tuple

import pandas as pd

from mlops.utils.airbnb_data_preparation.cleaning import clean
from mlops.utils.airbnb_data_preparation.feature_selector import select_features
from mlops.utils.airbnb_data_preparation.splitters import split_on_ratio

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def transform(
    df: pd.DataFrame, **kwargs
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    test_size = kwargs.get('test_size')
    target = kwargs.get('target')

    df = clean(df)
    df = select_features(df, features=[target])

    df_train, df_val = split_on_ratio(
        df,
        test_size
        
    )

    return df, df_train, df_val