import streamlit as st
from googleapiclient.discovery import build
from src.data_collection import clean_video_id, get_video_info, get_video_comments
from src.preprocessing import preprocess_comments
from src.sentiment_analysis import analyze_comments, summarize_sentiments
from src.visualization import plot_sentiment
import config

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
                    preprocessed_comments = preprocess_comments(comments)
                    sentiments = analyze_comments(preprocessed_comments)
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
