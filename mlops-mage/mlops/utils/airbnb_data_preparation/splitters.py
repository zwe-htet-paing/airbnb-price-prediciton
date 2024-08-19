from typing import List, Tuple, Union

from pandas import DataFrame, Index
from sklearn.model_selection import train_test_split


def split_on_ratio(
    df: DataFrame,
    test_size: float = 0.2,
    return_indexes: bool = False,
    random_state: int = 0,
) -> Union[Tuple[DataFrame, DataFrame], Tuple[Index, Index]]:
    # Split the DataFrame
    df_train, df_val = train_test_split(df, test_size=test_size, random_state=random_state)

    if return_indexes:
        return df_train.index, df_val.index

    return df_train, df_val