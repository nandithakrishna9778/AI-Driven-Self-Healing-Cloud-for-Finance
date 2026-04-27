# AI Self-Healing System

## Overview

This project is an AI-based self-healing system that detects anomalies in system performance and transactions, and automatically performs corrective actions.


## Features

* Anomaly detection using Isolation Forest (Machine Learning)
* Automatic self-healing (CPU, latency, error rate correction)
* Transaction fraud detection
* Real-time monitoring dashboard using Streamlit
* Logging of system issues and recovery actions



## Technologies Used

* Python
* Pandas, NumPy
* Scikit-learn
* Streamlit
* Matplotlib



## How It Works

1. System and transaction data are generated
2. Machine learning model detects anomalies
3. If anomalies are found, self-healing actions are applied
4. Results are logged and displayed in dashboard


## Project Structure

* `main.py` → Main controller (runs full system)
* `generate_data.py` → Generates system & transaction data
* `anomaly.py` → Detects anomalies using ML
* `app.py` → Streamlit dashboard
* `data/` → Stores generated data
* `logs/` → Stores system logs


How to Run

### Step 1: Clone repository

```bash
git clone <your-repo-link>
cd <your-project-folder>
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run main system

```bash
python main.py
```

### Step 4: Run dashboard

```bash
streamlit run app.py
```
Output

* Detects system anomalies (CPU, latency, errors, disk usage)
* Detects suspicious transactions
* Automatically applies fixes
* Displays results in interactive dashboard

Limitations

* Uses synthetic data (not real-time production data)
* Model parameters may require tuning for real-world scenarios


Future Improvements

* Real-time data streaming
* Advanced anomaly detection models
* Alert system (Email/SMS notifications)


Conclusion

This project demonstrates how AI can be used not only to detect system issues but also to automatically resolve them, improving reliability and reducing manual intervention.

Author
Nanditha Krishna EM