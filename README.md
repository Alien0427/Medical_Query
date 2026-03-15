# 🏥 Trustworthy Medical Triage AI

A full-stack AI-powered medical triage tool that analyzes user-described symptoms and returns a structured JSON assessment — with a built-in deterministic safety guardrail that bypasses the LLM entirely for life-threatening emergencies.

---

## 📁 Project Structure

```
medical_query/
├── index.html          # Frontend UI (form + dynamic results display)
├── style.css           # Clinical, responsive CSS design system
├── app.py              # FastAPI backend server (REST API)
├── triage_backend.py   # Core LLM integration + safety interceptor
├── test_api.py         # Python test suite (3 test scenarios)
├── requirements.txt    # Python dependencies
└── .gitignore
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Alien0427/Medical_Query.git
cd Medical_Query
```

### 2. Create & Activate a Virtual Environment
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Your Gemini API Key
```powershell
# Windows PowerShell
$env:GEMINI_API_KEY="your-gemini-api-key-here"

# Mac/Linux
export GEMINI_API_KEY="your-gemini-api-key-here"
```
> ⚠️ **Never hardcode your API key in source files.** Always use environment variables.

---

## ▶️ Running the Application

### Start the Backend API Server
```bash
uvicorn app:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### Open the Frontend
In a second terminal, serve the frontend:
```bash
python -m http.server 3000
```
Then open your browser and navigate to `http://localhost:3000`.

---

## 🧪 Running Tests

With the server running, open another terminal and execute:
```bash
python test_api.py
```

This runs three scenarios:
| Scenario | Input | Expected |
|----------|-------|----------|
| **A - Benign** | Mild headache for a few hours | `Low` urgency via LLM |
| **B - Complex** | Fever, chills, persistent cough for 4 days | `Medium/High` urgency via LLM |
| **C - Critical** | Severe chest pain and shortness of breath | `CRITICAL` — **LLM bypassed** by regex guardrail |

---

## 🛡️ Safety Architecture

```
User Input
    │
    ▼
┌─────────────────────────────┐
│  Deterministic Safety Layer │  ← Regex pattern matching (no LLM call)
│  (check_high_risk_symptoms) │    Returns CRITICAL instantly if triggered
└────────────┬────────────────┘
             │ (safe input only)
             ▼
┌─────────────────────────────┐
│      Gemini 2.5 Flash       │  ← Strict system prompt, JSON output mode
│  (analyze_symptoms via LLM) │
└─────────────────────────────┘
```

---

## ⚕️ Disclaimer

This tool is for **educational and demonstration purposes only**. It is **not a substitute for professional medical advice, diagnosis, or treatment**. Always consult a qualified healthcare provider.
