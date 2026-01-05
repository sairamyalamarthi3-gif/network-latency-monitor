import requests
import time

def http_latency(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=2)
        end = time.time()

        if response.status_code == 200:
            return round((end - start) * 1000, 2)
        return None
    except:
        return None


def calculate_jitter(latency_list):
    if len(latency_list) < 2:
        return 0
    prev = latency_list[-2]
    curr = latency_list[-1]
    if prev is None or curr is None:
        return None
    return round(abs(curr - prev), 2)
