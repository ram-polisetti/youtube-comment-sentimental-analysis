import streamlit as st
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from textblob import TextBlob
import matplotlib.pyplot as plt
import re
import base64
from io import BytesIO
import numpy as np
from tqdm import tqdm

def clean_video_id(video_id):
    """
    Extract the video ID from a full YouTube URL or clean up any additional parameters.

    Args:
    video_id (str): The input video ID or URL.

    Returns:
    str: The cleaned video ID.
    """
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
    """
    Fetch video information from YouTube API.

    Args:
    youtube: The YouTube API client.
    video_id (str): The ID of the video.

    Returns:
    dict: Video information including title, view count, like count, and comment count.
    """
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
        st.error(f"An error occurred: {e}")
        return None

def get_video_comments(youtube, video_id, max_results=None):
    """
    Fetch comments from a YouTube video.

    Args:
    youtube: The YouTube API client.
    video_id (str): The ID of the video.
    max_results (int): The maximum number of comments to fetch. If None, fetch all comments.

    Returns:
    list: A list of comment texts.
    """
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
        st.error(f"An error occurred: {e}")
        return comments

def analyze_sentiment(comments):
    """
    Perform sentiment analysis on a list of comments.

    Args:
    comments (list): A list of comment texts.

    Returns:
    list: A list of sentiment polarity scores.
    """
    sentiments = []
    for comment in comments:
        blob = TextBlob(comment)
        sentiments.append(blob.sentiment.polarity)
    return sentiments

def plot_sentiment(sentiments):
    """
    Create a histogram of sentiment distribution.

    Args:
    sentiments (list): A list of sentiment polarity scores.

    Returns:
    str: Base64 encoded string of the plot image.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(sentiments, bins=50, edgecolor='black')
    plt.title('Sentiment Distribution of YouTube Comments')
    plt.xlabel('Sentiment Polarity')
    plt.ylabel('Frequency')

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    return img_str

def summarize_sentiments(sentiments):
    """
    Summarize the sentiment analysis results.

    Args:
    sentiments (list): A list of sentiment polarity scores.

    Returns:
    dict: A summary of sentiment analysis including counts and averages.
    """
    positive = sum(1 for s in sentiments if s > 0)
    negative = sum(1 for s in sentiments if s < 0)
    neutral = sum(1 for s in sentiments if s == 0)

    avg_sentiment = np.mean(sentiments)
    median_sentiment = np.median(sentiments)

    return {
        'positive': positive,
        'negative': negative,
        'neutral': neutral,
        'average': avg_sentiment,
        'median': median_sentiment
    }

def main():
    st.title("YouTube Comment Sentiment Analysis")

    api_key = st.text_input("Enter your YouTube Data API key:", type="password")
    video_url = st.text_input("Enter the YouTube video URL:")

    if api_key and video_url:
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_id = clean_video_id(video_url)

        video_info = get_video_info(youtube, video_id)

        if video_info:
            st.subheader("Video Information")
            st.write(f"Title: {video_info['title']}")
            st.write(f"Views: {video_info['views']:,}")
            st.write(f"Likes: {video_info['likes']:,}")
            st.write(f"Total Comments: {video_info['comment_count']:,}")

            max_comments = st.number_input("Number of comments to analyze:", min_value=1, max_value=video_info['comment_count'], value=min(1000, video_info['comment_count']))

            if st.button("Analyze Comments"):
                with st.spinner("Fetching and analyzing comments..."):
                    comments = get_video_comments(youtube, video_id, max_comments)
                    sentiments = analyze_sentiment(comments)
                    summary = summarize_sentiments(sentiments)

                    st.subheader("Sentiment Analysis Results")
                    st.write(f"Number of comments analyzed: {len(comments)}")
                    st.write(f"Positive comments: {summary['positive']} ({summary['positive']/len(comments)*100:.2f}%)")
                    st.write(f"Negative comments: {summary['negative']} ({summary['negative']/len(comments)*100:.2f}%)")
                    st.write(f"Neutral comments: {summary['neutral']} ({summary['neutral']/len(comments)*100:.2f}%)")
                    st.write(f"Average sentiment: {summary['average']:.4f}")
                    st.write(f"Median sentiment: {summary['median']:.4f}")

                    img_str = plot_sentiment(sentiments)
                    st.image(f"data:image/png;base64,{img_str}", caption="Sentiment Distribution")

if __name__ == "__main__":
    main()
