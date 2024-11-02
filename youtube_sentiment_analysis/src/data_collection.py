from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def clean_video_id(video_id):
    """Extract the video ID from a full YouTube URL or clean up any additional parameters."""
    import re
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'^([\w-]{11})$',
        r'(?:youtu\.be\/|youtube\.com\/embed\/)?([\w-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, video_id)
        if match:
            return match.group(1)
    return video_id

def get_video_info(youtube, video_id):
    """Fetch video information from YouTube API."""
    try:
        video_response = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()

        if not video_response['items']:
            return None

        video_data = video_response['items'][0]
        return {
            'title': video_data['snippet']['title'],
            'views': int(video_data['statistics']['viewCount']),
            'likes': int(video_data['statistics'].get('likeCount', 0)),
            'comment_count': int(video_data['statistics'].get('commentCount', 0))
        }
    except HttpError as e:
        print(f"An error occurred: {e}")
        return None

def get_video_comments(youtube, video_id, max_results=None):
    """Fetch comments from a YouTube video."""
    comments = []
    results = None

    try:
        while True:
            if results is None:
                results = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    maxResults=100
                ).execute()
            else:
                if 'nextPageToken' not in results:
                    break
                results = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    maxResults=100,
                    pageToken=results['nextPageToken']
                ).execute()

            for item in results['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
                if max_results and len(comments) >= max_results:
                    return comments

        return comments
    except HttpError as e:
        print(f"An error occurred: {e}")
        return comments
