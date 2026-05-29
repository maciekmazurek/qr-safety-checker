from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="qr-safety-checker-backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # W produkcji zmień na konkretny adres URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definiujemy, jakich danych oczekujemy od frontendu (bezpieczne sprawdzanie typów)
class UrlCheckRequest(BaseModel):
    url: HttpUrl

# Główny endpoint, do którego telefon będzie wysyłał odczytany link
@app.post("/api/check-url")
def check_url(payload: UrlCheckRequest):
    scanned_url = str(payload.url)
    
    if "malicious" in scanned_url or "test-danger" in scanned_url:
        return {"url": scanned_url, "status": "MALICIOUS", "message": "This URL is flagged as malicious."}
    
    return {"url": scanned_url, "status": "SAFE", "message": "This URL looks safe."}