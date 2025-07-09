from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "QR Code Generator Backend is running."}
