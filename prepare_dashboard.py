import umap
import numpy as np
import plotly.express as px
from topic_clustering import get_embeddings, cluster_comments
from scrape_data import get_comments,store_comment_threads,get_video_metadata,store_video_metadata,extract_video_id
from process_data import build_dashboard_data
import os 

from IPython import embed
def gather_data(youtube_url:str):

    video_id = extract_video_id(youtube_url)
    if (not os.path.exists(f"data/comments/comments_{video_id}.json")):
        store_comment_threads(youtube_url,50)

    if (not os.path.exists(f"data/videos/video_{video_id}.json")):
        store_video_metadata(youtube_url)

    
    df_video = get_video_metadata(youtube_url)
    df_comments = get_comments(youtube_url)

    docs = df_comments["textOriginal"].tolist()
    topic_model,topics, probs = cluster_comments(docs)
    variables = build_dashboard_data(video_df = df_video,comments_df=df_comments,topics=topics,topic_model=topic_model,probabilities=probs)
    embed()


    

gather_data(input("url : "))