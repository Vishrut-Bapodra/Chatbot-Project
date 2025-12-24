import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Any

DB_PATH = "chatbot_memory.db"

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS chat_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT DEFAULT 'New Chat',
        created_at TEXT NOT NULL
)
""")
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS chat_messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY(session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE
)
""")
    

    conn.commit()
    conn.close()

def create_chat_session(name: str = "New Chat") -> int:
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_sessions (name, created_at) VALUES (?,?)",
        (name, datetime.utcnow().isoformat())
    )
    conn.commit()
    session_id = cur.lastrowid
    conn.close()
    return session_id

def get_all_chats() -> List[Dict[str, Any]]:
    conn = get_db()
    rows = conn.execute("SELECT id, name, created_at FROM chat_sessions ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def rename_chat(session_id: int, new_name: str) -> None:
    conn = get_db()
    conn.execute("UPDATE chat_sessions SET name = ? WHERE id = ?", (new_name, session_id))
    conn.commit()
    conn.close()

def delete_chat(session_id: int) -> None:
    conn = get_db()
    conn.execute("DELETE FROM chat_sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()

def save_message(session_id: int, role: str, content: str) -> int:
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_messages (session_id, role, content, timestamp) VALUES (?,?,?,?)",
        (session_id, role, content, datetime.utcnow().isoformat())
    )
    conn.commit()
    msg_id = cur.lastrowid
    conn.close()
    return msg_id

def load_chat_messages(session_id: int, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    conn = get_db()
    if limit is None:
        rows = conn.execute(
            "SELECT id, role, content, timestamp FROM chat_messages WHERE session_id = ? ORDER BY id ASC",
            (session_id,)
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT id, role, content, timestamp FROM chat_messages
            WHERE session_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (session_id, limit)
        ).fetchall()
        rows = list(reversed(rows))
    conn.close()
    return [{"id": r["id"], "role": r["role"], "content": r["content"], "timestamp": r["timestamp"]} for r in rows]

def clear_chat_messages(session_id: int) -> None:
    conn = get_db()
    conn.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()


def get_chat_count() -> int:
    conn = get_db()
    row = conn.execute("SELECT COUNT(*) as c FROM chat_sessions").fetchone()
    conn.close()
    return int(row["c"]) if row else 0
