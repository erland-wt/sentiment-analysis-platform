from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR /
    "models" /
    "logistic_regression_model_v1.pkl"
)

TFIDF_PATH = (
    BASE_DIR /
    "models" /
    "tfidf.pkl"
)

model = joblib.load(
    MODEL_PATH
)

tfidf = joblib.load(
    TFIDF_PATH
)