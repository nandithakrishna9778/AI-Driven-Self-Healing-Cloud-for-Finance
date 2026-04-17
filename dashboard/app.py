
import streamlit as st
import pandas as pd
import plotly.express as px
import os

from scripts.anomaly import detect_system_anomalies, detect_transaction_anomalies


st.set_page_config(page_title="AI Self-Healing System", layout="wide")

st.title("AI Self-Healing System Dashboard")


# ---------------- LOAD DATA ---------------- #
@st.cache_data
def load_system_data():
    return pd.read_csv("data/system_metrics.csv")

@st.cache_data
def load_healed_data():
    if os.path.exists("data/healed_system_metrics.csv"):
        return pd.read_csv("data/healed_system_metrics.csv")
    return None

@st.cache_data
def load_transaction_data():
    return pd.read_csv("data/transactions.csv")


# ---------------- SYSTEM SECTION ---------------- #
st.header("🖥 System Monitoring")

if os.path.exists("data/system_metrics.csv"):

    df = load_system_data()
    df = detect_system_anomalies(df)

    anomalies = df[df["anomaly"] == 1]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Anomalies", len(anomalies))

    # CPU Graph
    fig = px.line(df, x="timestamp", y="cpu_usage", title="CPU Usage")
    st.plotly_chart(fig, use_container_width=True)

    # 🔥 Self-healing comparison
    healed_df = load_healed_data()

    if healed_df is not None:
        st.subheader(" Self-Healing Effect")

        col1, col2 = st.columns(2)

        with col1:
            st.write("Before Healing")
            st.line_chart(df["cpu_usage"])

        with col2:
            st.write("After Healing")
            st.line_chart(healed_df["cpu_usage"])

        st.success("System auto-healed successfully")

else:
    st.warning("Run main.py first")


# ---------------- TRANSACTIONS ---------------- #
st.header(" Transaction Monitoring")

if os.path.exists("data/transactions.csv"):

    df_t = load_transaction_data()
    df_t = detect_transaction_anomalies(df_t)

    anomalies_t = df_t[df_t["anomaly"] == 1]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Transactions", len(df_t))
    with col2:
        st.metric("Fraud Detected", len(anomalies_t))

    fig2 = px.line(df_t, x="timestamp", y="amount", title="Transaction Amount")
    st.plotly_chart(fig2, use_container_width=True)

    if not anomalies_t.empty:
        st.subheader(" Suspicious Transactions")
        st.dataframe(anomalies_t.head(20))

else:
    st.warning("Run main.py first")
