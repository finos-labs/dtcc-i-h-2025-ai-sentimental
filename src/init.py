import pandas as pd

df = pd.read_csv("Corporate_Actions.csv")
print(df.shape)
print(df.columns.tolist())