"""
predict.py
----------
Standalone prediction helper used by both the CLI and Django views.

Usage (CLI):
    conda run -n tf_env python predict.py "This movie was absolutely fantastic!"
"""

import os
import pickle
import sys

from preprocessing import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")
MODEL_PATH = os.path.join(BASE_DIR, "sentiment_model.pkl")


def load_artifacts():
    """Load and return (vectorizer, model).  Raises FileNotFoundError if missing."""
    missing = [p for p in (VECTORIZER_PATH, MODEL_PATH) if not os.path.exists(p)]
    if missing:
        raise FileNotFoundError(
            "Model artefacts not found. Please run `python train.py` first.\n"
            f"Missing: {missing}"
        )
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return vectorizer, model


def predict_sentiment(text: str, vectorizer=None, model=None) -> dict:
    """
    Predict sentiment for *text*.

    Parameters
    ----------
    text       : raw review text
    vectorizer : pre-loaded TfidfVectorizer (loaded from disk if None)
    model      : pre-loaded LogisticRegression (loaded from disk if None)

    Returns
    -------
    dict with keys:
        label      – "Positive" | "Negative"
        confidence – float 0–100 (percentage of winning class)
        proba_pos  – raw probability of Positive class
        proba_neg  – raw probability of Negative class
    """
    if vectorizer is None or model is None:
        vectorizer, model = load_artifacts()

    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])
    proba = model.predict_proba(vec)[0]   # [P(neg), P(pos)]

    proba_neg, proba_pos = float(proba[0]), float(proba[1])
    label = "Positive" if proba_pos >= 0.5 else "Negative"
    confidence = max(proba_pos, proba_neg) * 100

    return {
        "label": label,
        "confidence": round(confidence, 2),
        "proba_pos": round(proba_pos * 100, 2),
        "proba_neg": round(proba_neg * 100, 2),
    }


# ── CLI entry point ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict.py \"<review text>\"")
        sys.exit(1)

    text = " ".join(sys.argv[1:])
    result = predict_sentiment(text)
    print(f"\n Review   : {text[:120]}…" if len(text) > 120 else f"\n Review   : {text}")
    print(f" Sentiment : {result['label']}")
    print(f" Confidence: {result['confidence']:.2f}%")
    print(f" P(Pos)    : {result['proba_pos']:.2f}%  |  P(Neg): {result['proba_neg']:.2f}%\n")
