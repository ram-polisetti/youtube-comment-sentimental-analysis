import matplotlib.pyplot as plt
import base64
from io import BytesIO

def plot_sentiment(sentiments):
    """Create a histogram of sentiment distribution."""
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
