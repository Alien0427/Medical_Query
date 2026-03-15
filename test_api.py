import requests
import json
import time

API_URL = "http://127.0.0.1:8000/api/triage"

def run_test(name, symptom_text):
    print(f"\n======================================")
    print(f"Running Test: {name}")
    print(f"Input: '{symptom_text}'")
    print(f"======================================")
    
    payload = {
        "symptoms": symptom_text,
        "duration": "Not specified"
    }
    
    try:
        start_time = time.time()
        response = requests.post(API_URL, json=payload)
        latency = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"Status: 200 OK (Latency: {latency:.2f}s)")
            print("Response JSON:")
            print(json.dumps(result, indent=4))
            
            # Highlight deterministic interceptor
            if result.get("urgency_level") == "CRITICAL" and latency < 0.5:
                print("\n[SUCCESS] CRITICAL urgency returned instantly (<0.5s), indicating the LLM was bypassed!")
        else:
            print(f"Error: Status code {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Connection refused. Is the FastAPI server running?")

if __name__ == "__main__":
    # Scenario A (Benign)
    run_test(
        name="Scenario A (Benign)",
        symptom_text="I have had a mild headache for a few hours."
    )
    
    # Scenario B (Complex)
    run_test(
        name="Scenario B (Complex)",
        symptom_text="I've had a fever, chills, and a persistent cough for 4 days."
    )
    
    # Scenario C (Critical Edge-Case)
    run_test(
        name="Scenario C (Critical Edge-Case)",
        symptom_text="I am experiencing severe chest pain and shortness of breath."
    )
