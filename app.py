from ping3 import ping
import streamlit as st
import pandas as pd
import time

st.title("📡 Real-Time Network Latency Monitor")

target = st.text_input("Enter IP or Hostname", "8.8.8.8")
interval = st.slider("Ping Interval (seconds)", 1, 12, 2)

latency_list = []
packet_loss_list = []
timestamps = []
placeholder = st.empty()

def ping_host(host):
    try:
        latency = ping(host, timeout=1)
        if latency is None:
            return None
        return round(latency * 1000, 2)
    except:
        return None

for _ in range(200):
    latency = ping_host(target)
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
        st.metric("Latency (ms)", latency if latency else "Timeout")
        st.line_chart(df.set_index("Time")[["Latency (ms)"]])

    time.sleep(interval)
