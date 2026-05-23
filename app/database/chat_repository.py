import sqlite3

class ChatRepository:
    def __init__(self):
        self.conn = sqlite3.connect("chatbot.db")
        self.cursor = self.conn.cursor()

        # Criando a tabela de usuários
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL UNIQUE
            )
        """)

        # Criando a tabela de historico
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)

        # Salvando e fechando conexão
        self.conn.commit()
        self.conn.close()
    

    def findUserId(self, id):
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users
            WHERE id = ?
        """, (id,))

        user = cursor.fetchone()

        conn.close()

        return user

    
    def createUser(self, user_id):
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO users (user_id)
            VALUES (?)
        """, (user_id,))

        conn.commit()
        conn.close()


    def deteleUser(self, id):
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM users
            WHERE id = ?
        """, (id,))

        conn.commit()
        conn.close()


    def findAllHistory(self, user_id):
        # Retorna os 5 historico com user_id correspondente

        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 5
        """, (user_id,))

        history = cursor.fetchall()

        conn.close()

        return history

    
    def createHistory(self, user_id, question):
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO history (user_id, message)
            VALUES (?, ?)
        """, (user_id, question))

        conn.commit()
        conn.close()


    def deleteHistory(self, id):
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM history
            WHERE id = ?
        """, (id,))

        conn.commit()
        conn.close()
