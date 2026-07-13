"""
preprocessing.py
----------------
Text cleaning utilities for IMDb Sentiment Analysis.
Handles: HTML stripping, lowercasing, punctuation removal, stopword filtering.
"""

import re
import string

# Attempt to use NLTK stopwords; fall back to a built-in set if unavailable.
try:
    import nltk
    from nltk.corpus import stopwords as _sw

    try:
        _STOPWORDS = set(_sw.words("english"))
    except LookupError:
        nltk.download("stopwords", quiet=True)
        _STOPWORDS = set(_sw.words("english"))

except ImportError:
    # Minimal English stop-word list used when NLTK is not installed.
    _STOPWORDS = {
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
        "your", "yours", "yourself", "yourselves", "he", "him", "his",
        "himself", "she", "her", "hers", "herself", "it", "its", "itself",
        "they", "them", "their", "theirs", "themselves", "what", "which",
        "who", "whom", "this", "that", "these", "those", "am", "is", "are",
        "was", "were", "be", "been", "being", "have", "has", "had", "having",
        "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if",
        "or", "because", "as", "until", "while", "of", "at", "by", "for",
        "with", "about", "against", "between", "into", "through", "during",
        "before", "after", "above", "below", "to", "from", "up", "down",
        "in", "out", "on", "off", "over", "under", "again", "further",
        "then", "once", "here", "there", "when", "where", "why", "how",
        "all", "both", "each", "few", "more", "most", "other", "some",
        "such", "no", "nor", "not", "only", "own", "same", "so", "than",
        "too", "very", "s", "t", "can", "will", "just", "don", "should",
        "now", "d", "ll", "m", "o", "re", "ve", "y", "ain", "aren",
        "couldn", "didn", "doesn", "hadn", "hasn", "haven", "isn", "ma",
        "mightn", "mustn", "needn", "shan", "shouldn", "wasn", "weren",
        "won", "wouldn",
    }

_HTML_TAG = re.compile(r"<[^>]+>")
_PUNCT_TABLE = str.maketrans("", "", string.punctuation)
_MULTI_SPACE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """
    Full cleaning pipeline:
      1. Strip HTML tags
      2. Lowercase
      3. Remove punctuation
      4. Remove stopwords
      5. Collapse extra whitespace
    """
    if not isinstance(text, str):
        return ""

    # 1. Strip HTML
    text = _HTML_TAG.sub(" ", text)

    # 2. Lowercase
    text = text.lower()

    # 3. Remove punctuation
    text = text.translate(_PUNCT_TABLE)

    # 4. Remove stopwords
    tokens = text.split()
    tokens = [t for t in tokens if t and t not in _STOPWORDS]

    # 5. Rejoin and collapse spaces
    text = _MULTI_SPACE.sub(" ", " ".join(tokens)).strip()
    return text


def clean_series(series):
    """Apply clean_text to a pandas Series and return a new Series."""
    return series.map(clean_text)
