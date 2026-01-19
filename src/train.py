import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

BASE_DIR = os.path.dirname(__file__)

DATA_PATH = os.path.join(BASE_DIR, "../data/bipolar_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "../models/model.pkl")

# Load dataset safely
df = pd.read_csv(
    DATA_PATH,
    sep=";",
    encoding="latin1",
    low_memory=False
)

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

# Keep only required columns
df = df[FEATURES]

# 🔑 CRITICAL FIX: convert European scientific notation to float
for col in FEATURES:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Replace NaN after conversion
df = df.fillna(0)

# Create target variable
conditions = [
    df["suicidality_total"] >= 2,
    (df["liwc_anxiety"] + df["liwc_sadness"]) >= 3
]
choices = ["high", "medium"]
df["risk_level"] = np.select(conditions, choices, default="low")

X = df[FEATURES]
y = df["risk_level"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

# Train
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, MODEL_PATH)
print("✅ Model trained and saved successfully")
