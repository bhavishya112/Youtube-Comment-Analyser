import openai
import pandas as pd
CLIENT = openai.Client(base_url = "http://127.0.0.1:11434/v1",api_key = "api_key")

def generate_summary(docs : pd.DataFrame )-> list[str]:
    docs.groupby("topic")["comment"].apply(list)
