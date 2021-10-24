import pandas as pd


raw_df = pd.read_pickle(r"dataframe_cleaner/raw_df.pkl")
print(raw_df)


class CleanDataFrame:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def remove_duplicates(self):
        self.drop_duplicate(inplace=True)


CleanDataFrame(raw_df).remove_duplicates()

print(raw_df)
