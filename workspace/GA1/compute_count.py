import json
import statistics
import sys
from pathlib import Path

# default JSON file next to this script; can pass path as first arg
path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("q-calculate-variance.json")

if not path.exists():
    print(f"Error: file not found: {path}")
    sys.exit(1)

with path.open("r", encoding="utf-8") as f:
    data = json.load(f)

if not isinstance(data, list) or not data:
    print("Error: expected a non-empty JSON array of numbers")
    sys.exit(1)

# statistics.variance uses sample variance (N-1 denominator)
var = statistics.variance(data)
print(f"{var:.2f}")