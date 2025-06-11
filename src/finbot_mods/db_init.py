from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("sqlite:///corporate.db")
try:
    pd.read_csv("data/external_csv/Corporate_Actions.csv").to_sql("corporate_action", engine, index=False)
except ValueError as e:
    print(e)


db = SQLDatabase(engine=engine)