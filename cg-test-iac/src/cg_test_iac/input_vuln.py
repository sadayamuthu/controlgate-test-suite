import sqlite3
import subprocess

def get_user_data(user_id: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Vulnerability: SQL Injection vector
    query = f"SELECT * FROM users WHERE id = '{user_id}';"
    cursor.execute(query)
    
    return cursor.fetchall()

def ping_server(hostname: str):
    # Vulnerability: OS Command Injection vector
    command = "ping -c 1 " + hostname
    subprocess.Popen(command, shell=True)
