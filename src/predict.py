import os
import joblib
import numpy as np

# ---------------- Paths ----------------
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "../models/model.pkl")

# ---------------- Load Model ONCE ----------------
model = joblib.load(MODEL_PATH)

# ---------------- Features ----------------
FEATURES = [
    "sent_neg",
    "sent_pos",
    "sent_compound",
    "liwc_anxiety",
    "liwc_sadness",
    "liwc_negative_emotion",
    "liwc_positive_emotion",
    "economic_stress_total",
    "isolation_total",
    "domestic_stress_total",
    "substance_use_total",
    "suicidality_total"
]

# ---------------- Prediction Function ----------------
def predict_risk(input_data):
    # Ensure all features exist
    row = [float(input_data.get(f, 0)) for f in FEATURES]

    prediction = model.predict([row])[0]
    confidence = model.predict_proba([row]).max()

    return prediction, round(confidence, 2)
