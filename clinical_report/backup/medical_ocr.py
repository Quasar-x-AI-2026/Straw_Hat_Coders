import google.generativeai as genai
import sqlite3
import json
from PIL import Image

# ==========================================
# SETUP: API Key Yahan Dalein
# ==========================================
API_KEY = "AIzaSyBNlpoPDE0gSVMdXL5ZDfQ1c2mNdx3pF-M" 
genai.configure(api_key=API_KEY)

print("Available Models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f" - {m.name}")

# Database ka naam
DB_NAME = "hospital_data.db"

# ==========================================
# STEP 0: Database Banana (Sirf ek baar banega)
# ==========================================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Hum table bana rahe hain columns ke saath
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age TEXT,
            diagnosis TEXT,
            medicines TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database ready.")

# ==========================================
# STEP 1: Gemini se Data EXTRACT karna
# ==========================================
def extract_data_from_image(image_path):
    print(f"🔍 Reading image: {image_path}...")
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        img = Image.open(image_path)

        # Hum Gemini ko strictly bol rahe hain ki JSON hi wapas kare
        prompt = """
        give all details of the image or pdf in json format. 

        """

        response = model.generate_content([prompt, img])
        
        # Safayi: Agar Gemini ne ```json laga diya to usse hatana
        cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
        
        # Text ko Python Dictionary (JSON) mein convert karna
        data_json = json.loads(cleaned_text)
        
        print("✅ Extraction Successful!")
        print(f"   Data Found: {data_json}")
        return data_json

    except Exception as e:
        print(f"❌ Error in Extraction: {e}")
        return None

# ==========================================
# STEP 2: Data ko Database mein INSERT karna
# ==========================================
def save_to_database(data):
    if not data:
        print("⚠️ No data to save.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO patients (name, age, diagnosis, medicines, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('name'), 
            data.get('age'), 
            data.get('diagnosis'), 
            data.get('medicines'), 
            data.get('date')
        ))
        conn.commit()
        print("💾 Data Saved to Database Successfully!")
    except Exception as e:
        print(f"❌ Database Error: {e}")
    finally:
        conn.close()

# ==========================================
# MAIN EXECUTION (Code yahan se shuru hoga)
# ==========================================
if __name__ == "__main__":
    # 1. Pehle Database setup karo
    init_db()

    # 2. Image ka naam batayein (Ye image aapke folder mein honi chahiye)
    image_file = "download.jpg"  # <--- Yahan apni image ka naam likhein

    # 3. Process shuru
    import os
    if os.path.exists(image_file):
        # Step 1: Extract
        extracted_data = extract_data_from_image(image_file)
        
        # Step 2: Save
        save_to_database(extracted_data)
    else:
        print(f"❌ File '{image_file}' nahi mili! Please image ko folder mein rakhein.")