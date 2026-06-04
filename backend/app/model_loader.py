import joblib

# load model
model = joblib.load(
    "models/logistic_regression_model_v1.pkl"
)

# load tfidf
tfidf = joblib.load(
    "models/tfidf.pkl"
)