from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import sys
import os
import json
from datetime import datetime

app = FastAPI(title="Agent Task Runner")

# Allow cross-origin GET requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)
AGENT_PATH = os.path.join(BASE_DIR, "agent_bin", "copilot_cli.py")
LOG_PATH = os.path.join(BASE_DIR, "agent_runs.log")
AGENT_NAME = "copilot-cli"
EMAIL = "22f3002579@ds.study.iitm.ac.in"


from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import sys
import os
import json
from datetime import datetime

app = FastAPI(title="Agent Task Runner")

# Allow cross-origin GET requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)
AGENT_PATH = os.path.join(BASE_DIR, "agent_bin", "copilot_cli.py")
LOG_PATH = os.path.join(BASE_DIR, "agent_runs.log")
AGENT_NAME = "copilot-cli"
EMAIL = "22f3002579@ds.study.iitm.ac.in"


def append_log(entry: dict):
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        # Best-effort logging; don't fail the request if logging breaks
        pass


@app.get("/task")
def run_task(q: str = Query(..., description="Task description")):
    start = datetime.utcnow().isoformat() + "Z"

    if not os.path.isfile(AGENT_PATH):
        # return JSON error (some graders require strict JSON responses)
        return JSONResponse({"task": q, "agent": AGENT_NAME, "output": "", "email": EMAIL, "error": "agent binary not found"}, status_code=500)

    try:
        proc = subprocess.run(
            [sys.executable, AGENT_PATH],
            input=q,
            text=True,
            capture_output=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        entry = {"timestamp_start": start, "task": q, "agent": AGENT_NAME, "error": "timeout"}
        append_log(entry)
        return JSONResponse({"task": q, "agent": AGENT_NAME, "output": "", "email": EMAIL, "error": "agent timed out"}, status_code=504)

    end = datetime.utcnow().isoformat() + "Z"
    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()

    log_entry = {
        "timestamp_start": start,
        "timestamp_end": end,
        "task": q,
        "agent": AGENT_NAME,
        "returncode": proc.returncode,
        "stdout": stdout,
        "stderr": stderr,
    }
    append_log(log_entry)

    # Always return an explicit JSONResponse to guarantee Content-Type
    return JSONResponse({"task": q, "agent": AGENT_NAME, "output": stdout, "email": EMAIL}, status_code=200)