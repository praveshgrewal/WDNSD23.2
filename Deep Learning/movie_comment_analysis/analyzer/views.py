"""
analyzer/views.py
-----------------
Django views for the Sentiment Analysis web app.

Artefacts (vectorizer.pkl + sentiment_model.pkl) are loaded once at module
import time so that every HTTP request is served from memory.
"""

import os
import sys

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

# Ensure the project root (where predict.py lives) is on sys.path
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# ── Load artefacts once ───────────────────────────────────────────────────────
_VECTORIZER = None
_MODEL = None
_LOAD_ERROR = None

try:
    from predict import load_artifacts, predict_sentiment as _predict
    _VECTORIZER, _MODEL = load_artifacts()
except FileNotFoundError as e:
    _LOAD_ERROR = str(e)
except Exception as e:
    _LOAD_ERROR = f"Unexpected error loading model: {e}"


# ── Training report ───────────────────────────────────────────────────────────
_REPORT_PATH = os.path.join(_PROJECT_ROOT, "training_report.txt")

def _read_report() -> str:
    if os.path.exists(_REPORT_PATH):
        with open(_REPORT_PATH, "r") as f:
            return f.read()
    return None


# ── Views ─────────────────────────────────────────────────────────────────────

def home(request):
    """Render the home page with the review input form."""
    context = {
        "model_ready": _LOAD_ERROR is None,
        "load_error": _LOAD_ERROR,
        "training_report": _read_report(),
    }
    return render(request, "analyzer/home.html", context)


@require_http_methods(["POST"])
def predict_view(request):
    """Handle POST form submission and return prediction result."""
    review_text = request.POST.get("review", "").strip()

    if not review_text:
        return render(request, "analyzer/home.html", {
            "model_ready": _LOAD_ERROR is None,
            "load_error": _LOAD_ERROR,
            "training_report": _read_report(),
            "error": "Please enter a review before clicking Predict.",
            "review_text": review_text,
        })

    if _LOAD_ERROR:
        return render(request, "analyzer/home.html", {
            "model_ready": False,
            "load_error": _LOAD_ERROR,
            "training_report": _read_report(),
            "review_text": review_text,
        })

    result = _predict(review_text, vectorizer=_VECTORIZER, model=_MODEL)

    context = {
        "model_ready": True,
        "load_error": None,
        "training_report": _read_report(),
        "review_text": review_text,
        "result": result,
    }
    return render(request, "analyzer/home.html", context)


def about(request):
    """Static about page with model and dataset information."""
    return render(request, "analyzer/about.html", {
        "model_ready": _LOAD_ERROR is None,
        "training_report": _read_report(),
    })
