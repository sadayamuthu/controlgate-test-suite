# Gate 6: Input Validation & Error Handling Gate
import os
import sqlite3

def run_query(user_id):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # SQL injection via string formatting
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    
    return cursor.fetchall()

def process_data(data):
    try:
        # Use of eval() - code injection risk
        result = eval(data)
        
        # Use of os.system() - command injection risk
        os.system(f"echo {data}")
    except:
        # Bare except clause
        pass

if __name__ == '__main__':
    run_query("1 OR 1=1")
    process_data("print('Hello')")
