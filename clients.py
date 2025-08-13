# clients.py
import pandas as pd
from datetime import datetime
from db import get_conn

def add_client(name, phone=None, email=None, notes=None, db_path=None):
    conn = get_conn(db_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO clients (name,phone,email,notes) VALUES (?,?,?,?)",
                (name, phone, email, notes))
    conn.commit()
    conn.close()

def add_policy(client_id, policy_no, insurer, policy_type, issued_date, expiry_date, premium, agent, status='Active', notes=None, db_path=None):
    conn = get_conn(db_path)
    cur = conn.cursor()
    cur.execute("""INSERT INTO policies (client_id,policy_no,insurer,policy_type,issued_date,expiry_date,premium,agent,status,notes)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (client_id, policy_no, insurer, policy_type, issued_date, expiry_date, premium, agent, status, notes))
    conn.commit()
    conn.close()

def list_policies(db_path=None):
    conn = get_conn(db_path)
    df = pd.read_sql_query("SELECT p.*, c.name as client_name, c.phone as client_phone FROM policies p LEFT JOIN clients c ON p.client_id=c.id", conn, parse_dates=['issued_date','expiry_date'])
    conn.close()
    return df
