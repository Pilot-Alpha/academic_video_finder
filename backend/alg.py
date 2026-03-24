import requests
import re
import math
from operator import itemgetter
from datetime import datetime
import os
API_KEY = os.getenv("YOUTUBE_API_KEY")


SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"

grade_aliases = {
    "SSC": ["ssc", "class 9", "class 10", "9", "10"],
    "HSC": ["hsc", "class 11", "class 12", "11", "12"]
}

video_type_aliases = {
     "problem-solving" : ["solution", "problem solving", "question", "questions", "cq", "mcq"],
     "revision": ["revision", "repeat", "short", "revisit"],
     "first-time": ["first time", "full explained", "full class", "academic class"],
     "one-shot" : ["one shot, one-shot", "marathon"]
}

def keyword_score(text, chapter):
    score = 0
    for word in chapter.lower().split():
        if word in text.lower():
            score += 1
    return score

def keyword_score_video_type(text, video_type):
    score = 0
    if any(alias in text for alias in video_type_aliases.get(video_type, [])):
        score += 1
    return score

def matches_grade(title, grade):
    title = title.lower()
    return any(alias in title for alias in grade_aliases.get(grade, []))

def matches_chapter(title, chapter):
    return any(word.lower() in title.lower()for word in chapter.split())

def parse_duration(duration):
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds

def find_video(grade, subject, chapter, video_type):
    key_words = f"{subject} {chapter} {grade} {video_type} Bangla Lecture"
    params = {
        "part": "snippet",
        "q": key_words,
        "type": "video",
        "maxResults": 50,
        "order": "relevance",
        "key": API_KEY
    }
    
    res = requests.get(SEARCH_URL, params=params)

    search_result = res.json()

    video_ids = [item['id']['videoId'] for item in search_result['items']]

    params = {
        "part": "snippet,statistics,contentDetails",
        "id": ",".join(video_ids),
        "key": API_KEY
    }

    res = requests.get(VIDEOS_URL, params=params)
    videos_info = res.json()

    videos = []
    for video in videos_info['items']:
        info = {
        "title": video['snippet']['title'],
        "description": video['snippet']['description'],
        "publishedAt": video['snippet']['publishedAt'],
        "channelId": video['snippet']['channelId'],
        "views": int(video['statistics'].get('viewCount', 0)),
        "likes": int(video['statistics'].get('likeCount', 0)),
        "comments": int(video['statistics'].get('commentCount', 0)),
        "duration": parse_duration(video['contentDetails']['duration']),
        "url": f"https://www.youtube.com/watch?v={video['id']}"
        }
        videos.append(info)
    
    best_videos = []

    for video in videos:

        score = 0
        
        title = video["title"]
        description = video["description"]
        views = video["views"]        
        likes = video["likes"]
        comments = video["comments"]
        duration = video["duration"]
        url = video["url"]
        published_date = datetime.strptime(video['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        days_old = (datetime.utcnow() - published_date).days
        
        
        recency_score = 50 / (math.log10(days_old + 10))
        score += recency_score

        if duration < 600:
            continue


        
        if matches_grade(title, grade):
            score += 20

        if matches_chapter(title, chapter) or matches_chapter(description, chapter):
            score += 20


        trusted_channels = ["acs", "udvash", "unmesh", "10ms", "bondi", "pathshala", "hulkenstein", "lobdhi"]

        if any(ch in title.lower() for ch in trusted_channels) or \
        any(ch in description.lower() for ch in trusted_channels):
            score += 40

        
        score += keyword_score(title, chapter) * 15
        score += keyword_score(description, chapter) * 8

        score += keyword_score_video_type(title, video_type=video_type) * 25
        score += keyword_score_video_type(description, video_type=video_type) * 10


        score += math.log10(views + 1) * 5
        score += math.log10(comments + 1) * 5
        if views != 0:
            score += (likes/(views+100)) * 15

        best_videos.append(
            {
                'score': score,
                'url': url
            }
        )

    if not best_videos:
        return None
    
    
    best_videos_sorted = sorted(best_videos, key=itemgetter('score'), reverse=True)

    for item in best_videos_sorted:
        item['url'] = item['url'].replace("watch?v=", "embed/")

    return best_videos_sorted

