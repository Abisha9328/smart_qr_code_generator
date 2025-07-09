rom fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from qr_utils import load_data, save_data

app = FastAPI()

@app.get("/r/{short_code}")
def redirect(short_code: str):
    data = load_data()
    if short_code not in data:
        raise HTTPException(status_code=404, detail="Short URL not found.")

    # Increment scan count
    data[short_code]["scan_count"] += 1
    save_data(data)

    # Redirect to original URL
    return RedirectResponse(url=data[short_code]["original_url"])

@app.get("/")
def home():
    return {"message": "Smart QR Redirect Server Running"}
