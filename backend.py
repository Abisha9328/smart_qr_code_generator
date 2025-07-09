from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os

# Load .env file if present
load_dotenv()

# Get MONGO_URI from environment variable
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set. Please set it in your .env or Render Environment Variables.")

# MongoDB setup
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Force connection test on startup
    client.server_info()
except errors.ServerSelectionTimeoutError:
    raise RuntimeError("Could not connect to MongoDB. Check your MONGO_URI and network settings.")

db = client["qrdb"]
collection = db["shorturls"]

app = FastAPI()

# Pydantic model for POST requests
class ShortURLRequest(BaseModel):
    short_code: str
    original_url: str

@app.get("/")
def home():
    return {"message": "Smart QR Redirect Server Running"}

@app.post("/api/create")
def create_short_url(request: ShortURLRequest):
    if collection.find_one({"short_code": request.short_code}):
        raise HTTPException(status_code=400, detail="Short code already exists.")

    collection.insert_one({
        "short_code": request.short_code,
        "original_url": request.original_url,
        "scan_count": 0
    })
    return {"message": "Short URL created successfully."}

@app.get("/r/{short_code}")
def redirect(short_code: str):
    doc = collection.find_one({"short_code": short_code})
    if not doc:
        raise HTTPException(status_code=404, detail="Short URL not found.")

    collection.update_one(
        {"short_code": short_code},
        {"$inc": {"scan_count": 1}}
    )
    return RedirectResponse(url=doc["original_url"])

@app.get("/api/data")
def get_all_data():
    data = {}
    try:
        for doc in collection.find():
            code = doc.get("short_code")
            if not code:
                continue
            data[code] = {
                "original_url": doc.get("original_url", ""),
                "scan_count": doc.get("scan_count", 0)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return data
