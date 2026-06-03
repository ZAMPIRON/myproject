import sqlite3

conn = sqlite3.connect("buddy.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("--- USERS REGISTERED ---")
try:
    cursor.execute("SELECT id, github, country, has_idea, pitch FROM users")
    usuarios = cursor.fetchall()
    
    if not usuarios:
        print("The database is empty!")
    else:
        for u in usuarios:
            print(f"ID: {u['id']} | GitHub: @{u['github']} | Timezone/Country: {u['country']} | Has Idea?: {u['has_idea']} | Pitch: '{u['pitch']}'")
except sqlite3.OperationalError as e:
    print(f"ERROR: Table not found or database is corrupted. Details: {e}")

conn.close()