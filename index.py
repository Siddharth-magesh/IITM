from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import numpy as np
from pathlib import Path
import json
import logging
from typing import List, Dict, Any


app = Flask(__name__)
CORS(app, resources={r"/latency": {"origins": "*"}})

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
		logger.info(f"Computed for region={region}: avg_latency={out[region]['avg_latency']} p95={out[region]['p95_latency']} avg_uptime={out[region]['avg_uptime']} breaches={out[region]['breaches']}")
	return out


@app.route('/', methods=['GET'])
def read_root():
	return jsonify({'message': 'Hello, World!'})


@app.route('/latency', methods=['POST', 'OPTIONS'])
def latency_endpoint():
	if request.method == 'OPTIONS':
		resp = make_response('', 200)
		resp.headers['Access-Control-Allow-Origin'] = '*'
		resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
		resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
		return resp

	data = request.get_json(silent=True) or {}
	regions = data.get('regions')
	threshold_ms = data.get('threshold_ms')
	records = data.get('records')

	print('[latency_endpoint] Received request:')
	print('  regions:', regions)
	print('  threshold_ms:', threshold_ms)
	print('  records_included_in_request:', bool(records))

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
			print(f"[latency_endpoint] No records provided; using embedded sample records (count={len(records)})")

	try:
		print(f"[latency_endpoint] Using records count={len(records)}")
		preview = records[:5]
		print(f"[latency_endpoint] Records preview: {preview}")
	except Exception as e:
		print('[latency_endpoint] Could not print records preview:', e)

	if not regions or threshold_ms is None:
		return jsonify({'error': 'Missing required fields: regions and threshold_ms'}), 400

	metrics = compute_metrics(records, float(threshold_ms))
	result = {}
	for region in regions:
		if region in metrics:
			result[region] = metrics[region]
		else:
			result[region] = {'avg_latency': None, 'p95_latency': None, 'avg_uptime': None, 'breaches': 0}

	resp = jsonify(result)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)

