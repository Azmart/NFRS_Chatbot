# frontend/app.py

import streamlit as st
import requests

API_URL = "http://localhost:8000/query"

st.set_page_config(page_title="NFRS/IFRS Assistant")
st.title("📘 NFRS / IFRS Financial Reporting Assistant")

question = st.text_area("Ask a financial reporting question:", height=100)

if st.button("Get Answer") and question.strip():
    with st.spinner("Searching knowledge base..."):
        response = requests.post(API_URL, json={"question": question})
        if response.ok:
            data = response.json()
            st.markdown("### 💬 Answer")
            st.write(data["answer"])

            st.markdown("### 📎 Sources")
            for source in data["sources"]:
                st.write(f"- {source['source']} (Page {source['page']})")
        else:
            st.error("Failed to get response from backend.")