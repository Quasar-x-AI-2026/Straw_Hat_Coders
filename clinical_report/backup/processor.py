import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def analyze_medical_report(image_content):
    """
    Image content (bytes) leta hai aur Structured JSON return karta hai.
    """
    print("🔄 Sending to Gemini for OCR & Analysis...")
    
    model = genai.GenerativeModel('gemini-2.5-flash')

    # Prompt Engineering: The most critical part
    prompt = """
    You are a strictly accurate Medical Data Extractor.
    Analyze this clinical report image. Extract data into a strictly valid JSON format.
    
    1. EXTRACT METADATA:
       - patient_name (String, or "Unknown")
       - report_date (YYYY-MM-DD format, or "Unknown")
       - lab_name (String, or "Unknown")

    2. EXTRACT TEST RESULTS (Array of objects). For each test parameter found:
       - category: (e.g., "Hematology", "Lipid Profile", "Liver Function")
       - test_name: (Standardized name, e.g., use "Hemoglobin" instead of "Hb")
       - original_result: (The exact string seen on paper)
       - numeric_value: (Extract ONLY the number. If "Positive"/"Reactive" -> 1.0. If "Negative"/"Non-reactive" -> 0.0. If null -> null)
       - unit: (The unit of measurement, e.g., "mg/dL", "%")
       - reference_range: (The normal range string, e.g., "12-16")
       - status: (Enum: "Normal", "Abnormal", "High", "Low", "Positive", "Negative")

    OUTPUT FORMAT:
    {
      "metadata": { ... },
      "results": [ ... ]
    }
    
    IMPORTANT: Do not include markdown formatting like ```json. Just raw JSON string.
    """

    try:
        # Streamlit uploads are bytes, verify format
        response = model.generate_content([
            {'mime_type': 'image/jpeg', 'data': image_content}, 
            prompt
        ])
        
        # Cleaning the response
        raw_text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw_text)
        return data

    except Exception as e:
        print(f"❌ Error in processing: {e}")
        return None

def get_ai_insights(patient_history_text, user_query):
    """
    User ke specific sawal ka jawab dene ke liye.
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"""
    Based on the following patient medical history:
    {patient_history_text}
    
    Answer this user query accurately and concisely: "{user_query}"
    If the value is critical, mention it.
    """
    response = model.generate_content(prompt)
    return response.text