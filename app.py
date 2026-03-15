from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from triage_backend import analyze_symptoms

app = FastAPI(title="Triage AI API")

# Allow CORS so your frontend index.html can call this API
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
    
    # Call the logic defined in your triage_backend.py
    result = analyze_symptoms(request.symptoms)
    
    if result is None:
        raise HTTPException(status_code=500, detail="Error communicating with LLM or parsing response.")
        
    return result
