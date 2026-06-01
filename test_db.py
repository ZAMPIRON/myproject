import sqlite3

# Conecta ao arquivo do banco de dados
conn = sqlite3.connect("buddy.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("--- USUÁRIOS CADASTRADOS ---")
try:
    cursor.execute("SELECT id, github, country, has_idea, pitch FROM users")
    usuarios = cursor.fetchall()
    
    if not usuarios:
        print("O banco de dados está vazio!")
    else:
        for u in usuarios:
            print(f"ID: {u['id']} | GitHub: @{u['github']} | Timezone/Country: {u['country']} | Tem Ideia?: {u['has_idea']} | Pitch: '{u['pitch']}'")
except sqlite3.OperationalError as e:
    print(f"Erro: A tabela não existe ou o banco está corrompido. Detalhes: {e}")

conn.close()