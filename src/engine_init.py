from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("sqlite:///corporate.db")
pd.read_csv("data/external_csv/Corporate_Actions.csv").to_sql("corporate_action", engine, index=False)


db = SQLDatabase(engine=engine)