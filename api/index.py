from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import numpy as np

app = FastAPI()

# Allow CORS from any origin for POST requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)


class Query(BaseModel):
    regions: List[str]
    threshold_ms: float
    # Optional: telemetry records can be provided inline
    records: List[Dict[str, Any]] = None


def compute_metrics(records: List[Dict[str, Any]], threshold_ms: float):
    # records: list of {region: str, latency_ms: float, uptime: float}
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
    return out


@app.post("/latency")
async def latency_endpoint(q: Query, request: Request):
    # Determine records: prefer inline records in request body; else, try to find sample in repo
    records = q.records
    if records is None:
        # Attempt to load a sample telemetry bundle from workspace/telemetry.json if present
        import json
        from pathlib import Path
        sample = Path(__file__).resolve().parents[1] / 'workspace' / 'telemetry.json'
        if sample.exists():
            try:
                with open(sample, 'r', encoding='utf-8') as f:
                    records = json.load(f)
            except Exception:
                records = []
        else:
            # No records available
            raise HTTPException(status_code=400, detail='No telemetry records provided in request and no sample bundle available.')

    metrics = compute_metrics(records, q.threshold_ms)

    # Ensure requested regions are present in response (if a region had no data, return zeros)
    result = {}
    for region in q.regions:
        if region in metrics:
            result[region] = metrics[region]
        else:
            result[region] = {
                'avg_latency': None,
                'p95_latency': None,
                'avg_uptime': None,
                'breaches': 0,
            }

    return result


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
