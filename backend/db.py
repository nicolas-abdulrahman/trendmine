import sqlite3
from contextlib import contextmanager

DB_NAME = "electric_trivia.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        # Tabela de Contas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Account (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        # Tabela de Perfis
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER DEFAULT 0,
                account_id INTEGER,
                FOREIGN KEY (account_id) REFERENCES Account(id)
            )
        """)
        conn.commit()

# Inicializa o banco ao importar o arquivo
init_db()
