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

    print("\nStarting self-healing process...")

    df = df.copy()
    actions = []

    if not anomalies.empty:

        # CPU healing
        if "cpu_usage" in anomalies.columns and anomalies["cpu_usage"].max() > 90:
            print(" High CPU detected → Reducing load")
            df["cpu_usage"] = df["cpu_usage"].astype(float)
            df.loc[df["cpu_usage"] > 90, "cpu_usage"] *= 0.6
            actions.append("CPU Load Balanced")

        # API latency healing
        if "api_latency" in anomalies.columns and anomalies["api_latency"].max() > 300:
            print("High latency detected → Restart simulation")
            df["api_latency"] = df["api_latency"].astype(float)
            df.loc[df["api_latency"] > 300, "api_latency"] *= 0.5
            actions.append("API Restarted")

        # Error rate healing
        if "error_rate" in anomalies.columns and anomalies["error_rate"].max() > 5:
            print("High error rate → Applying recovery")
            df["error_rate"] = df["error_rate"].astype(float)
            df.loc[df["error_rate"] > 5, "error_rate"] *= 0.4
            actions.append("System Recovered")

        # Disk IO healing (NEW but safe)
        if "disk_io" in df.columns:
            if "disk_io" in anomalies.columns and anomalies["disk_io"].max() > 300:
                print(" High disk usage → Optimizing IO")
                df["disk_io"] = df["disk_io"].astype(float)
                df.loc[df["disk_io"] > 300, "disk_io"] *= 0.7
                actions.append("Disk Optimized")

    # If no issues
    if not actions:
        actions = ["System Healthy"]

    final_action = ", ".join(actions)

    print(f" Action taken: {final_action}")
    log(f"Self-healing action: {final_action}")

    # ---------------- SAVE HEALING LOG ---------------- #
    healing_entry = pd.DataFrame([{
        "timestamp": datetime.now(),
        "issue": "System Anomaly",
        "action": final_action,
        "status": "Resolved" if final_action != "System Healthy" else "Healthy"
    }])

    log_path = "data/healing_log.csv"

    if os.path.exists(log_path):
        healing_entry.to_csv(log_path, mode='a', header=False, index=False)
    else:
        healing_entry.to_csv(log_path, index=False)

    # Save healed dataset
    df.to_csv("data/healed_system_metrics.csv", index=False)

    return df, final_action


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
        cols = ["timestamp", "cpu_usage", "api_latency", "error_rate"]

        if "disk_io" in df.columns:
            cols.append("disk_io")

        print(anomalies[cols].head())

        # Apply healing
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

    print("\nRunning AI Self-Healing System...\n")

    # Always generate fresh data
    generate_data()

    system_df, healed_df, action = check_system()
    transaction_df, txn_anomalies = check_finance()

    print("\nRun completed successfully\n")


# ---------------- RUN ---------------- #
if __name__ == "__main__":
    main()