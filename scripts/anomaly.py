import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_system_anomalies(df):

    feature_cols = ["cpu_usage", "api_latency", "error_rate"]

    features = df[feature_cols]

    model = IsolationForest(contamination=0.1, random_state=42)

    df["anomaly"] = model.fit_predict(features)
    df["anomaly"] = df["anomaly"].map({1: 0, -1: 1})

    print("System anomalies detected:", df["anomaly"].sum())

    return df


def detect_transaction_anomalies(df):

    df["log_amount"] = df["amount"].apply(lambda x: 0 if x <= 0 else np.log(x))

    features = df[["log_amount"]]

    model = IsolationForest(contamination=0.05, random_state=42)

    df["anomaly"] = model.fit_predict(features)
    df["anomaly"] = df["anomaly"].map({1: 0, -1: 1})

    print("Transaction anomalies detected:", df["anomaly"].sum())

    return df