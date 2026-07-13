# 🎬 SentiScope – IMDb Movie Review Sentiment Analyzer

An end-to-end **Sentiment Analysis** web application that classifies IMDb movie reviews as **Positive** or **Negative** using a **TF-IDF + Logistic Regression** pipeline, served through a premium **Django** web interface.

---

## 📁 Project Structure

```
movie_comment_analysis/
│
├── IMDB Dataset.csv          ← IMDb dataset (auto-detected)
│
├── preprocessing.py          ← Text cleaning utilities
├── train.py                  ← Model training script
├── predict.py                ← Inference helper (CLI + Django)
│
├── vectorizer.pkl            ← (generated) TF-IDF vectorizer
├── sentiment_model.pkl       ← (generated) Trained LR model
├── training_report.txt       ← (generated) Evaluation metrics
│
├── manage.py                 ← Django management entry-point
├── requirements.txt          ← Python dependencies
│
├── sentiment_app/            ← Django project package
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── analyzer/                 ← Django app
    ├── __init__.py
    ├── apps.py
    ├── urls.py
    ├── views.py
    └── templates/
        └── analyzer/
            ├── base.html     ← Shared layout
            ├── home.html     ← Prediction form page
            └── about.html    ← Model information page
```

---

## ⚙️ Setup & Usage

### Prerequisites
- Conda environment **`tf_env`** with Python 3.11+
- IMDb dataset CSV in the project directory (auto-detected)

### 1 · Install Dependencies

```bash
conda run -n tf_env pip install -r requirements.txt
```

### 2 · Train the Model

```bash
conda run -n tf_env python train.py
```

This will:
- Auto-detect the IMDb CSV in the current directory
- Clean and preprocess all 50,000 reviews
- Train a TF-IDF (50K features, unigrams+bigrams) + Logistic Regression model
- Print and save evaluation metrics to `training_report.txt`
- Save `vectorizer.pkl` and `sentiment_model.pkl`

**Expected output:**
```
Accuracy  : 0.8940  (89.40%)
Precision : 0.8912
Recall    : 0.8975
F1-Score  : 0.8943
```

### 3 · Start the Django Server

```bash
conda run -n tf_env python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

### 4 · Command-Line Prediction (optional)

```bash
conda run -n tf_env python predict.py "This film was absolutely brilliant!"
```

---

## 🧪 Model Details

| Component | Choice |
|---|---|
| Vectorizer | TF-IDF (max 50K features, (1,2)-grams, sublinear TF) |
| Classifier | Logistic Regression (C=1.0, max_iter=1000) |
| Train/Test Split | 80% / 20% (stratified) |
| Text Cleaning | HTML strip, lowercase, remove punctuation, remove stopwords |
| Dataset | IMDb 50K Movie Reviews (balanced, 25K pos / 25K neg) |

---

## 📊 Evaluation Metrics Displayed

- ✅ Accuracy
- ✅ Precision
- ✅ Recall
- ✅ F1-Score
- ✅ Confusion Matrix
- ✅ Full Classification Report

All metrics are saved to `training_report.txt` and displayed in the Django web UI.

---

## 🌐 Django Web Interface

| Page | URL | Description |
|---|---|---|
| Home | `/` | Review input form + prediction results |
| About | `/about/` | Model details, pipeline, tech stack |

**Features:**
- 🎬 Premium dark-mode UI with glassmorphism
- ⚡ Real-time sentiment prediction with confidence score
- 📊 Visual confidence bar + probability pills
- 🔖 Sample review chips to test quickly
- 📋 Collapsible training evaluation report

---

## 🛠 Tech Stack

- **Python** 3.11 (conda: tf_env)
- **scikit-learn** – TF-IDF, Logistic Regression, metrics
- **pandas** – dataset loading and processing
- **Django** 5.x – web framework
- **NLTK** (optional) – enhanced English stopwords

---

## 📜 License

MIT – for educational purposes.
