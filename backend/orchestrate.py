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
    """Main Server Endpoint
    Args:
        video (Video): A json object containing video information, it currently holds video_url

    Returns: 
        job_id (dict): Json like object for Nth job running on the server
        """
    job_id = str(uuid.uuid4())

    STATUS[job_id] = {
        "status": "running",
        "stage": "analysing..."
    }

    Thread(target=gather_data, args=(
        job_id, STATUS[job_id], video.video_url), daemon=True).start()

    return {"job_id": job_id}


# status = {"stage":"---","status":"---"}
def gather_data(job_id: str, status: dict, youtube_url: str):
    """Does all the Download-Read-PreProcess Logic, Performance Main Orchestration Logic. 
    Stores the calculated and processed variables inside variables_state.pkl because at refresh the dashboard lost its data

    Args:
        job_id (str): job_id of the server
        status (dict): the internal status variable for updating frontend about inner processes (see STATUS)
        youtube_url (str): youtube's video_url to start gathering the comments
    """

    video_id = extract_video_id(youtube_url)
    if (not os.path.exists(f"data/comments/comments_{video_id}.json")):
        status['stage'] = 'downloading comments'
        download_comment_threads(youtube_url, 30000)

    if (not os.path.exists(f"data/videos/video_{video_id}.json")):
        status['stage'] = 'downloading video metadata'
        download_video_metadata(youtube_url)

    status['stage'] = 'retrieving data'
    df_video = get_video_metadata(youtube_url)
    df_comments = get_comments(youtube_url)

    docs = df_comments["textOriginal"].tolist()

    status['stage'] = 'clustering comments'
    topic_model, topics, probs = cluster_comments(docs)

    status['stage'] = 'preparing dashboard variables'
    variables = build_dashboard_data(video_df=df_video, comments_df=df_comments,
                                     topics=topics, topic_model=topic_model, probabilities=probs)

    status['stage'] = 'storing variables'
    with open("backend/variables_state.pkl", "wb") as fb:
        pickle.dump(variables, fb)

    # return variables
    VARIABLES[job_id] = {"variables": variables}

    status['status'] = 'complete'

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
    """Updates the client on current running internal processes
    Args:
        job_id (str): Job Id of the process in the server
    Returns:
        status (dict): status of the form {"status":"running","stage":"downloading data"}"""
    return STATUS[job_id]


@app.post("/result/{job_id}")
def result(job_id: str):
    """Returns the Final Calculated Dashboard Variables(Currently Useless as we're directly saving things in pickle file)
    Args:
        job_id (str): Job ID of the Thread running on the Agent Server
    Returns:
        variables (dict): dictionary of all calculated and preprocessed variables
        """
    return VARIABLES[job_id]["variables"]
