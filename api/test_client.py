import requests
import json

URL = 'http://127.0.0.1:8000/latency'

sample_records = [
    {'region': 'emea', 'latency_ms': 120, 'uptime': 0.999},
    {'region': 'emea', 'latency_ms': 200, 'uptime': 0.995},
    {'region': 'amer', 'latency_ms': 150, 'uptime': 0.9995},
    {'region': 'amer', 'latency_ms': 180, 'uptime': 0.998},
    {'region': 'amer', 'latency_ms': 300, 'uptime': 0.99},
]

payload = {
    'regions': ['emea', 'amer'],
    'threshold_ms': 157,
    'records': sample_records,
}

resp = requests.post(URL, json=payload)
print('status', resp.status_code)
print(json.dumps(resp.json(), indent=2))
