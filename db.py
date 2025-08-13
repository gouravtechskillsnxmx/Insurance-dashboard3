# db.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "renewal.db"
DB_PATH.parent.mkdir(exist_ok=True)

SCHEMA = [
"""CREATE TABLE IF NOT EXISTS clients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    notes TEXT
)""",
"""CREATE TABLE IF NOT EXISTS policies(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    policy_no TEXT,
    insurer TEXT,
    policy_type TEXT,
    issued_date TEXT,
    expiry_date TEXT,
    premium REAL,
    agent TEXT,
    status TEXT,
    notes TEXT,
    FOREIGN KEY(client_id) REFERENCES clients(id)
)""",
"""CREATE TABLE IF NOT EXISTS reminders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_id INTEGER,
    remind_date TEXT,
    sent INTEGER DEFAULT 0,
    medium TEXT,
    message TEXT,
    created_at TEXT,
    FOREIGN KEY(policy_id) REFERENCES policies(id)
)"""
]

def init(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    for s in SCHEMA:
        cur.execute(s)
    conn.commit()
    conn.close()

def get_conn(db_path=DB_PATH):
    return sqlite3.connect(r"C:\Gourav_CashNxMx_TechSkillsNxMx\PythonNxMx\small projects\Insurance_dashboard3\data\renewal.db")
