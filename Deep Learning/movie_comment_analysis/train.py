"""
train.py
--------
Trains a TF-IDF + Logistic Regression sentiment classifier on the IMDb dataset.

Usage:
    conda run -n tf_env python train.py

Outputs:
    vectorizer.pkl          – fitted TfidfVectorizer
    sentiment_model.pkl     – fitted LogisticRegression model
    training_report.txt     – full classification report + confusion matrix
"""

import glob
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from preprocessing import clean_series

# ── Constants ────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")
MODEL_PATH = os.path.join(BASE_DIR, "sentiment_model.pkl")
REPORT_PATH = os.path.join(BASE_DIR, "training_report.txt")

RANDOM_STATE = 42
TEST_SIZE = 0.20
MAX_FEATURES = 50_000
NGRAM_RANGE = (1, 2)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _find_csv(directory: str) -> str:
    """Auto-detect the first CSV file in *directory* (case-insensitive match)."""
    patterns = [
        os.path.join(directory, "*.csv"),
        os.path.join(directory, "**", "*.csv"),
    ]
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        if files:
            # Prefer files whose name contains 'imdb' or 'sentiment'
            preferred = [
                f for f in files
                if any(kw in os.path.basename(f).lower() for kw in ("imdb", "sentiment", "movie"))
            ]
            return preferred[0] if preferred else files[0]
    raise FileNotFoundError(
        "No CSV file found in the current directory. "
        "Please place the IMDb dataset CSV here."
    )


def _load_dataset(csv_path: str) -> pd.DataFrame:
    """Load the IMDb CSV and normalise column names."""
    print(f"[INFO] Loading dataset: {os.path.basename(csv_path)}")
    df = pd.read_csv(csv_path)

    # Identify review and label columns flexibly
    review_col = next(
        (c for c in df.columns if "review" in c.lower() or "text" in c.lower()), None
    )
    label_col = next(
        (c for c in df.columns if "sentiment" in c.lower() or "label" in c.lower()), None
    )

    if review_col is None or label_col is None:
        raise ValueError(
            f"Could not identify review/label columns. Found: {list(df.columns)}"
        )

    df = df[[review_col, label_col]].rename(
        columns={review_col: "review", label_col: "sentiment"}
    )
    df.dropna(inplace=True)

    # Normalise labels → 0 / 1
    unique_labels = df["sentiment"].unique()
    if set(unique_labels) <= {"positive", "negative", "pos", "neg"}:
        df["label"] = df["sentiment"].map(
            lambda x: 1 if str(x).lower() in ("positive", "pos") else 0
        )
    else:
        df["label"] = df["sentiment"].astype(int)

    print(f"[INFO] Dataset size: {len(df):,} rows  |  "
          f"Positive: {df['label'].sum():,}  |  Negative: {(df['label'] == 0).sum():,}")
    return df


# ── Main training pipeline ────────────────────────────────────────────────────

def train():
    t0 = time.time()

    # 1. Locate & load CSV
    csv_path = _find_csv(BASE_DIR)
    df = _load_dataset(csv_path)

    # 2. Clean text
    print("[INFO] Cleaning text …")
    df["clean_review"] = clean_series(df["review"])

    # 3. Train / test split
    X = df["clean_review"]
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"[INFO] Train: {len(X_train):,}  |  Test: {len(X_test):,}")

    # 4. TF-IDF vectorisation
    print("[INFO] Fitting TF-IDF vectorizer …")
    vectorizer = TfidfVectorizer(
        max_features=MAX_FEATURES,
        ngram_range=NGRAM_RANGE,
        sublinear_tf=True,
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # 5. Train Logistic Regression
    print("[INFO] Training Logistic Regression …")
    model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, C=1.0)
    model.fit(X_train_tfidf, y_train)

    # 6. Evaluate
    y_pred = model.predict(X_test_tfidf)
    accuracy  = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="binary")
    recall    = recall_score(y_test, y_pred, average="binary")
    f1        = f1_score(y_test, y_pred, average="binary")
    cm        = confusion_matrix(y_test, y_pred)
    report    = classification_report(y_test, y_pred, target_names=["Negative", "Positive"])

    # 7. Print results
    separator = "=" * 60
    results = (
        f"\n{separator}\n"
        f"  SENTIMENT ANALYSIS – EVALUATION RESULTS\n"
        f"{separator}\n"
        f"  Accuracy  : {accuracy:.4f}  ({accuracy*100:.2f}%)\n"
        f"  Precision : {precision:.4f}\n"
        f"  Recall    : {recall:.4f}\n"
        f"  F1-Score  : {f1:.4f}\n"
        f"{separator}\n"
        f"  Confusion Matrix:\n"
        f"  {cm}\n"
        f"  (rows=Actual, cols=Predicted | 0=Negative, 1=Positive)\n"
        f"{separator}\n"
        f"  Classification Report:\n\n"
        f"{report}\n"
        f"{separator}\n"
        f"  Training time: {time.time() - t0:.1f}s\n"
        f"{separator}\n"
    )
    print(results)

    # 8. Save report to file
    with open(REPORT_PATH, "w") as f:
        f.write(results)
    print(f"[INFO] Report saved → {REPORT_PATH}")

    # 9. Persist artefacts
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
    print(f"[INFO] Vectorizer saved → {VECTORIZER_PATH}")

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"[INFO] Model saved → {MODEL_PATH}")

    print("\n✅  Training complete. You can now run the Django app.\n")

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "confusion_matrix": cm.tolist(),
        "classification_report": report,
    }


if __name__ == "__main__":
    train()
