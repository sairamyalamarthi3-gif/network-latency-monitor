import requests

def http_trace(url):
    try:
        response = requests.options(url)
        return response.headers
    except:
        return {"trace": "Not available"}
