import sqlite3
import pandas as pd

DB_NAME = "clinical_db.sqlite"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Reports Table
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

    # Test Results Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER,
            test_category TEXT,
            test_name TEXT,
            result_value TEXT,
            value_numeric REAL,
            unit TEXT,
            reference_range TEXT,
            is_abnormal INTEGER,
            FOREIGN KEY (report_id) REFERENCES reports (id)
        )
    ''')
    conn.commit()
    conn.close()

def save_report_data(metadata, test_data):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO reports (filename, patient_name, report_date, lab_name)
            VALUES (?, ?, ?, ?)
        ''', (metadata.get('filename'), metadata.get('patient_name'), 
              metadata.get('report_date'), metadata.get('lab_name')))
        
        report_id = cursor.lastrowid
        
        for item in test_data:
            # Smart status check
            status = str(item.get('status', '')).lower()
            is_abnormal = 1 if status in ['abnormal', 'high', 'low', 'positive'] else 0
            
            cursor.execute('''
                INSERT INTO test_results 
                (report_id, test_category, test_name, result_value, value_numeric, unit, reference_range, is_abnormal)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                report_id,
                item.get('category', 'General'),
                item.get('test_name'),
                item.get('original_result'),
                item.get('numeric_value'),
                item.get('unit'),
                item.get('reference_range'),
                is_abnormal
            ))
        conn.commit()
        return True, "Data saved successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def get_trend_data(parameter_name):
    conn = get_connection()
    # Fuzzy search for parameter
    query = f'''
        SELECT r.report_date, t.value_numeric, t.unit, t.reference_range
        FROM test_results t
        JOIN reports r ON t.report_id = r.id
        WHERE t.test_name LIKE ? 
        ORDER BY r.report_date ASC
    '''
    try:
        df = pd.read_sql_query(query, conn, params=(f'%{parameter_name}%',))
    except:
        df = pd.DataFrame()
    conn.close()
    return df

# 👇 YEH FUNCTION MISSING THA, ISLIYE ERROR AA RAHA THA
def get_unique_test_names():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT test_name FROM test_results ORDER BY test_name ASC")
        return [row[0] for row in cursor.fetchall() if row[0]]
    except:
        return []
    finally:
        conn.close()