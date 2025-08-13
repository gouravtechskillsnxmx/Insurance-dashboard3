elif tab == "Send Test Message":
    phone = st.text_input("Phone for test (with country code)", value="")
    msg = st.text_area(
        "Message",
        value="Reminder: your policy is due soon. Contact your agent."
    )

    if st.button("Send"):
        try:
            sid = reminders.send_test_message(phone, msg)

            if sid == "SIMULATED-SEND":
                st.warning(f"[SIMULATION MODE] Would send to {phone}: {msg}")
            elif sid and sid.startswith("SM"):
                st.success(f"✅ Sent via Twilio (SID: {sid})")
            elif sid:
                st.info(f"Message sent with SID: {sid}")
            else:
                st.error("❌ Failed to send. Check Twilio logs or credentials.")

        except Exception as e:
            st.error(f"Send failed: {e}")
