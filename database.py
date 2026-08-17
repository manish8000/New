import sqlite3

DB_NAME = "quiz_bot.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        is_banned INTEGER DEFAULT 0,
        is_auth INTEGER DEFAULT 0,
        premium INTEGER DEFAULT 0
    )''')

    # Quizzes Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS quizzes (
        quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        questions TEXT,
        penalty REAL DEFAULT 0.0,
        speed TEXT DEFAULT 'normal'
    )''')

    # Stats Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (
        user_id INTEGER PRIMARY KEY,
        quizzes_taken INTEGER DEFAULT 0,
        correct_answers INTEGER DEFAULT 0,
        wrong_answers INTEGER DEFAULT 0
    )''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    
