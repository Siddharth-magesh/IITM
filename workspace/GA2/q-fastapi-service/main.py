from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import List, Dict, Any, Optional
import csv

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],expose_headers=["*"])


def load_students(csv_path: Path) -> List[Dict[str, Any]]:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    students: List[Dict[str, Any]] = []
    with csv_path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # Expecting columns: studentId,class (in that order), preserve order
        for row in reader:
            # normalize keys
            sid = row.get('studentId') or row.get('studentid') or row.get('id')
            cls = row.get('class') or row.get('Class')
            if sid is None or cls is None:
                # skip invalid rows
                continue
            try:
                sid_val = int(sid)
            except Exception:
                # keep original if cannot convert
                try:
                    sid_val = int(float(sid))
                except Exception:
                    sid_val = sid
            students.append({"studentId": sid_val, "class": cls})
    return students


CSV_PATH = Path(__file__).resolve().parent / "q-fastapi.csv"


@app.get("/api")
def get_students(class_: Optional[List[str]] = Query(None, alias="class")):
    """Return students from q-fastapi.csv. Use repeated ?class=1A&class=1B to filter."""
    try:
        students = load_students(CSV_PATH)
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

    if class_:
        # preserve CSV order while filtering
        allowed = set(class_)
        filtered = [s for s in students if s.get("class") in allowed]
        return {"students": filtered}
    return {"students": students}


if __name__ == "__main__":
    import uvicorn
    # Run the app object directly to avoid import-by-string issues
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
