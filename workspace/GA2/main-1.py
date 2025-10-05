from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import Dict, Any, List
import numpy as np
import json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], expose_headers=["*"])


def load_bundle() -> List[Dict[str, Any]]:
    p = Path(__file__).resolve().parent / "q-vercel-latency.json"
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def compute_metrics(records: List[Dict[str, Any]], threshold_ms: float) -> Dict[str, Dict[str, Any]]:
    by_region = {}
    for r in records:
        reg = r.get("region")
        if not reg:
            continue
        lat = r.get("latency_ms", r.get("latency"))
        if lat is None:
            continue
        if r.get("uptime") is not None:
            try:
                up_raw = float(r.get("uptime"))
            except Exception:
                continue
            up = up_raw * 100.0 if up_raw <= 1.0 else up_raw
        elif r.get("uptime_pct") is not None:
            try:
                up = float(r.get("uptime_pct"))
            except Exception:
                continue
        else:
            continue
        by_region.setdefault(reg, {"latencies": [], "uptimes": []})
        by_region[reg]["latencies"].append(float(lat))
        by_region[reg]["uptimes"].append(float(up))

    out = {}
    for reg, d in by_region.items():
        l = np.array(d["latencies"], dtype=float)
        u = np.array(d["uptimes"], dtype=float)
        if l.size == 0:
            continue
        out[reg] = {
            "avg_latency": round(float(np.mean(l)), 2),
            "p95_latency": round(float(np.percentile(l, 95)), 2),
            "avg_uptime": round(float(np.mean(u)), 3),
            "breaches": int((l > threshold_ms).sum()),
        }
    return out


@app.post("/")
@app.post("/latency")
async def latency_endpoint(payload: Dict[str, Any]):
    regions = payload.get("regions")
    threshold_ms = payload.get("threshold_ms")
    if not regions or threshold_ms is None:
        raise HTTPException(status_code=400, detail="Missing required fields: regions and threshold_ms")

    records = payload.get("records")
    if records is None:
        records = load_bundle()

    metrics = compute_metrics(records, float(threshold_ms))
    result = {r: metrics.get(r, {"avg_latency": None, "p95_latency": None, "avg_uptime": None, "breaches": 0}) for r in regions}
    return {"regions": result}
