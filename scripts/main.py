import pandas as pd
from anomaly import detect_system_anomalies, detect_transaction_anomalies
from generate_data import SystemDataGenerator, TransactionDataGenerator
from datetime import datetime
import os


# ---------------- LOG FUNCTION ---------------- #
def log(message):
    with open("logs/log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {message}\n")


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
        print("\nSample system anomalies:")
        print(anomalies[[
            "timestamp", "cpu_usage", "api_latency", "error_rate"
        ]].head())

        log("System anomaly detected - restart simulated")
    else:
        print("System healthy")


# ---------------- FINANCE CHECK ---------------- #
def check_finance():

    df = pd.read_csv("data/transactions.csv")

    print("\n--- CURRENT TRANSACTIONS ---")
    print(df.head())

    df = detect_transaction_anomalies(df)

    anomalies = df[df["anomaly"] == 1]

    print(f"\nTotal anomalies detected: {len(anomalies)}")

    if not anomalies.empty:
        print("\nSample suspicious transactions:")
        print(anomalies[["timestamp", "amount"]].head())

        # Save suspicious transactions
        if not os.path.exists("data/suspicious_transactions.csv"):
            anomalies.to_csv("data/suspicious_transactions.csv", index=False)
        else:
            anomalies.to_csv("data/suspicious_transactions.csv", mode='a', header=False, index=False)

        log("Financial anomaly detected - stored for review")

        print("\nSuspicious transactions saved to file")

    else:
        print("Finance data clean")


# ---------------- MAIN ---------------- #
def main():
    print("\nRunning AI self-healing system...\n")

    # Step 1: Generate fresh data
    generate_data()

    # Step 2: Detect + Handle
    check_system()
    check_finance()

    print("\nRun completed\n")


if __name__ == "__main__":
    main()