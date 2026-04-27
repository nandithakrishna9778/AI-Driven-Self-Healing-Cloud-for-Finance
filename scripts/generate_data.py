import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


# ---------------- SYSTEM DATA GENERATOR ---------------- #
class SystemDataGenerator:

    def __init__(self, num_records=3000):
        self.num_records = num_records

    def generate(self):
        data = []

        # Use current time as reference
        current_time = datetime.now()

        for i in range(self.num_records):

            # Generate timestamp (past → present)
            timestamp = current_time - timedelta(minutes=self.num_records - i)

            # -------- NORMAL VALUES -------- #
            cpu_usage = np.random.randint(40, 85)
            api_latency = np.random.randint(100, 600)
            error_rate = np.random.uniform(0, 20)

            # New: disk usage
            disk_io = np.random.randint(100, 500)

            # -------- ADD ANOMALIES -------- #
            if np.random.rand() < 0.1:
                cpu_usage = np.random.randint(90, 100)

            if np.random.rand() < 0.08:
                api_latency = np.random.randint(400, 600)

            if np.random.rand() < 0.05:
                error_rate = np.random.uniform(10, 20)

            if np.random.rand() < 0.07:
                disk_io = np.random.randint(350, 500)

            # Store record
            data.append([
                timestamp,
                cpu_usage,
                api_latency,
                error_rate,
                disk_io
            ])

        # Create DataFrame
        df = pd.DataFrame(data, columns=[
            "timestamp",
            "cpu_usage",
            "api_latency",
            "error_rate",
            "disk_io"
        ])

        return df


# ---------------- TRANSACTION DATA GENERATOR ---------------- #
class TransactionDataGenerator:

    def __init__(self, num_records=3000):
        self.num_records = num_records

    def generate(self):
        data = []

        current_time = datetime.now()

        for i in range(self.num_records):

            timestamp = current_time - timedelta(minutes=self.num_records - i)

            # Normal transaction
            amount = abs(np.random.normal(500, 200))
            amount = max(50, amount)

            transaction_type = np.random.choice(["credit", "debit"])

            is_anomaly = 0
            label = "normal"

            # Fraud case
            if np.random.rand() < 0.05:
                amount = np.random.choice([100000, 150000, 200000])
                is_anomaly = 1
                label = "fraud"

            data.append([
                timestamp,
                amount,
                transaction_type,
                label,
                is_anomaly
            ])

        df = pd.DataFrame(data, columns=[
            "timestamp",
            "amount",
            "type",
            "label",
            "is_anomaly"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
        return df


# ---------------- MAIN FUNCTION ---------------- #
def main():

    print("Generating fresh data...")

    os.makedirs("data", exist_ok=True)

    # Generate system data
    system_gen = SystemDataGenerator()
    system_df = system_gen.generate()
    system_df.to_csv("data/system_metrics.csv", index=False)

    # Generate transaction data
    transaction_gen = TransactionDataGenerator()
    transaction_df = transaction_gen.generate()
    transaction_df.to_csv("data/transactions.csv", index=False)

    print("Data updated at:", datetime.now())


# ---------------- RUN ---------------- #
if __name__ == "__main__":
    main()