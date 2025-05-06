import os
import sqlite3

# Insecure: hardcoded credentials
username = "admin"
password = "1234"

# Insecure SQL query (SQL injection vulnerability)
def login(user_input):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{user_input}'"
    cursor.execute(query)
    result = cursor.fetchone()
    return result

# Insecure command execution (OS command injection)
def delete_file(filename):
    os.system("rm " + filename)

# Insecure: No input validation
user_input = input("Enter your username: ")
print(login(user_input))
