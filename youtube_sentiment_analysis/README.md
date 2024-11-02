# YouTube Comment Sentiment Analysis

This project performs sentiment analysis on YouTube video comments using the YouTube Data API and TextBlob for natural language processing.

## Project Structure

```
youtube_sentiment_analysis/
├── data/                  # Directory for storing any data files (if needed)
├── models/                # Directory for storing trained models (if applicable)
├── src/                   # Source code for the project
│   ├── __init__.py
│   ├── data_collection.py # Functions for collecting data from YouTube API
│   ├── preprocessing.py   # Functions for text preprocessing
│   ├── sentiment_analysis.py # Functions for sentiment analysis
│   └── visualization.py   # Functions for data visualization
├── app.py                 # Main Streamlit application
├── config.py              # Configuration settings
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## Setup and Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/youtube-sentiment-analysis.git
   cd youtube-sentiment-analysis
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Obtain a YouTube Data API key:
   - Go to the [Google Developers Console](https://console.developers.google.com/)
   - Create a new project or select an existing one
   - Enable the YouTube Data API v3 for your project
   - Create credentials (API key) for the YouTube Data API

## Running the Application

To run the Streamlit app:

```
streamlit run app.py
```

This will start the application and open it in your default web browser. If it doesn't open automatically, you can access it at the URL shown in the terminal (usually http://localhost:8501).

## Usage

1. When the app loads, you'll see a text input field asking for your YouTube Data API key. Enter the API key you obtained from the Google Developers Console.

2. In the next field, paste the URL of the YouTube video you want to analyze.

3. Use the number input to specify how many comments you want to analyze. The default is set to 1000, but you can adjust this based on your needs and the video's comment count.

4. Click the "Analyze Comments" button to start the analysis.

5. The app will display:
   - Basic video information (title, views, likes, comment count)
   - A summary of the sentiment analysis results
   - A visualization of the sentiment distribution

## Troubleshooting

- If you encounter any issues with missing modules, make sure you've activated your virtual environment (if you created one) and installed all requirements.
- If you get an error related to the YouTube API, double-check that your API key is correct and has the necessary permissions.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.
