import pandas as pd

df_dict = {
    "series1": [1, 2, 3] * 3,
    "series2": [3.2234, 47.44, 0.345] * 3,
    "series3": ["test1", "test2", "test3"] * 3,
}

raw_df = pd.DataFrame.from_dict(df_dict)

print(raw_df.head())

raw_df.to_pickle("raw_df.pkl")
