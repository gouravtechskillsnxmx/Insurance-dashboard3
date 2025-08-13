import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import db, clients, reminders
from clients import list_policies, add_client, add_policy

# Initialize DB and scheduler
db.init()
reminders.queue_upcoming_reminders()  # non-blocking

st.set_page_config(page_title="Renewal Reminder & Client Manager", layout="wide")
st.title("Renewal Reminder & Client Manager (Demo)")

tab = st.sidebar.radio("Menu", ["Dashboard", "Add Client/Policy", "Upcoming Renewals", "Send Test Message"])

if tab == "Dashboard":
    df = list_policies()
    st.metric("Total Policies", len(df))
    today = datetime.today().date()
    soon = df[
        (pd.to_datetime(df['expiry_date']).dt.date >= today) &
        (pd.to_datetime(df['expiry_date']).dt.date <= (today + timedelta(days=30)))
    ]
    st.metric("Renewals next 30d", len(soon))
    st.dataframe(df.sort_values('expiry_date').head(50))

elif tab == "Add Client/Policy":
    with st.form("client_form", clear_on_submit=True):
        name = st.text_input("Client name")
        phone = st.text_input("Phone (with country code, e.g. +91...)")
        email = st.text_input("Email")
        notes = st.text_area("Notes")
        if st.form_submit_button("Add Client"):
            if not name:
                st.error("Name required")
            else:
                clients.add_client(name, phone, email, notes)
                st.success("Client added")

    st.markdown("---")
    with st.form("policy_form", clear_on_submit=True):
        clients_df = pd.read_sql("SELECT id,name FROM clients", db.get_conn(), parse_dates=[])
        client_options = clients_df.to_dict(orient='records')
        if client_options:
            cid = st.selectbox(
                "Client",
                options=[c['id'] for c in client_options],
                format_func=lambda x: next((c['name'] for c in client_options if c['id'] == x), str(x))
            )
        else:
            cid = None
            st.info("Add a client first")

        policy_no = st.text_input("Policy No")
        insurer = st.text_input("Insurer")
        ptype = st.text_input("Policy Type")
        issued = st.date_input("Issued Date", value=datetime.today().date())
        expiry = st.date_input("Expiry Date", value=(datetime.today() + timedelta(days=365)).date())
        premium = st.number_input("Premium", value=10000.0, min_value=0.0)
        agent = st.text_input("Agent", value="You")
        if st.form_submit_button("Add Policy"):
            if not cid:
                st.error("No client selected")
            else:
                add_policy(
                    cid, policy_no, insurer, ptype,
                    issued.isoformat(), expiry.isoformat(),
                    float(premium), agent
                )
                st.success("Policy added")

elif tab == "Upcoming Renewals":
    df = list_policies()
    df['expiry_date'] = pd.to_datetime(df['expiry_date']).dt.date
    soon = df[df['expiry_date'] <= (datetime.today().date() + timedelta(days=30))]
    st.dataframe(soon.sort_values('expiry_date').reset_index(drop=True))
    if not soon.empty:
        if st.download_button(
            "Download Renewals as Excel",
            data=soon.to_excel(index=False),
            file_name=f"renewals_{datetime.today().date()}.xlsx"
        ):
            st.success("Exported to Excel")

elif tab == "Send Test Message":
    phone = st.text_input("Phone for test (with country code)", value="")
    msg = st.text_area("Message", value="Reminder: your policy is due soon. Contact your agent.")
    if st.button("Send"):
        try:
            sid = reminders.send_test_message(phone, msg)

            if sid == "SIMULATED-SEND":
                st.warning(f"[SIMULATION MODE] Would send to {phone}: {msg}")

            elif sid and isinstance(sid, str) and sid.startswith("SM"):
                st.success(f"✅ Sent via Twilio (SID: {sid})")

            elif sid:
                st.info(f"Message sent, SID: {sid}")

            else:
                st.error("❌ Failed to send. Check Twilio logs or credentials.")

        except Exception as e:
            st.error(f"Send failed: {e}")

st.caption(
    "Template: customize fields, add agent login, WhatsApp reminders, or import your CSVs into data/ folder."
)
