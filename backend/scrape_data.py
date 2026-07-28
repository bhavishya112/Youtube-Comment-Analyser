import re
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import json
from pandas import json_normalize

load_dotenv(".env")

API_KEY = os.environ.get("YOUTUBE_API_KEY")
YOUTUBE = build("youtube", "v3", developerKey=API_KEY)


def extract_video_id(url: str) -> str:
    """
    Extracts the YouTube video ID from common URL formats.
    """

    parsed = urlparse(url.strip())

    # https://youtu.be/VIDEO_ID
    if parsed.netloc == "youtu.be":
        return parsed.path.lstrip("/")

    # https://www.youtube.com/watch?v=VIDEO_ID
    if "youtube.com" in parsed.netloc:
        query = parse_qs(parsed.query)
        if "v" in query:
            return query["v"][0]

    # fallback regex
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    if match:
        return match.group(1)

    raise ValueError("Could not extract video ID.")


def download_video_metadata(video_url):
    video_id = extract_video_id(video_url)
    request = YOUTUBE.videos().list(
        part="snippet,statistics",
        id=video_id
    )

    response = request.execute()

    if not response["items"]:
        return None

    item = response["items"][0]

    snippet = item["snippet"]
    statistics = item.get("statistics", {})

    with open(f"data/videos/video_{video_id}.json", "w", encoding="utf-8") as fp:
        json.dump(obj={
            "video_id": video_id,
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "tags": snippet.get("tags", []),
            "category_id": snippet.get("categoryId"),
            "channel_id": snippet.get("channelId"),
            "channel_title": snippet.get("channelTitle"),
            "published_at": snippet.get("publishedAt"),
            "default_language": snippet.get("defaultLanguage"),
            "default_audio_language": snippet.get("defaultAudioLanguage"),
            "view_count": statistics.get("viewCount"),
            "like_count": statistics.get("likeCount"),
            "comment_count": statistics.get("commentCount"),
        },
            fp=fp,
            ensure_ascii=False, indent=4)


def get_video_metadata(video_url: str):
    video_id = extract_video_id(video_url)
    path = f"./data/videos/video_{video_id}.json"
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No comment data found for video id {video_id}")

    with open(path, "r", encoding="utf-8") as fp:
        result = json.load(fp)

    df = json_normalize(result)
    df.columns = [col.split(".")[-1] for col in df.columns]
    df = df[
        [
            "title",
            "description",
            "tags",
            "published_at",
            "default_language",
            "default_audio_language",
            "view_count",
            "like_count",
            "comment_count"
        ]
    ]

    return df

from pathlib import Path
from googleapiclient.errors import HttpError

def download_comment_threads(video_url: str, max_comments: int = 10):
    video_id = extract_video_id(video_url)

    comments = []
    page_size = min(max_comments, 100)

    request = YOUTUBE.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=page_size,
        textFormat="plainText",
        order="relevance",
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

    return df


if __name__ == "__main__":

    url = input("YouTube URL: ")
    download_comment_threads(url, max_comments=50)
    print(get_comments(url).to_markdown)
