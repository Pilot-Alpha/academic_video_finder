import requests
import re

API_KEY = "AIzaSyC1-EQwFTWeuWUBsb_-0i4A5dUjgA23Ufc"

SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"

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

        if duration < 3600:
            continue

        title_match_chapter = False
        title_match_class = False

        for word in chapter.split():
            if any(word.lower() in title.lower() for word in chapter.split()):
                title_match_chapter = True

        for word in grade.split():
            if any(word.lower() in title.lower() for word in grade.split()):
                title_match_class = True

        if title_match_chapter == False or title_match_class == False:
            continue


        if any(item.lower() == 'acs' for item in title.split()) or any(item.lower() == 'udvash' for item in title.split()) or any(item.lower() == 'unmesh' for item in title.split()) or any(item.lower() == '10ms' for item in title.split()) or any(item.lower() == 'bondi' for item in title.split()) or any(item.lower() == 'pathshala' for item in title.split()) or any(item.lower() == 'acs' for item in description.split()) or any(item.lower() == 'udvash' for item in description.split()) or any(item.lower() == 'unmesh' for item in description.split()) or any(item.lower() == '10ms' for item in description.split()) or any(item.lower() == 'bondi' for item in description.split()) or any(item.lower() == 'pathshala' for item in description.split()):
            score += 20

        score += (views/500000) * 10
        score += (comments/1000) * 5
        score += (likes/views) * 10

        best_videos.append(
            {
                'score': score,
                'url': url
            }
        )

    if not best_videos:
        return None
    
    top_score = best_videos[0]['score']
    best_video_url = best_videos[0]['url']
    
    for video in best_videos:
        if video['score'] > top_score:
            best_video_url = video['url']
        
    return best_video_url

print(find_video("SSC", "Physics", "Vector", "One Shot"))