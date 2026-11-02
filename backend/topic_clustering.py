from os import getenv
from dotenv import load_dotenv
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
import openai
from bertopic.representation import OpenAI
from bertopic.representation import KeyBERTInspired
from logger import setup_logger
from bertopic._utils import MyLogger
import logging
import os

logging.basicConfig(format="%(asctime)s - %(filename)s - %(message)s",
                    datefmt="%d %b %H:%M", level=logging.DEBUG, filename=f"logs/{__name__}.log")


load_dotenv(".env")
GROQ_API_KEY = getenv("GROQ_API_KEY")
NIM_API_KEY = getenv("NIM_API_KEY")

EMB_MODEL = "nvidia/nemotron-3-embed-1b"

emb_client = openai.OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NIM_API_KEY
)


def get_embeddings(docs: list[str], input_type="passage"):
    response = emb_client.embeddings.create(
        model=EMB_MODEL,
        input=docs,
        extra_body={
            "input_type": input_type,
            "truncate": "END"
        }
    )

    embeddings = [
        item.embedding
        for item in sorted(response.data, key=lambda x: x.index)
    ]

    return np.asarray(embeddings, dtype=np.float32)


try:
    # EMB_MODEL = SentenceTransformer("AkshitaS/bhasha-embed-v0")
    # EMB_MODEL = SentenceTransformer("baai/bge-m3")

    with open("stopwords.txt", "r", encoding="utf-8") as f:
        x = f.readlines()
        x = [word.strip() for word in x]

    STOPWORDS = x

    # representation_model = KeyBERTInspired()
    client = openai.OpenAI(
        api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")

    def cluster_comments(docs: list[str]):
        """Uses Bertopic for Clustering comments, internally piped to Local LLM for Topic Generation.
        Since Bertopic natively returns only representative words from the topic, we needed the llm pipeline
        Args:
            docs (list(str)): the list of all utf-8 strings (comments having emojis)
        Returns:
            Tuple (tuple) : Tuple (topic_model, topics, probabilities)
                where \\
                topic_model (BERTopic) : the fitted model\\
                topics (list(int)) : list of topics ids\\
                probabilities (ndarray): confidence scores for each topic"""
        representation_model = OpenAI(
            client=client, model="qwen/qwen3.8-27b", chat=True)
        # client=client, model="gemma3n:e2b", chat=True)
        hdbscan_model = HDBSCAN(
            min_cluster_size=10, metric="euclidean", prediction_data=True
        )  # change this

        umap_model = UMAP(
            n_neighbors=50, n_components=5, metric="euclidean", min_dist=0.0, random_state=42
        )
        vectorizer = CountVectorizer(
            stop_words=STOPWORDS, ngram_range=(1, 2), min_df=2)

        from bertopic import BERTopic

        embeddings = get_embeddings(docs)

        topic_model = BERTopic(
            nr_topics=20,
            language="multilingual",
            calculate_probabilities=False,
            vectorizer_model=vectorizer,
            umap_model=umap_model,
            hdbscan_model=hdbscan_model,
            verbose=True,
            representation_model=representation_model
        )

        topics, probs = topic_model.fit_transform(
            embeddings=embeddings, documents=docs)
        # print(f"topics : {topics}\n\nprobs : {probs}")

        return topic_model, topics, probs

except Exception as E:
    # from winsound import Beep
    # Beep(1000, 1000)
    import sys
    logging.error(E)

# from scrape_comments import get_comments

# df = get_comments("https://www.youtube.com/watch?v=RBRiNVfvSxU&t=735s")
# print(df["textOriginal"])
# cluster_comments(df["textOriginal"])
