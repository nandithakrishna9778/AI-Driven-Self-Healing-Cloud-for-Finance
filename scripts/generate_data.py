import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# ================= SYSTEM DATA GENERATOR ================= #
class SystemDataGenerator:

    def __init__(self, num_records=3000):
        self.num_records = num_records

    def get_time_load(self, hour):
        if 9 <= hour <= 12:
            return 1.2
        elif 12 <= hour <= 16:
            return 1.5
        elif 16 <= hour <= 20:
            return 1.3
        else:
            return 0.7

    def generate(self):

        data = []
        start_time = datetime.now()

        server_profiles = {
            "server_1": 40,
            "server_2": 50,
            "server_3": 60,
            "server_4": 45
        }

        for i in range(self.num_records):

            timestamp = start_time + timedelta(minutes=i)
            hour = timestamp.hour

            server_id = np.random.choice(list(server_profiles.keys()))

            base_cpu = server_profiles[server_id]
            load_factor = self.get_time_load(hour)

            transaction_count = int(np.random.randint(200, 500) * load_factor)

            cpu = base_cpu * load_factor + (transaction_count * 0.05)
            cpu = min(cpu, 100)

            memory = np.random.normal(60, 10)
            latency = 100 + (transaction_count * 0.3)
            error_rate = 1 + (cpu / 100) * 2

            is_anomaly = 0

            # Inject anomalies
            if np.random.rand() < 0.05:

                event = np.random.choice(["spike", "failure", "attack"])
                is_anomaly = 1

                if event == "spike":
                    transaction_count *= 2
                    cpu += 30
                    latency += 100

                elif event == "failure":
                    error_rate += 8
                    latency += 200

                elif event == "attack":
                    transaction_count *= 3
                    cpu += 40
                    error_rate += 5

            cpu = min(cpu, 100)

            data.append([
                timestamp,
                server_id,
                cpu,
                memory,
                latency,
                transaction_count,
                error_rate,
                "running",
                is_anomaly
            ])
            df = pd.DataFrame(data, columns=[
            "timestamp",
            "server_id",
            "cpu_usage",
            "memory_usage",
            "api_latency",
            "transaction_count",
            "error_rate",
            "system_status",
            "is_anomaly"
        ])

        return df


# ================= TRANSACTION DATA GENERATOR ================= #
class TransactionDataGenerator:

    def __init__(self, num_records=3000):
        self.num_records = num_records

    def generate(self):

        data = []
        start_time = datetime.now()

        for i in range(self.num_records):

            timestamp = start_time + timedelta(minutes=i)

            # Generate realistic positive transaction amount
            amount = abs(np.random.normal(500, 200))
            amount = max(50, amount)

            transaction_type = np.random.choice(["credit", "debit"])

            is_anomaly = 0

            # Inject anomalies
            if np.random.rand() < 0.05:
                amount = np.random.choice([80000, 100000, 150000])
                is_anomaly = 1

            data.append([
                timestamp,
                amount,
                transaction_type,
                is_anomaly
            ])
            df = pd.DataFrame(data, columns=[
            "timestamp",
            "amount",
            "type",
            "is_anomaly"
        ])

        return df


# ================= MAIN (OPTIONAL DIRECT RUN) ================= #
if __name__ == "__main__":

    print("Generating system data...")
    system_gen = SystemDataGenerator()
    system_df = system_gen.generate()
    system_df.to_csv("data/system_metrics.csv", index=False)

    print("Generating transaction data...")
    transaction_gen = TransactionDataGenerator()
    transaction_df = transaction_gen.generate()
    transaction_df.to_csv("data/transactions.csv", index=False)

    print("All datasets generated successfully!")