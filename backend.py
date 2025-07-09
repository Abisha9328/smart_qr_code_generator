from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import json
import os

app = FastAPI()

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

class ShortURLRequest(BaseModel):
    short_code: str
    original_url: str

@app.get("/")
def home():
    return {"message": "Smart QR Redirect Server Running"}

@app.post("/api/create")
def create_short_url(request: ShortURLRequest):
    data = load_data()
    if request.short_code in data:
        raise HTTPException(status_code=400, detail="Short code already exists.")
    data[request.short_code] = {"original_url": request.original_url, "scan_count": 0}
    save_data(data)
    return {"message": "Short URL created successfully."}

@app.get("/r/{short_code}")
def redirect(short_code: str):
    data = load_data()
    if short_code not in data:
        raise HTTPException(status_code=404, detail="Short URL not found.")
    data[short_code]["scan_count"] += 1
    save_data(data)
    return RedirectResponse(url=data[short_code]["original_url"])

@app.get("/api/data")
def get_all_data():
    return load_data()
