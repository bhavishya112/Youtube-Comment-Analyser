from collections import Counter, defaultdict
import numpy as np
import pandas as pd
import json
from IPython import embed 


def build_dashboard_data(
    video_df:pd.DataFrame,
    comments_df: pd.DataFrame,
    topics,
    topic_model,
    probabilities=None,
):
    """
    comments_df columns:
    -------------------
    authorDisplayName
    textOriginal
    likeCount
    updatedAt
    totalReplyCount

    topics : BERTopic topic ids
    """
    
    df = comments_df.copy()

    df["topic_id"] = topics
    df["prob"] = probabilities
    df["topic_name"] = df["topic_id"].map(topic_model.topic_labels_)
    df["topic_name"] = df["topic_name"].fillna("Noise")
    # from IPython import embed 
    # embed()

    # -------------------------
    # Global Stats
    # -------------------------

    stats = {
        "total_comments": len(df),
        "unique_authors": df.authorDisplayName.nunique(),
        "total_likes": int(df.likeCount.sum()),
        "total_replies": int(df.totalReplyCount.sum()),
        "avg_likes": float(df.likeCount.mean()),
        "avg_replies": float(df.totalReplyCount.mean()),
        "topics_found": int(df.topic_id.nunique() - (1 if -1 in df.topic_id.values else 0)),
        "noise_comments": int((df.topic_id == -1).sum()),
    }

    #--------------------------
    # VIDEO DATA
    #---------------------------

    video = video_df.to_dict("records")

    # -------------------------
    # Topic Distribution
    # -------------------------

    topic_distribution = (
        df.groupby("topic_name")
        .size()
        .sort_values(ascending=False)
        .reset_index(name="count")
        .to_dict("records")
    )

    topic_distribution = [
        {
            "topic_id": int(top["topic_name"].split("_")[0]),
            "topic_name": top["topic_name"],
            "count": top["count"],
        }
        for top in topic_distribution
    ]

    
    # -------------------------
    # Top liked comments
    # -------------------------

    top_liked = (
        df.sort_values("likeCount", ascending=False)
        .head(20)
        .to_dict("records")
    )

    # -------------------------
    # Top replied comments
    # -------------------------

    top_discussions = (
        df.sort_values("totalReplyCount", ascending=False)
        .head(20)
        .to_dict("records")
    )

    # -------------------------
    # Topic Cards
    # -------------------------

    topics_data = []

    topic_info = topic_model.get_topic_info()

    for topic_id in topic_info.Topic:

        if topic_id == -1:
            continue

        subset = df[df.topic_id == topic_id]

        rep_doc = topic_model.get_representative_docs(topic_id)
        keywords = topic_model.get_topic(topic_id)

        topics_data.append({

            "id": int(topic_id),

            "name": topic_model.topic_labels_[topic_id],

            "confidence": round(df.prob[df.topic_id == 0][0],2),

            "size": len(subset),

            "percentage": round(
                len(subset) / len(df) * 100,
                2
            ),

            "keywords": [
                k
                for k, _
                in keywords
            ],

            "avg_likes": float(subset.likeCount.mean()),

            "avg_replies": float(subset.totalReplyCount.mean()),

            "total_likes": int(subset.likeCount.sum()),

            "total_replies": int(subset.totalReplyCount.sum()),

            "representative_comment":
                rep_doc[0] if rep_doc else "",

            "top_comments":
                subset.sort_values(
                    "likeCount",
                    ascending=False
                ).head(5).to_dict("records"),

            # ---------- NEEDS LLM ----------
            "summary": None,
            "category": None,          # love/hate/request/question...
            "creator_takeaway": None,
        })
    
    for t in topics_data:
        value = {
            "topic_name":t['name'],
            "repr_comments":topic_model.get_representative_docs(t['id'])[:5],
            "size_percent":t['percentage'],
            "likes_percentage":t['total_likes']/stats["total_likes"],
            "replies_percentage":t['total_replies']/stats["total_replies"]
        }


        result:dict = _get_summary(value)

        if(result):
            t['summary'] = result['summary']
            t['category'] = result['category']
            t['creator_takeaway'] = result['creator_takeaway']

        else:
            print("oops sorry...couldn't _get_summary")

        # embed()

    # -------------------------
    # Engagement
    # -------------------------

    engagement = []

    for t in topics_data:

        t = (
            t["total_likes"]
            + 5 * t["total_replies"]
        )

        engagement.append({

            "topic": t["name"],

            "score": score,

            "likes": t["total_likes"],

            "replies": t["total_replies"]
        })

    engagement.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # from IPython import embed
    # embed()
    return {
        "video_info":video,

        "stats": stats,

        "topic_distribution": topic_distribution,

        "topics": topics_data,

        "top_liked": top_liked,

        "top_discussions": top_discussions,

        "engagement": engagement,

        "comments": df.to_dict("records")
    }

import re

def _clean_llm_json(raw_text: str):
    """
    Clean and parse JSON-like text from an LLM response.
    Returns a Python dict if successful, else None.
    """
    try:
        # Step 1: Extract JSON substring (between first { and last })
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if match:
            raw_text = match.group(0)

        # Step 2: Remove trailing commas before } or ]
        raw_text = re.sub(r",\s*([\]}])", r"\1", raw_text)

        # Step 3: Try parsing
        return json.loads(raw_text)

    except Exception as e:
        print("Failed to parse JSON:", e)
        return None
    
def _get_summary(value:dict):
    import openai
    client = openai.OpenAI(base_url="http://127.0.0.1:11434/v1",api_key="api_key")
    system_prompt = {"role":"system","content":"""Analyse the given youtube comment data and return result in json STRICTLY like below:
{"category": "Love | Hate | Request | Question | Humor | Suggestion",
  "summary": "...",
  "creator_takeaway": "..."
}"""
                    }
    user_prompt = {"role":"user","content":"\n".join([f"{k} : {v}" for k, v in value.items()])}

    response = client.chat.completions.create(model = "ibm/granite4.1:3b",messages= [system_prompt,user_prompt])
    ans = response.choices[0].message.content
    print("response : ",ans)

    return _clean_llm_json(ans)
