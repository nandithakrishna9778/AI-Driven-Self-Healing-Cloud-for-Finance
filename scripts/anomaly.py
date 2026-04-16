import pandas as pd
from sklearn.ensemble import IsolationForest
def detect_system_anomalies(df):
    features = df[[
        "cpu_usage",
        "memory_usage",
        "api_latency",
        "transaction_count",
        "error_rate"
    ]]

    model = IsolationForest(contamination=0.05, random_state=42)
    df["anomaly"] = model.fit_predict(features)

    df["anomaly"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)

    return df


# ---------------- TRANSACTION ANOMALY ---------------- #
def detect_transaction_anomalies(df):

    features = df[["amount"]]

    model = IsolationForest(contamination=0.05, random_state=42)
    df["anomaly"] = model.fit_predict(features)

    df["anomaly"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)

    return df