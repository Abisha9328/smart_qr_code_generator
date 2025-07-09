from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from qr_utils import load_data, save_data
import logging

# Setup logging
logging.basicConfig(level=logging.WARNING)

app = FastAPI()

@app.get("/r/{short_code}")
def redirect(short_code: str):
    logging.warning(f"Received redirect request for code: {short_code}")
    
    data = load_data()
    logging.warning(f"Available short codes in data: {list(data.keys())}")

    if short_code not in data:
        logging.warning("Short code not found in data.")
        raise HTTPException(status_code=404, detail="Short URL not found.")

    # Increment scan count
    data[short_code]["scan_count"] += 1
    save_data(data)

    # Redirect to original URL
    logging.warning(f"Redirecting to: {data[short_code]['original_url']}")
    return RedirectResponse(url=data[short_code]["original_url"])

@app.get("/")
def home():
    return {"message": "Smart QR Redirect Server Running"}
