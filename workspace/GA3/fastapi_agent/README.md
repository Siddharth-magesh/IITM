Agent Task Runner
=================

This folder contains a minimal FastAPI app that accepts a task description and forwards it to a safe, local demo "copilot-cli" agent implementation which only supports computing small factorials.

How to run (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Then open:

http://localhost:8000/task?q=Write%20and%20run%20a%20program%20that%20prints%208%21%20as%20a%20single%20integer

The server will return JSON like:

{
  "task": "...",
  "agent": "copilot-cli",
  "output": "40320",
  "email": "22f3002579@ds.study.iitm.ac.in"
}
