import streamlit as st
import pandas as pd
import time

from monitor_engine import http_latency, calculate_jitter
from alert_engine import send_email_alert, send_slack_alert, send_teams_alert
from storage_engine import save_to_csv, save_to_sqlite
from traceroute_engine import http_trace

st.set_page_config(page_title="Advanced Network Diagnostics", layout="wide")

st.title("📡 Advanced Network Diagnostics Dashboard")

hosts = st.text_area(
    "Enter URLs to monitor (one per line)",
    "https://google.com\nhttps://cloudflare.com\nhttps://bbc.co.uk"
).splitlines()

interval = st.slider("Ping Interval (seconds)", 1, 10, 2)

email_alerts = st.checkbox("Enable Email Alerts")
slack_alerts = st.checkbox("Enable Slack Alerts")
teams_alerts = st.checkbox("Enable Teams Alerts")

sender = st.text_input("Email Sender")
password = st.text_input("Email Password", type="password")
receiver = st.text_input("Email Receiver")

slack_webhook = st.text_input("Slack Webhook URL")
teams_webhook = st.text_input("Teams Webhook URL")

data = {host: {"latency": [], "jitter": [], "loss": [], "timestamps": []} for host in hosts}

placeholder = st.empty()

for _ in range(200):
    for host in hosts:
        latency = http_latency(host)
        timestamps = data[host]["timestamps"]
        timestamps.append(time.strftime("%H:%M:%S"))

        if latency is None:
            data[host]["latency"].append(None)
            data[host]["loss"].append(100)
            data[host]["jitter"].append(None)

            msg = f"ALERT: {host} is DOWN"
            if email_alerts:
                send_email_alert(sender, password, receiver, "Host Down", msg)
            if slack_alerts:
                send_slack_alert(slack_webhook, msg)
            if teams_alerts:
                send_teams_alert(teams_webhook, msg)

        else:
            data[host]["latency"].append(latency)
            data[host]["loss"].append(0)
            jitter = calculate_jitter(data[host]["latency"])
            data[host]["jitter"].append(jitter)

    with placeholder.container():
        for host in hosts:
            st.subheader(f"Monitoring: {host}")

            df = pd.DataFrame({
                "Time": data[host]["timestamps"],
                "Latency (ms)": data[host]["latency"],
                "Packet Loss (%)": data[host]["loss"],
                "Jitter (ms)": data[host]["jitter"]
            }).set_index("Time")

            st.line_chart(df[["Latency (ms)"]])
            st.line_chart(df[["Packet Loss (%)"]])
            st.line_chart(df[["Jitter (ms)"]])

    time.sleep(interval)
