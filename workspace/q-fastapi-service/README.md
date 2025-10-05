FastAPI service serving q-fastapi.csv

Run locally (Git Bash):

1. Install deps in a venv:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

2. Place `q-fastapi.csv` next to `main.py` (same folder).

3. Run the app:

uvicorn main:app --reload --host 127.0.0.1 --port 8000

API endpoint:
- GET /api  -> returns all students
- GET /api?class=1A -> returns students in class 1A
- GET /api?class=1A&class=1B -> returns students in classes 1A or 1B

Response format:
{
  "students": [ {"studentId": 1, "class": "1A"}, ... ]
}
