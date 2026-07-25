import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
import openai
from bertopic.representation import OpenAI
from bertopic.representation import KeyBERTInspired

EMB_MODEL = SentenceTransformer("AkshitaS/bhasha-embed-v0")


# representation_model = KeyBERTInspired()
client = openai.OpenAI(api_key="sk-...",base_url="http://127.0.0.1:11434/v1")
representation_model = OpenAI(client=client, model="ibm/granite4.1:3b", chat=True)



hdbscan_model = HDBSCAN(
    min_cluster_size=2, metric="euclidean", prediction_data=True
)  # change this

umap_model = UMAP(
    n_neighbors=15, n_components=5, metric="cosine", min_dist=0.0, random_state=42
)


vectorizer = CountVectorizer(stop_words=None, ngram_range=(1, 2), min_df=2)
# client = OpenAI(base_url="http://localhost:11434/v1", api_key="api_key")


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
    from bertopic import BERTopic

    embeddings = get_embeddings(docs)
    topic_model = BERTopic(
        language="multilingual",
        calculate_probabilities=False,
        vectorizer_model=vectorizer,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        verbose=True,
        representation_model=representation_model
    )
    topics, probs = topic_model.fit_transform(embeddings=embeddings, documents=docs)
    # print(f"topics : {topics}\n\nprobs : {probs}")
    return topic_model,topics, probs


# from scrape_comments import get_comments

# df = get_comments("https://www.youtube.com/watch?v=RBRiNVfvSxU&t=735s")
# print(df["textOriginal"])
# cluster_comments(df["textOriginal"])
