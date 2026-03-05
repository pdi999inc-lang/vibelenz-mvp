from fastapi import FastAPI
from pydantic import BaseModel

from engine.safety_detector import SafetyDetector

app = FastAPI(title="VibeLenz API")

detector = SafetyDetector()

class Message(BaseModel):
    text: str

@app.get("/")
def home():
    return {"service": "VibeLenz Safety API", "status": "running"}

@app.post("/analyze")
def analyze(msg: Message):
    result = detector.analyze(msg.text)
    return {"analysis": result}
