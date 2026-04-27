import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest


# ---------------- SYSTEM ANOMALY DETECTION ---------------- #
def detect_system_anomalies(df):

    df = df.copy()

    # Select available features (include disk_io if present)
    feature_cols = ["cpu_usage", "api_latency", "error_rate"]

    if "disk_io" in df.columns:
        feature_cols.append("disk_io")

    # Handle missing values (safety)
    df[feature_cols] = df[feature_cols].ffill()

    features = df[feature_cols]

    # Isolation Forest model
    model = IsolationForest(contamination=0.1, random_state=42)

    # Predict anomalies
    df["anomaly"] = model.fit_predict(features)

    # Convert: normal = 0, anomaly = 1
    df["anomaly"] = df["anomaly"].map({1: 0, -1: 1})

    print("System anomalies detected:", df["anomaly"].sum())

    return df


# ---------------- TRANSACTION ANOMALY DETECTION ---------------- #
def detect_transaction_anomalies(df):

    df = df.copy()

    # Log transformation (stabilizes large values)
    df["log_amount"] = df["amount"].apply(
        lambda x: 0 if x <= 0 else np.log(x)
    )

    features = df[["log_amount"]]

    # Isolation Forest model
    model = IsolationForest(contamination=0.05, random_state=42)

    # Predict anomalies
    df["anomaly"] = model.fit_predict(features)

    # Convert: normal = 0, anomaly = 1
    df["anomaly"] = df["anomaly"].map({1: 0, -1: 1})

    print("Transaction anomalies detected:", df["anomaly"].sum())

    return df