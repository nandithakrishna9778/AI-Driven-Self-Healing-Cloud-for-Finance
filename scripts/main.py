
import pandas as pd
from anomaly import detect_system_anomalies, detect_transaction_anomalies
from generate_data import SystemDataGenerator, TransactionDataGenerator
from datetime import datetime
import os


# ---------------- ENSURE FOLDERS ---------------- #
os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)


# ---------------- LOG FUNCTION ---------------- #
def log(message):
    with open("logs/log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {message}\n")


# ---------------- SELF HEALING FUNCTION ---------------- #
def self_heal_system(df, anomalies):
    print("\n⚙️ Initiating self-healing actions...")

    df = df.copy()

    max_cpu = anomalies["cpu_usage"].max()
    max_latency = anomalies["api_latency"].max()
    max_error = anomalies["error_rate"].max()

    action = "System Healthy"

    if max_cpu > 90:
        print("High CPU → Scaling down load")
        df.loc[df["cpu_usage"] > 90, "cpu_usage"] *= 0.6
        action = "Load Balanced"

    if max_latency > 300:
        print("High latency → Restarting API")
        df.loc[df["api_latency"] > 300, "api_latency"] *= 0.5
        action = "API Restarted"

    if max_error > 5:
        print("High error → System recovery")
        df.loc[df["error_rate"] > 5, "error_rate"] *= 0.4
        action = "System Recovered"

    print(f"Action taken: {action}")
    log(f"Self-healing action: {action}")

    # Save healed dataset
    df.to_csv("data/healed_system_metrics.csv", index=False)

    return df, action


# ---------------- DATA GENERATION ---------------- #
def generate_data():
    print("Generating fresh data...")

    system_gen = SystemDataGenerator()
    system_df = system_gen.generate()
    system_df.to_csv("data/system_metrics.csv", index=False)

    transaction_gen = TransactionDataGenerator()
    transaction_df = transaction_gen.generate()
    transaction_df.to_csv("data/transactions.csv", index=False)


# ---------------- SYSTEM CHECK ---------------- #
def check_system():

    df = pd.read_csv("data/system_metrics.csv")
    df = detect_system_anomalies(df)

    anomalies = df[df["anomaly"] == 1]

    print(f"\nSystem anomalies detected: {len(anomalies)}")

    if not anomalies.empty:
        print("\nSample anomalies:")
        print(anomalies[[
            "timestamp", "cpu_usage", "api_latency", "error_rate", "severity"
        ]].head())

        print("\nSeverity breakdown:")
        print(anomalies["severity"].value_counts())

        # 🔥 SELF HEALING
        healed_df, action = self_heal_system(df, anomalies)

    else:
        print("System healthy")
        action = "No Action Needed"
        healed_df = df

    return df, healed_df, action


# ---------------- FINANCE CHECK ---------------- #
def check_finance():

    df = pd.read_csv("data/transactions.csv")

    df = detect_transaction_anomalies(df)

    anomalies = df[df["anomaly"] == 1]

    print(f"\nFinancial anomalies detected: {len(anomalies)}")

    if not anomalies.empty:
        anomalies.to_csv("data/suspicious_transactions.csv", index=False)
        log(f"Financial anomaly detected | Count: {len(anomalies)}")

    return df, anomalies


# ---------------- MAIN ---------------- #
def main():
    print("\nRunning AI self-healing system...\n")

    if not os.path.exists("data/system_metrics.csv"):
        generate_data()

    system_df, healed_df, action = check_system()
    transaction_df, txn_anomalies = check_finance()

    print("\nRun completed\n")


if __name__ == "__main__":
    main()

