import sqlite3

conn = sqlite3.connect(
 "naqaa.db",
 check_same_thread=False
)

db = conn.cursor()

db.execute("""
CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY,
nickname TEXT,
start_date TEXT,
relapses INTEGER DEFAULT 0,
best_streak INTEGER DEFAULT 0,
points INTEGER DEFAULT 0
)
""")

conn.commit()


def add_user(uid):
    db.execute("""
    INSERT OR IGNORE INTO users
    (user_id,nickname,start_date)
    VALUES (?,?,date('now'))
    """,(uid,"أخي الكريم"))

    conn.commit()


def get_user(uid):
    db.execute(
      "SELECT * FROM users WHERE user_id=?",
      (uid,)
    )
    return db.fetchone()


def add_relapse(uid):
    db.execute("""
    UPDATE users
    SET relapses=relapses+1,
    start_date=date('now')
    WHERE user_id=?
    """,(uid,))
    conn.commit()
