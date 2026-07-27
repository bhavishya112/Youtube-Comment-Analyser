import umap
import numpy as np
import plotly.express as px
from backend.topic_clustering import get_embeddings, cluster_comments
from backend.scrape_data import get_comments

while True:
    df = get_comments(input("youtube URL : "))
    print(df["textOriginal"])
    docs = df["textOriginal"].tolist()
    topic_model,topics, probs = cluster_comments(docs)

    # Suppose you already have your embeddings from BERTopic
    embeddings = get_embeddings(docs)

    # Reduce to 2D
    umap_model = umap.UMAP(
        n_neighbors=15, n_components=2, min_dist=0.0, metric="cosine"
    )
    umap_embeddings = np.asarray(umap_model.fit_transform(embeddings))

    # Build dataframe for plotting
    import pandas as pd

    df = pd.DataFrame(
        {
            "x": umap_embeddings[:, 0],
            "y": umap_embeddings[:, 1],
            "topic": topics,
            "comment": docs,
            "prob": probs,
        }
    )

    # Interactive scatter plot
    fig = px.scatter(
        df,
        x="x",
        y="y",
        color="topic",
        hover_data={"comment": True, "prob": True, "topic": True},
    )

    fig.update_layout(title="BERTopic Clusters in 2D")
    fig.show()
