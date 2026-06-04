from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import numpy as np

from app.schemas import SentimentRequest
from app.preprocessing import preprocess_text
from app.model_loader import model, tfidf
from app.utils import split_sentences

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://sentiment-analysis-plat-git-93a5d3-erland-widyatamakas-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_summary(sentiment):

    if sentiment == "positive":
        return (
            "Berita Baik. Mayoritas isi teks "
            "mengandung sentimen positif."
        )

    elif sentiment == "negative":
        return (
            "Berita Buruk. Mayoritas isi teks "
            "mengandung sentimen negatif."
        )

    return (
        "Berita Netral. Isi teks "
        "cenderung informatif atau seimbang."
    )

@app.get("/")
def home():
    return {
        "message": "Sentiment Analysis API Running"
    }


@app.post("/predict")
def predict_sentiment(request: SentimentRequest):

    raw_text = request.text

    # overall preprocessing
    clean_text = preprocess_text(raw_text)

    # vectorize
    vectorized_text = tfidf.transform(
        [clean_text]
    )

    # overall prediction
    overall_prediction = model.predict(
        vectorized_text
    )[0]
    
    probabilities = model.predict_proba(
        vectorized_text
    )[0]

    confidence = float(
        np.max(probabilities)
    )

    # split per sentence
    sentences = split_sentences(raw_text)

    sentence_results = []

    for sentence in sentences:

        clean_sentence = preprocess_text(
            sentence
        )

        vectorized_sentence = tfidf.transform(
            [clean_sentence]
        )

        prediction = model.predict(
            vectorized_sentence
        )[0]

        sentence_results.append({
            "sentence": sentence,
            "clean_sentence": clean_sentence,
            "sentiment": prediction
        })
    
    positive_count = sum(
        1 for item in sentence_results
        if item["sentiment"] == "positive"
    )

    neutral_count = sum(
        1 for item in sentence_results
        if item["sentiment"] == "neutral"
    )

    negative_count = sum(
        1 for item in sentence_results
        if item["sentiment"] == "negative"
    )
    
    total_sentences = max(
        len(sentence_results),
        1
    )
        
    positive_percentage = round(
    positive_count / total_sentences * 100,
        2
    )

    neutral_percentage = round(
        neutral_count / total_sentences * 100,
        2
    )

    negative_percentage = round(
        negative_count / total_sentences * 100,
        2
    )

    return {
        "overall_sentiment": overall_prediction,
        "summary": generate_summary(
            overall_prediction
        ),
        "confidence": confidence,
        "sentences": sentence_results,

        "statistics": {
            "positive": positive_count,
            "neutral": neutral_count,
            "negative": negative_count,

            "positive_percentage":
                positive_percentage,
            "neutral_percentage":
                neutral_percentage,
            "negative_percentage":
                negative_percentage
        }
    }