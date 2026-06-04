import os
import urllib.request
import joblib

MODEL_DIR = "models"

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "logistic_regression_model_v1.pkl"
)

TFIDF_PATH = os.path.join(
    MODEL_DIR,
    "tfidf.pkl"
)

MODEL_URL = (
    "https://raw.githubusercontent.com/"
    "erland-wt/"
    "sentiment-analysis-platform/"
    "main/"
    "backend/"
    "models/"
    "logistic_regression_model_v1.pkl"
)

TFIDF_URL = (
    "https://raw.githubusercontent.com/"
    "erland-wt/"
    "sentiment-analysis-platform/"
    "main/"
    "backend/"
    "models/"
    "tfidf.pkl"
)

if not os.path.exists(MODEL_PATH):
    print("Downloading model...")
    urllib.request.urlretrieve(
        MODEL_URL,
        MODEL_PATH
    )

if not os.path.exists(TFIDF_PATH):
    print("Downloading TF-IDF...")
    urllib.request.urlretrieve(
        TFIDF_URL,
        TFIDF_PATH
    )

model = joblib.load(
    MODEL_PATH
)

tfidf = joblib.load(
    TFIDF_PATH
)