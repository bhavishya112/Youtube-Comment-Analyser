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
# from backend.topic_clustering import get_embeddings, cluster_comments
# from backend.scrape_data import get_comments,get_video_metadata
# from backend.process_data import build_dashboard_data

# from IPython import embed
# df = get_comments("https://www.youtube.com/watch?v=RBRiNVfvSxU&t=736s")

# df_video =  get_video_metadata("https://www.youtube.com/watch?v=RBRiNVfvSxU&t=736s")
# docs = df["textOriginal"].tolist()
# topic_model,topics, probs = cluster_comments(docs)

# def gather_data(youtube_url:str):
#     variables = build_dashboard_data(video_df = df_video ,comments_df=df,topics=topics,topic_model=topic_model,probabilities=probs)
#     from IPython import embed
#     embed()


# while True:
#     gather_data("https://www.youtube.com/watch?v=RBRiNVfvSxU&t=736s")


# import requests

# response = requests.request(method='post',url='http://localhost:8001/analyse',json={"url":"https://www.youtube.com/watch?v=MmNFJ4CGvyw&t=1141s"}).json()
# print("type:response = ",type(response))
# print("response = ",response)


# from backend.scrape_data import download_comment_threads

# download_comment_threads()

# import winsound
# winsound.Beep(1000,1000)
from backend.scrape_data import *
import os.path
import json


def download_comment_threads(video_url: str, max_comments: int = 5000):
    """Download at most max_comments number of comments and store it in data/comments as Json"""
    video_id = extract_video_id(video_url)

    comments = []
    page_size = min(max_comments, 100)

    request = YOUTUBE.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=page_size,
        textFormat="plainText",
        order="time",
        fields="""
            items(
                snippet(
                    totalReplyCount,
                    topLevelComment(
                        snippet(
                            authorDisplayName,
                            textOriginal,
                            likeCount,
                            publishedAt,
                            updatedAt
                        )
                    )
                )
            ),
            nextPageToken
        """.replace("\n", "").replace(" ", "")
    )
    try:
        while request and len(comments) < max_comments:
            response = request.execute()
            comments.extend(response["items"])

            if len(comments) >= max_comments:
                comments = comments[:max_comments]
                break

            request = YOUTUBE.commentThreads().list_next(request, response)

        Path("data/comments").mkdir(parents=True, exist_ok=True)

        with open(
            f"data/comments/comments_{video_id}.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(comments, f, ensure_ascii=False, indent=4)

        return comments

    except HttpError as e:
        print(f"YouTube API error: {e}")
        return []


def get_comments(video_url: str):
    """Read all the comments stored it in data/comments and return DataFrame of it"""
    video_id = extract_video_id(video_url)
    path = f"./data/comments/comments_{video_id}.json"
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No comment data found for video id {video_id}")

    with open(path, "r", encoding="utf-8") as fp:
        result = json.load(fp)

    df = json_normalize(result)
    df.columns = [col.split(".")[-1] for col in df.columns]
    df = df[
        [
            "authorDisplayName",
            "textOriginal",
            "likeCount",
            "publishedAt",
            "updatedAt",
            "totalReplyCount",
        ]
    ]
    # return df
    from IPython import embed
    embed()
    return df.drop_duplicates()

download_comment_threads("https://www.youtube.com/watch?v=ZPRVIvyz0kk")
get_comments("https://www.youtube.com/watch?v=ZPRVIvyz0kk")
