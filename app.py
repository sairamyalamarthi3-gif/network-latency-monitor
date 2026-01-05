import streamlit as st
import subprocess
import platform
import time
import pandas as pd

st.set_page_config(page_title="Real-Time Network Monitor", layout="wide")
st.title("📡 Real-Time Network Latency & Packet Loss Monitor")

# User inputs
target = st.text_input("Enter IP or Hostname to Monitor", "8.8.8.8")
interval = st.slider("Ping Interval (seconds)", 1, 12, 2)

placeholder = st.empty()
latency_list = []
packet_loss_list = []
timestamps = []

def ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    result = subprocess.run(command, capture_output=True, text=True)

    output = result.stdout.lower()

    if "unreachable" in output or "timed out" in output:
        return None

    for line in output.split("\n"):
        if "time=" in line:
            try:
                latency = float(line.split("time=")[1].split("ms")[0])
                return latency
            except:
                return None
    return None

# Real-time loop
for _ in range(200):
    latency = ping(target)
    timestamps.append(time.strftime("%H:%M:%S"))

    if latency is None:
        latency_list.append(None)
        packet_loss_list.append(100)
    else:
        latency_list.append(latency)
        packet_loss_list.append(0)

    df = pd.DataFrame({
        "Time": timestamps,
        "Latency (ms)": latency_list,
        "Packet Loss (%)": packet_loss_list
    })

    with placeholder.container():
        st.subheader(f"Monitoring: {target}")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Latest Latency (ms)", latency if latency else "Timeout")
        with col2:
            st.metric("Latest Packet Loss (%)", 0 if latency else 100)

        st.line_chart(df.set_index("Time")[["Latency (ms)"]])
        st.line_chart(df.set_index("Time")[["Packet Loss (%)"]])

    time.sleep(interval)
