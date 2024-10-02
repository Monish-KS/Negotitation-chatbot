# app/sentiment.py

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(user_offer):
    """
    Analyzes the sentiment of the input text.
    Returns 'positive', 'neutral', or 'negative'.
    """
    text = str(user_offer)
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    else:
        return "neutral"
