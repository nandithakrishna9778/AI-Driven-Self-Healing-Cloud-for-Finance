AI Self-Healing System Dashboard

Project Overview

This project is an AI-based system designed to monitor system performance metrics, detect anomalies, and simulate a self-healing mechanism. It uses machine learning techniques to identify unusual patterns in system behavior and visualizes the results using an interactive dashboard.

---

Features

- Real-time system monitoring (CPU, Memory, Disk I/O)
- Anomaly detection using machine learning
- Interactive dashboard using Streamlit
-  Simulated self-healing mechanism
- Modular project design

---

Installation & Setup

1. Create Virtual Environment

python -m venv venv

2. Activate Environment

venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

---

How to Run

Step 1: Generate Data

python scripts/generate_data.py

Step 2: Run Backend (Optional)

python scripts/main.py

Step 3: Launch Dashboard

python -m streamlit run dashboard/app.py

---

Dataset Information

- The dataset is synthetically generated
- Contains approximately 3000 records
- Includes:
  - Timestamp
  - CPU Usage
  - Memory Usage
  - Disk I/O

---

Anomaly Detection

- Detects unusual spikes and drops in system metrics
- Identifies abnormal system behavior
- Can be extended to real-world monitoring systems

---

Self-Healing Concept

- Detect anomalies
- Apply corrective logic (simulated)
- Generate a healed dataset

---

 Technologies Used

- Python
- Pandas
- Scikit-learn
- Streamlit
- Plotly

---

Use Cases

- System monitoring dashboards
- Predictive maintenance
- AI-based automation systems
- IT infrastructure health monitoring

---

Future Improvements

- Real-time data integration
- Alert system (email/SMS)
- Advanced anomaly detection models
- Cloud deployment

---

 Author

Nanditha Krishna EM