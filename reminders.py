# reminders.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import pandas as pd
from db import get_conn
from whatsapp import send_whatsapp

sched = BackgroundScheduler()

def queue_upcoming_reminders(db_path=None):
    conn = get_conn(db_path)
    df = pd.read_sql_query("""
        SELECT r.id as rid, r.policy_id, r.remind_date, r.sent, r.medium, r.message, p.policy_no, c.phone
        FROM reminders r
        JOIN policies p ON p.id=r.policy_id
        JOIN clients c ON c.id=p.client_id
        WHERE r.sent=0 AND DATE(r.remind_date) <= DATE('now','+30 day')
    """, conn)
    conn.close()
    for _, row in df.iterrows():
        run_dt = pd.to_datetime(row['remind_date']).to_pydatetime()
        sched.add_job(send_reminder_job, 'date', run_date=run_dt, args=[row['rid']], id=f"rem_{row['rid']}", replace_existing=True)
    if not sched.running:
        sched.start()

def send_reminder_job(reminder_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT r.id,p.policy_no,c.phone,r.message FROM reminders r JOIN policies p ON p.id=r.policy_id JOIN clients c ON c.id=p.client_id WHERE r.id=?", (reminder_id,))
    r = cur.fetchone()
    if not r:
        conn.close(); return
    _, policy_no, phone, message = r
    try:
        send_whatsapp(phone, message)
        cur.execute("UPDATE reminders SET sent=1 WHERE id=?", (reminder_id,))
        conn.commit()
    except Exception as e:
        print("send failed:", e)
    conn.close()
