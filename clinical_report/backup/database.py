import sqlite3
import pandas as pd

DB_NAME = "clinical_db.sqlite"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    """Database tables create karega agar wo exist nahi karti."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Reports Table (Har upload ki summary)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            patient_name TEXT,
            report_date TEXT,
            lab_name TEXT
        )
    ''')

    # 2. Test Results Table (Deep Data: Har ek single test parameter)
    # is_abnormal: 1 if user needs attention, 0 if normal
    # value_numeric: Sirf number store karega graph ke liye (e.g., 12.5)
    # unit: Standard unit (e.g., g/dL)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER,
            test_category TEXT,   -- e.g., 'Hemogram', 'Lipid Profile'
            test_name TEXT,       -- e.g., 'Hemoglobin', 'Cholesterol'
            result_value TEXT,    -- Original string e.g., '12.5 g/dL'
            value_numeric REAL,   -- Clean number for graphs: 12.5
            unit TEXT,            -- Clean unit: 'g/dL'
            reference_range TEXT, -- e.g., '13.0 - 17.0'
            is_abnormal INTEGER,  -- 0 (Normal) or 1 (Abnormal)
            FOREIGN KEY (report_id) REFERENCES reports (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")

def save_report_data(metadata, test_data):
    """
    Ek baar mein puri report save karega.
    metadata: Dictionary {filename, patient_name, report_date, ...}
    test_data: List of Dictionaries containing test results
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Insert Metadata
        cursor.execute('''
            INSERT INTO reports (filename, patient_name, report_date, lab_name)
            VALUES (?, ?, ?, ?)
        ''', (metadata.get('filename'), metadata.get('patient_name'), 
              metadata.get('report_date'), metadata.get('lab_name')))
        
        report_id = cursor.lastrowid # Abhi jo report save hui, uska ID le lo
        
        # 2. Insert All Test Results (Loop)
        for item in test_data:
            cursor.execute('''
                INSERT INTO test_results 
                (report_id, test_category, test_name, result_value, value_numeric, unit, reference_range, is_abnormal)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                report_id,
                item.get('category', 'General'),
                item.get('test_name'),
                item.get('original_result'),
                item.get('numeric_value'), # Ye hum Python/Gemini se clean karke bhejenge
                item.get('unit'),
                item.get('reference_range'),
                1 if item.get('status') == 'Abnormal' else 0 # Logic for 0/1
            ))
            
        conn.commit()
        return True, "Data saved successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def get_trend_data(parameter_name):
    """Graph banane ke liye specific parameter ka historical data layega"""
    conn = get_connection()
    query = f'''
        SELECT r.report_date, t.value_numeric, t.unit, t.reference_range
        FROM test_results t
        JOIN reports r ON t.report_id = r.id
        WHERE t.test_name LIKE ? 
        ORDER BY r.report_date ASC
    '''
    # Fuzzy matching taaki 'Hemoglobin' aur 'Hb' same maane jayein
    df = pd.read_sql_query(query, conn, params=(f'%{parameter_name}%',))
    conn.close()
    return df

# Initialize DB on first run
if __name__ == "__main__":
    init_db()