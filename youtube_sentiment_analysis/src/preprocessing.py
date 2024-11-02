import re

def preprocess_text(text):
    """Preprocess the text by removing special characters, links, etc."""
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_comments(comments):
    """Preprocess a list of comments."""
    return [preprocess_text(comment) for comment in comments]
