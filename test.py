# from topic_clustering import cluster_comments
# from scrape_data import get_comments
# import pandas as pd

# import openai
# CLIENT = openai.Client(base_url = "http://127.0.0.1:11434/v1",api_key = "api_key")

# while True:
#     df = get_comments(input("youtube url : "))
#     comments = df["textOriginal"].to_list()
#     topic_model,topics,probs = cluster_comments(comments)

#     joined = pd.DataFrame({"topic":topics,"comment":comments})

#     result = joined.groupby("topic")["comment"].apply(list)

#     # from IPython import embed

#     # embed()

#     import random
#     import ast
#     # Function to sample N comments per topic
#     def sample_comments(grouped : pd.Series, n=4):
#         samples = {}
#         for topic, comments in grouped.items():
#             samples[topic] = random.sample(comments, min(n, len(comments)))
#         return samples

#     samples = sample_comments(result, n=3)

#     system_prompt = {"role":"system","content":'''generate one phrase english summary of the following n sentences give result in list format like ['topic'], the topic can't be more than 1, you have to summarize in a way that covers all of them
#     the sentences are given below : \n'''}
#     # Send each topic’s sample to Ollama/Granite
#     results = {}
#     for topic, comments in samples.items():
#         prompt = {"role":"user","content": f"\n".join(comments)}
#         response = CLIENT.chat.completions.create(model="ibm/granite4.1:3b", messages=[system_prompt,prompt]) # type: ignore
#         results[topic] = ast.literal_eval(response.choices[0].message.content)

#     # Merge back into DataFrame
#     df_results = pd.DataFrame({
#         "topic": list(results.keys()),
#         "analysis": list(results.values())
#     })

#     print(df_results)

#     from IPython import embed
#     embed()




# import umap
# import numpy as np
# import plotly.express as px
# from topic_clustering import get_embeddings, cluster_comments
# from scrape_data import get_comments
# from process_data import build_dashboard_data

# from IPython import embed
# df = get_comments("https://www.youtube.com/watch?v=RBRiNVfvSxU&t=736s")

# def gather_data(youtube_url:str):
#     docs = df["textOriginal"].tolist()
#     topic_model,topics, probs = cluster_comments(docs)
#     variables = build_dashboard_data(comments_df=df,topics=topics,topic_model=topic_model,probabilities=probs)
#     # embed()


# while True:
#     gather_data("https://www.youtube.com/watch?v=RBRiNVfvSxU&t=736s")




import requests

response = requests.request(method='post',url='http://localhost:8001/analyse',json={"url":"https://www.youtube.com/watch?v=MmNFJ4CGvyw&t=1141s"}).json()
print("type:response = ",type(response))
print("response = ",response)


