from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
def home():
    return {"message": "QR Code Generator Backend is running."}

@app.get("/api/echo")
def echo_url(url: str = Query(..., description="The original URL to echo")):
    return {"original_url": url}
