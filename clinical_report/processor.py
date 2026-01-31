import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def analyze_medical_report(image_content):
    print("Sending to Gemini...")
    prompt = """
    Extract data from this medical report into JSON.
    Keys: 
    1. metadata: {patient_name, report_date, lab_name}
    2. results: [{category, test_name, original_result, numeric_value (float/null), unit, reference_range, status}]
    Return ONLY JSON.
    """
    try:
        response = model.generate_content([{'mime_type': 'image/jpeg', 'data': image_content}, prompt])
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Error: {e}")
        return None

def generate_trend_analysis(parameter_name, trend_data_text):
    prompt = f"""
    Act as an AI Doctor. Analyze the trend for "{parameter_name}".
    Data: {trend_data_text}
    
    Output Format (Markdown):
    ### 🧐 Observation
    (Is it increasing/decreasing? Is it safe?)
    
    ### 🥗 Recommendations
    (Diet/Lifestyle tips)
    
    ### 💡 Suggestions
    (Next steps like re-testing)
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {e}"

def get_chat_response(medical_history, chat_history, user_question):
    try:
        # Build context from last 5 messages
        context_str = ""
        for msg in chat_history[-5:]:
            role = "User" if msg["role"] == "user" else "AI"
            context_str += f"{role}: {msg['content']}\n"

        prompt = f"""
        You are a medical assistant.
        Patient History: {medical_history}
        Chat Context: {context_str}
        User Question: {user_question}
        
        Answer professionally and concisely.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Chat Error: {e}"