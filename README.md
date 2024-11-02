# YouTube Comment Sentiment Analysis App

This Streamlit app performs sentiment analysis on YouTube video comments using the YouTube Data API and TextBlob for natural language processing.

## Features

- Fetch video information (title, views, likes, comment count)
- Analyze sentiment of video comments
- Visualize sentiment distribution
- Customizable number of comments to analyze

## How it works

1. The app uses the YouTube Data API to fetch video information and comments.
2. It cleans and processes the comments using regular expressions.
3. Sentiment analysis is performed using TextBlob, which assigns a polarity score to each comment.
4. The results are summarized and visualized using matplotlib.

## Setup and Running the App

1. Clone this repository.
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```
   streamlit run youtube_sentiment_analysis.py
   ```

## Usage

1. Enter your YouTube Data API key.
2. Paste the URL of the YouTube video you want to analyze.
3. Adjust the number of comments to analyze if desired.
4. Click "Analyze Comments" to start the analysis.

## Code Structure

- `clean_video_id()`: Extracts the video ID from a YouTube URL.
- `get_video_info()`: Fetches basic information about the video.
- `get_video_comments()`: Retrieves comments from the video.
- `analyze_sentiment()`: Performs sentiment analysis on the comments.
- `plot_sentiment()`: Creates a histogram of sentiment distribution.
- `summarize_sentiments()`: Calculates summary statistics of the sentiment analysis.

## Note

Ensure you have a valid YouTube Data API key with the necessary permissions to access video information and comments.
