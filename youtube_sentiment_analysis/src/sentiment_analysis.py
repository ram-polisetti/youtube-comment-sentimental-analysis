from textblob import TextBlob

def analyze_sentiment(comment):
    """Perform sentiment analysis on a single comment."""
    blob = TextBlob(comment)
    return blob.sentiment.polarity

def analyze_comments(comments):
    """Perform sentiment analysis on a list of comments."""
    return [analyze_sentiment(comment) for comment in comments]

def summarize_sentiments(sentiments):
    """Summarize the sentiment analysis results."""
    positive = sum(1 for s in sentiments if s > 0)
    negative = sum(1 for s in sentiments if s < 0)
    neutral = sum(1 for s in sentiments if s == 0)

    return {
        'positive': positive,
        'negative': negative,
        'neutral': neutral,
        'average': sum(sentiments) / len(sentiments) if sentiments else 0,
        'median': sorted(sentiments)[len(sentiments) // 2] if sentiments else 0
    }
