import pandas as pd


def clean(
    df: pd.DataFrame,
    include_extreme_prices: bool = False,
) -> pd.DataFrame:
    # drop unuse coloumns
    df.drop(['host_id','name','latitude','longitude','id','host_name','last_review', 'neighbourhood_group', 'license'], axis=1, inplace=True)
    df.dropna(subset=['price'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # fill na value 
    df['reviews_per_month'] = df['reviews_per_month'].fillna(0)

    if include_extreme_prices:
        df = df[(df.price >= 1) & (df.price <= 201)]
    
    # Feature selection
    categorical = ['room_type', 'neighbourhood']
    df[categorical] = df[categorical].astype(str)

    return df