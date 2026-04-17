import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


# ---------------- SYSTEM ANOMALY ---------------- #
def detect_system_anomalies(df):

    df = df.copy()

    # Feature Engineering
    df["cpu_latency_ratio"] = df["cpu_usage"] / (df["api_latency"] + 1)
    df["error_cpu_ratio"] = df["error_rate"] / (df["cpu_usage"] + 1)

    features = df[[
        "cpu_usage",
        "memory_usage",
        "api_latency",
        "transaction_count",
        "error_rate",
        "cpu_latency_ratio",
        "error_cpu_ratio"
    ]]

    # Scaling
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Model
    model = IsolationForest(
        contamination='auto',
        random_state=42
    )

    df["anomaly"] = model.fit_predict(features_scaled)

    # Convert (-1 → anomaly, 1 → normal)
    df["anomaly"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)

    # Severity Classification
    def classify_severity(row):
        if row["cpu_usage"] > 90 or row["error_rate"] > 8:
            return "HIGH"
        elif row["cpu_usage"] > 75:
            return "MEDIUM"
        else:
            return "LOW"

    df["severity"] = df.apply(classify_severity, axis=1)

    return df


# ---------------- TRANSACTION ANOMALY ---------------- #
def detect_transaction_anomalies(df):

    df = df.copy()

    # Feature Engineering
    df["log_amount"] = np.log1p(df["amount"])

    features = df[[
        "amount",
        "log_amount"
    ]]

    # Scaling
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Model
    model = IsolationForest(
        contamination='auto',
        random_state=42
    )

    df["anomaly"] = model.fit_predict(features_scaled)

    # Convert labels
    df["anomaly"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)

    return df
