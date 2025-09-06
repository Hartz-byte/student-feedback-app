import streamlit as st
import requests
import pandas as pd
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Student Feedback", layout="wide")
st.title("Student Feedback Form (Streamlit + FastAPI)")

# ---- Create / Update Form ----
with st.form("feedback_form"):
    name = st.text_input("Student name")
    email = st.text_input("Email")
    course = st.text_input("Course")
    rating = st.selectbox("Rating", [1, 2, 3, 4, 5], index=4)
    tags = st.text_input("Tags (comma separated)")
    comments = st.text_area("Comments")

    submit = st.form_submit_button("Submit")
    if submit:
        payload = {
            "name": name,
            "email": email,
            "course": course,
            "rating": rating,
            "tags": [t.strip() for t in tags.split(",") if t.strip()],
            "comments": comments,
        }
        resp = requests.post(f"{API_URL}/feedback", json=payload)
        if resp.status_code == 200:
            st.success("Feedback saved.")
        else:
            st.error(f"Error: {resp.text}")


# ---- List entries ----
resp = requests.get(f"{API_URL}/feedback")
if resp.status_code == 200:
    data = resp.json()
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df[["id", "name", "course", "rating", "submitted_at"]], use_container_width=True)

        selected_id = st.selectbox("Select ID for actions", options=df["id"])
        if st.button("Delete"):
            r = requests.delete(f"{API_URL}/feedback/{selected_id}")
            if r.status_code == 200:
                st.success("Deleted.")
            else:
                st.error(r.text)

        if st.button("Summarize"):
            r = requests.get(f"{API_URL}/summarize/{selected_id}")
            if r.status_code == 200:
                st.info(r.json()["summary"])
            else:
                st.error(r.text)
    else:
        st.info("No feedback available yet.")
else:
    st.error("Failed to connect to backend.")
