import sys
import os

# Allow importing triage_backend from the project root
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from triage_backend import analyze_symptoms

app = FastAPI(title="Medical Triage API")

# Allow CORS so the frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SymptomRequest(BaseModel):
    symptoms: str
    duration: str = None

@app.post("/api/triage")
def triage_endpoint(request: SymptomRequest):
    if not request.symptoms or not request.symptoms.strip():
        raise HTTPException(status_code=400, detail="Symptoms text cannot be empty.")

    # Call the core triage logic
    result = analyze_symptoms(request.symptoms)

    if result is None:
        raise HTTPException(status_code=500, detail="Error communicating with LLM or parsing response.")

    return result
