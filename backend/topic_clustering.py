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
logger = MyLogger()

logger.configure("INFO")  # Tracks only ERROR and CRITICAL levels

# 2. Extract the underlying standard Python logger object
bertopic_base_logger = logging.getLogger("BERTopic")

# 3. Create a file handler to route the log stream to a text file
file_handler = logging.FileHandler("logs/topic_clustering.log", mode="a")

# 4. Set a readable formatting layout for the file output
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# 5. Attach the file handler to BERTopic's logger engine
bertopic_base_logger.addHandler(file_handler)


# logger = setup_logger(__name__, "logs/topic_clustering.log")

try:
    EMB_MODEL = SentenceTransformer("AkshitaS/bhasha-embed-v0")
    # EMB_MODEL = SentenceTransformer("baai/bge-m3")

    with open("stopwords.txt", "r", encoding="utf-8") as f:
        x = f.readlines()
        x = [word.strip() for word in x]

    STOPWORDS = x

    # representation_model = KeyBERTInspired()
    client = openai.OpenAI(
        api_key="sk-...", base_url="http://127.0.0.1:11434/v1")

    class OpenAIEmbeddings:
        def __init__(self, model="bge-m3"):
            self.model = model

        def __call__(self, docs: pd.Series):
            # docs is a list of strings

            response = client.embeddings.create(
                input=docs, model=self.model, extra_body={"keep_alive": -1}
            )
            embeddings = [i.embedding for i in response.data]
            # convert list of embedding vectors to a 2D numpy array
            return np.asarray(embeddings, dtype=float)

    def get_embeddings(docs: list[str]):
        # return OpenAIEmbeddings()(docs)
        return np.asarray(EMB_MODEL.encode(docs))

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
            client=client, model="ibm/granite4.1:3b", chat=True)
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
    logger.exception(E)

# from scrape_comments import get_comments

# df = get_comments("https://www.youtube.com/watch?v=RBRiNVfvSxU&t=735s")
# print(df["textOriginal"])
# cluster_comments(df["textOriginal"])
