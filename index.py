from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from typing import List, Dict, Any
from pathlib import Path
import json
import logging


app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
	expose_headers=["*"]
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("iitm-latency")


def compute_metrics(records: List[Dict[str, Any]], threshold_ms: float):
	by_region = {}
	for r in records:
		region = r.get('region')
		if region is None:
			continue
		latency = r.get('latency_ms')
		uptime = r.get('uptime')
		if latency is None or uptime is None:
			continue
		by_region.setdefault(region, {'latencies': [], 'uptimes': []})
		by_region[region]['latencies'].append(float(latency))
		by_region[region]['uptimes'].append(float(uptime))

	out = {}
	for region, data in by_region.items():
		lats = np.array(data['latencies'], dtype=float)
		ups = np.array(data['uptimes'], dtype=float)
		if lats.size == 0:
			continue
		avg_latency = float(np.mean(lats))
		p95_latency = float(np.percentile(lats, 95))
		avg_uptime = float(np.mean(ups))
		breaches = int(np.sum(lats > threshold_ms))
		out[region] = {
			'avg_latency': round(avg_latency, 3),
			'p95_latency': round(p95_latency, 3),
			'avg_uptime': round(avg_uptime, 6),
			'breaches': breaches,
		}
		logger.info(f"Computed for region={region}: {out[region]}")
	return out


@app.get('/')
def read_root():
	return {"message": "Hello, World!"}


@app.post('/latency')
async def latency_endpoint(payload: Dict[str, Any], request: Request):
	regions = payload.get('regions')
	threshold_ms = payload.get('threshold_ms')
	records = payload.get('records')

	logger.info(f"Received payload regions={regions} threshold_ms={threshold_ms} records_included={bool(records)}")

	if records is None:
		sample = Path(__file__).resolve().parent / 'workspace' / 'telemetry.json'
		if sample.exists():
			try:
				with open(sample, 'r', encoding='utf-8') as f:
					records = json.load(f)
			except Exception:
				records = None
		if not records:
			records = [
				{'region': 'emea', 'latency_ms': 120, 'uptime': 0.999},
				{'region': 'emea', 'latency_ms': 200, 'uptime': 0.995},
				{'region': 'emea', 'latency_ms': 95, 'uptime': 0.9999},
				{'region': 'amer', 'latency_ms': 150, 'uptime': 0.9995},
				{'region': 'amer', 'latency_ms': 180, 'uptime': 0.998},
				{'region': 'amer', 'latency_ms': 300, 'uptime': 0.99},
			]
			logger.info(f"Using embedded sample records (count={len(records)})")

	if not regions or threshold_ms is None:
		raise HTTPException(status_code=400, detail='Missing required fields: regions and threshold_ms')

	metrics = compute_metrics(records, float(threshold_ms))
	result = {}
	for region in regions:
		if region in metrics:
			result[region] = metrics[region]
		else:
			result[region] = {'avg_latency': None, 'p95_latency': None, 'avg_uptime': None, 'breaches': 0}

	return result

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)