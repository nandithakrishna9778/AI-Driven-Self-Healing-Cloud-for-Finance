import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# ---------------- AUTO REFRESH ---------------- #
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=60000, key="refresh")  # 60 sec

st.set_page_config(page_title="AI Self-Healing System", layout="wide")

st.title("AI Self-Healing System Dashboard")


# ---------------- LOAD TRANSACTION DATA ---------------- #
try:
    transaction_df = pd.read_csv("data/transactions.csv")
    transaction_df["timestamp"] = pd.to_datetime(transaction_df["timestamp"])

    last_timestamp = str(transaction_df["timestamp"].iloc[-1])
    anomaly_count = int(transaction_df["is_anomaly"].sum())

except:
    transaction_df = pd.DataFrame()
    last_timestamp = "N/A"
    anomaly_count = "N/A"


# ---------------- LOAD SYSTEM DATA ---------------- #
try:
    system_df = pd.read_csv("data/system_metrics.csv")
    system_df["timestamp"] = pd.to_datetime(system_df["timestamp"])
except:
    system_df = pd.DataFrame()


# ---------------- ADD ANOMALY + HEALING ---------------- #
if not system_df.empty:

    # SAME LOGIC (unchanged)
    system_df["anomaly"] = system_df["cpu_usage"] > 90

    system_df["healed_cpu"] = system_df["cpu_usage"].apply(
        lambda x: x if x < 90 else 70
    )

    # NEW (safe add only)
    if "disk_io" in system_df.columns:
        system_df["healed_disk"] = system_df["disk_io"].apply(
            lambda x: x if x < 300 else 200
        )

else:
    system_df["anomaly"] = []
    system_df["healed_cpu"] = []


# ---------------- LIVE STATUS ---------------- #
st.subheader("Live Data Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Last Data Timestamp", last_timestamp)

with col2:
    st.metric("Transaction Anomalies", anomaly_count)

try:
    file_time = datetime.fromtimestamp(
        os.path.getmtime("data/system_metrics.csv")
    ).strftime("%Y-%m-%d %H:%M:%S")
except:
    file_time = "N/A"

with col3:
    st.metric("Data Last Updated", file_time)

with col4:
    st.metric("Dashboard Refresh Time", datetime.now().strftime("%H:%M:%S"))


# ---------------- SYSTEM MONITORING ---------------- #
st.subheader("System Monitoring")

if not system_df.empty:

    st.write("Total Records:", len(system_df))
    st.write("System Anomalies:", int(system_df["anomaly"].sum()))

    plot_df = system_df.tail(200)

    # ---------------- CPU GRAPH ---------------- #
    st.subheader("CPU Usage (Before vs After Self-Healing)")

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(plot_df["timestamp"], plot_df["cpu_usage"], label="Before", alpha=0.6)
    ax.plot(plot_df["timestamp"], plot_df["healed_cpu"], label="After (Healed)", linestyle="--")

    anomalies = plot_df[plot_df["anomaly"] == True]

    ax.scatter(
        anomalies["timestamp"],
        anomalies["cpu_usage"],
        color="red",
        s=20,
        label="Anomaly"
    )

    ax.set_xlabel("Time")
    ax.set_ylabel("CPU Usage")
    ax.legend()
    plt.xticks(rotation=30)

    st.pyplot(fig)

    # ---------------- NEW DISK GRAPH (ADDED ONLY) ---------------- #
    if "disk_io" in plot_df.columns:
        st.subheader("Disk Usage Monitoring")

        fig2, ax2 = plt.subplots(figsize=(10, 4))

        ax2.plot(plot_df["timestamp"], plot_df["disk_io"], label="Disk IO", alpha=0.6)

        if "healed_disk" in plot_df.columns:
            ax2.plot(plot_df["timestamp"], plot_df["healed_disk"], linestyle="--", label="Optimized")

        ax2.set_xlabel("Time")
        ax2.set_ylabel("Disk IO")
        ax2.legend()
        plt.xticks(rotation=30)

        st.pyplot(fig2)

    # ---------------- ALERT ---------------- #
    if len(anomalies) > 0:
        st.warning("Anomalies detected â Self-healing applied")
    else:
        st.success("System stable")

else:
    st.write("No system data available")


# ---------------- TRANSACTIONS ---------------- #
st.subheader("Suspicious Transactions")

try:
    suspicious_df = transaction_df[transaction_df["is_anomaly"] == 1]
    st.dataframe(suspicious_df.tail(10), use_container_width=True)
except:
    st.write("No suspicious data")


# ---------------- SELF HEALING ACTIONS ---------------- #
st.subheader("Self-Healing Actions")

try:
    healing_df = pd.read_csv("data/healing_log.csv")
    st.dataframe(healing_df.tail(10), use_container_width=True)
except:
    st.write("No healing actions yet")


# ---------------- DEBUG ---------------- #
st.subheader("Debug Info")

try:
    mod_time = datetime.fromtimestamp(
        os.path.getmtime("data/system_metrics.csv")
    ).strftime("%Y-%m-%d %H:%M:%S")

    st.write("Last data update:", mod_time)
except:
    st.write("File not found")