# Project Flow

Comments

 ↓ 

(Cleaning)

↓

 Embeddings          }

↓                               |  

 HDBSCAN              |----------Bertopic (topic_clustering.py)

↓                               |

Topic Clusters       }

↓

(Visualize)

↓

Build Dashboard data (Topic Clusters)

↓ 

Dashboard

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

}

]



## UI Generation

- Generate Streamlit UI 