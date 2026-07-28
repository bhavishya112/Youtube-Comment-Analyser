V.I.S.I.O.N.<br>-Viewer Insight & Sentiment Intelligence Optimization Network


# Project Flow

<div align = "center">
URL <br>
↓<br> 
Comments

 ↓ 

(Cleaning)

↓



$$

\left.\begin{array}{l}
\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \  
\end{array}
\right.
\left.\begin{array}{c}
Embeddings \\ 
\\
\downarrow \\
\\
HDBSCAN \\
\\
\downarrow \\
\\
Topic \space Clusters
\end{array}
 \right\}  - Bertopic


 
 
$$

↓

(Visualize)

↓

Prepare Dashboard Data

↓ 

Dashboard

</div>

# Dashboard

Praise
Criticism
Suggestion
Question
Request
Bug / Error
Humor
Meme
Spam
Confusion
Emotion<br>Other

### Variables to prepare :

`video` = {
    "title": "",
    "channel": "",
    "thumbnail": "",
    "published_at": "",
    "views": 0,
    "likes": 0,
    "comment_count": 0,
    "duration": "",
    "url": ""
}

`stats` = {
    "total_comments": 0,
    "unique_authors": 0,
    "total_likes": 0,
    "total_replies": 0,

```
"avg_likes": 0,
"avg_replies": 0,

"topics_found": 0,
"noise_comments": 0,

"largest_topic_size": 0
}
```

`categories` = {
    "love": 0,
    "hate": 0,
    "request": 0,
    "question": 0,
    "humor": 0,
    "suggestion": 0,
    "spam": 0
}

`topic_distribution` = [
    {
        "topic":"Editing",
        "count":423
    },
    {
        "topic":"Music",
        "count":312
    }
]

`top_liked` = [

{
"text":"",

"likes":10234,

"topic":"Editing"
}

]

`top_discussions` = [

{
"text":"",

"replies":84,

"topic":"Thumbnail"
}

]

`topics_data` = [

{
"id":0,

"name":"Editing",

"size":423,

"percentage":24.3,

"keywords":[
"editing",
"transition",
"camera"
],

"category":"love",

"avg_likes":18,

"avg_replies":4,

"representative_comment":"The editing deserves an Oscar.",

"summary":"Viewers overwhelmingly praised the editing quality.",

"top_comments":[
...
]

}

]

`comments` = [

{
"author":"John",

"text":"Amazing editing",

"likes":51,

"replies":3,

"date":"",

"topic":"Editing",

"category":"love"

}

]

`engagement` = [

{
"topic":"Editing",

"likes":18200,

"replies":2310,

"score":24500

}

]

`topic_sentiment` = [

{

"topic":"Editing",

"love":91,

"hate":4,

"request":5

}

]

`insights` = {

"strengths":[

"Editing",

"Music"

],

"weaknesses":[

"Thumbnail",

"Audio"

],

"requests":[

"Part 2",

"Tutorial"

],

"summary":"..."

}

`edges` = [

("Editing","Music",0.83),

("Thumbnail","Clickbait",0.75)

]

`timeline` = [

{

"hour":1,

"Editing":23,

"Thumbnail":8,

"Music":4

}]

### *Prepared Variables* :

<pre><code>
video_info : list(dict_keys(['title', 'description', 'tags', 'published_at', 'default_language', 'default_audio_language', 'view_count', 'like_count', 'comment_count']))

------------------------------------------------------------

stats : dict_keys(['total_comments', 'unique_authors', 'total_likes', 'total_replies', 'avg_likes', 'avg_replies', 'topics_found', 'noise_comments'])

<!-- ------------------------------------------------------------

topic_distribution : list(dict_keys(['topic_id', 'topic_name', 'count']))

------------------------------------------------------------ -->

topics : list(dict_keys(['id', 'name', 'confidence', 'size', 'percentage', 'keywords', 'avg_likes', 'avg_replies', 'total_likes', 'total_replies', 'representative_comment', 'top_comments', 'summary', 'category', 'creator_takeaway']))

------------------------------------------------------------

top_liked : list(dict_keys(['authorDisplayName', 'textOriginal', 'likeCount', 'publishedAt', 'updatedAt', 'totalReplyCount', 'topic_id', 'prob', 'topic_name']))

------------------------------------------------------------

top_discussions : list(dict_keys(['authorDisplayName', 'textOriginal', 'likeCount', 'publishedAt', 'updatedAt', 'totalReplyCount', 'topic_id', 'prob', 'topic_name']))

------------------------------------------------------------

engagement : list(dict_keys(['topic', 'score', 'likes', 'replies']))

------------------------------------------------------------

comments : list(dict_keys(['authorDisplayName', 'textOriginal', 'likeCount', 'publishedAt', 'updatedAt', 'totalReplyCount', 'topic_id', 'prob', 'topic_name']))

------------------------------------------------------------

</code></pre>

### Layout : 

--------------------------------------------------------
(LLM CALL 3)
AI Insights

Strengths
Weaknesses
Requests


```
------------------------------------------------------------------
                            Video
                Views | likes | comments | language 
-----------------------------------------------------------------
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Topics   │ │ Love     │ │ Hate     │ | Requests │ │Suggestion│
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
--------------------------------------------------------------------
Share of Categories in comments     Tags of the video 
(Pie Chart)                          (Word Cloud)


--------------------------------------------------------
Topic Distribution              Topics Discussed over time
(By likes,comments,replies)     (Line Chart)

██████████████ Editing
██████████ Music
██████ Thumbnail

--------------------------------------------------------

Detailed Topic Explorer

▼ Editing

Summary

Creator Takeaway

Representative comment

Top comments

```

## UI Generation

### Make Landing Page

### Dashboard Graphs (More)

*video_info*<br>
Tags: word cloud or bar chart of tag frequency.

*topics over time*<br>Line Chart that shows over time what topics are commented and how much

*Noise vs Topics Found*<br>stacked bar or donut chart.

*Pie Chart*<br> share of different categories (in total comments)





