import time
import pickle
from backend.topic_clustering import get_embeddings, cluster_comments
from backend.scrape_data import get_comments, download_comment_threads, get_video_metadata, download_video_metadata, extract_video_id
from backend.process_data import build_dashboard_data
import os
from IPython import embed
from fastapi import FastAPI
from urllib.parse import urlparse
import multiprocessing
import os
import uuid
from pydantic import BaseModel
from threading import Thread

app = FastAPI()


class Video(BaseModel):
    video_url: str


class Job(BaseModel):
    job_id: str


STATUS = dict()

STATUS = {}  # structure= {job_id : {"status" : "--","stage":"---"}}
VARIABLES = {}  # structure= {job_id : variables}


@app.post("/analyse")
def start_analysis(video: Video):
    job_id = str(uuid.uuid4())

    STATUS[job_id] = {
        "status": "running",
        "stage": "analysing..."
    }

    Thread(target=gather_data, args=(
        job_id, STATUS[job_id], video.video_url), daemon=True).start()

    return {"job_id": job_id}


def gather_data(job_id: str, status: dict, youtube_url: str): #status = {"stage":"---","status":"---"}

    video_id = extract_video_id(youtube_url)
    if (not os.path.exists(f"data/comments/comments_{video_id}.json")):
        download_comment_threads(status,youtube_url, 500)

    if (not os.path.exists(f"data/videos/video_{video_id}.json")):
        download_video_metadata(status,youtube_url)

    df_video = get_video_metadata(status,youtube_url)
    df_comments = get_comments(status,youtube_url)

    docs = df_comments["textOriginal"].tolist()
    topic_model, topics, probs = cluster_comments(status,docs)
    variables = build_dashboard_data(status,video_df=df_video, comments_df=df_comments,
                                     topics=topics, topic_model=topic_model, probabilities=probs)
    # return variables
    VARIABLES[job_id] = {"variables": variables}

# def gather_data(job_id: str, youtube_url: str): #dummy gather_data
#     with open("backend/variables_state.pkl", "rb") as fb:
#         variables = pickle.load(fb)

#     STATUS[job_id]["stage"] = "orchestrating"

#     time.sleep(0.5)

#     STATUS[job_id]["stage"] = "paraphrasing"

#     time.sleep(0.5)

#     STATUS[job_id]["stage"] = "writing"

#     time.sleep(0.5)

#     STATUS[job_id]["status"] = "complete"
#     # return variables
#     VARIABLES[job_id] = {"variables": variables}


@app.get("/status/{job_id}")
def get_status(job_id: str):
    return STATUS[job_id]


@app.post("/result/{job_id}")
def result(job_id: str):
    return VARIABLES[job_id]["variables"]
