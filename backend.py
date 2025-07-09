from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get MONGO_URI from environment
MONGO_URI = os.getenv("MONGO_URI")


# MongoDB setup
client = MongoClient(MONGO_URI)
db = client["qrdb"]  # Database name
collection = db["shorturls"]  # Collection name

# FastAPI app
app = FastAPI()

# Pydantic model for creating short URLs
class ShortURLRequest(BaseModel):
    short_code: str
    original_url: str

@app.get("/")
def home():
    return {"message": "Smart QR Redirect Server Running"}

@app.post("/api/create")
def create_short_url(request: ShortURLRequest):
    # Check if short code already exists
    if collection.find_one({"short_code": request.short_code}):
        raise HTTPException(status_code=400, detail="Short code already exists.")

    # Insert the new short code mapping
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

    # Increment scan count
    collection.update_one(
        {"short_code": short_code},
        {"$inc": {"scan_count": 1}}
    )

    return RedirectResponse(url=doc["original_url"])

@app.get("/api/data")
def get_all_data():
    data = {}
    for doc in collection.find():
        code = doc["short_code"]
        data[code] = {
            "original_url": doc["original_url"],
            "scan_count": doc["scan_count"]
        }
    return data
