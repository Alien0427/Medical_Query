import os
import json
import re
from google import genai
from google.genai import types

# Initialize the Google GenAI client. 
# Make sure to set the GEMINI_API_KEY environment variable before running.
# Example: export GEMINI_API_KEY="your-api-key-here" (Linux/Mac)
# Example: set GEMINI_API_KEY="your-api-key-here" (Windows CMD)
# Example: $env:GEMINI_API_KEY="your-api-key-here" (Windows PowerShell)
client = genai.Client()

def check_high_risk_symptoms(symptom_text: str):
    """
    Immediately checks the user's input for high-risk medical keywords using regular expressions.
    Returns a hardcoded critical alert dictionary if found, avoiding the LLM entirely.
    """
    # Define a predefined list of high-risk keywords
    high_risk_patterns = [
        r'\bchest\s+pain\b',
        r'\bshort(ness)?\s+of\s+breath\b',
        r'\bsevere\s+bleeding\b',
        r'\bheart\s+attack\b',
        r'\bcannot\s+breathe\b',
        r'\bstroke\b',
        r'\bunconscious\b',
        r'\bprofusely?\s+bleeding\b',
        r'\bsudden\s+numbness\b'
    ]
    
    # Combine patterns into a single regex and search (case-insensitive)
    combined_pattern = re.compile('|'.join(high_risk_patterns), re.IGNORECASE)
    
    if combined_pattern.search(symptom_text):
        return {
            "urgency_level": "CRITICAL",
            "possible_categories": ["Medical Emergency"],
            "disclaimer": "CRITICAL ALERT: Your symptoms suggest a potential life-threatening emergency. Please STOP using this tool and IMMEDIATELY call emergency services (e.g., 911) or your local emergency number."
        }
    
    return None

def analyze_symptoms(symptom_text: str) -> dict:
    """
    Sends symptom text to the Gemini LLM and parses the JSON triage response.
    """
    # Deterministic Safety Layer: Check for high-risk emergency terms first.
    critical_alert = check_high_risk_symptoms(symptom_text)
    if critical_alert:
        print(">> Triggered deterministic safety interceptor <<")
        return critical_alert

    system_prompt = """You are a preliminary medical triage assistant. You are strictly forbidden from providing medical diagnoses. Your only job is to analyze the described symptoms and output a JSON object with three fields:
"urgency_level" (Low, Medium, High),
"possible_categories" (a list of broad medical categories, NOT specific diseases), and
"disclaimer" (a mandatory string explicitly stating your uncertainty and advising the user to consult a doctor).
If the user inputs life-threatening symptoms, immediately set urgency to "CRITICAL" and recommend emergency services.

You must output absolutely nothing besides the raw JSON object. The JSON should match this exact structure:
{
    "urgency_level": "...",
    "possible_categories": ["...", "..."],
    "disclaimer": "..."
}"""

    try:
        # Using gemini-2.5-flash for fast and reliable JSON generation.
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Here are my symptoms: {symptom_text}",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                temperature=0.0 # Strict and deterministic output
            )
        )
        
        # Get the string content of the response
        result_content = response.text
        
        # Parse it into a Python dictionary
        triage_result = json.loads(result_content)
        
        return triage_result

    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON. Error: {e}")
        print(f"Raw output was: {response.text}")
        return None
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return None

if __name__ == "__main__":
    # Test cases to prove the prompt properly handles both minor and critical situations
    test_cases = [
        "I have a mild headache and a runny nose that lasted for 2 days now.",
        "Suddenly my chest feels incredibly tight, I'm sweating profusely, and my left arm is completely numb.",
        "I have a weird rash on my leg, it's slightly itchy.",
        "I just fell and have severe bleeding from my leg. Please help."
    ]

    for i, user_input in enumerate(test_cases, 1):
        print(f"\n" + "="*50)
        print(f"Test case {i}: {user_input}")
        
        # NOTE: This will fail if GEMINI_API_KEY is not set. 
        result = analyze_symptoms(user_input)
        
        if result:
            print("\nParsed Triage Output:")
            print(json.dumps(result, indent=4))
        else:
            print("\nNo output or failed to parse.")
        print("="*50)
