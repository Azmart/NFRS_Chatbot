# frontend/app.py

import streamlit as st
import requests
import uuid
import datetime

API_URL = "http://localhost:8000"

# Session state for conversation and language
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "language" not in st.session_state:
    st.session_state.language = "English"

# Language options
LANGUAGE_OPTIONS = {
    "English": "en",
    "Nepali (Romanized)": "ne-roman",
    "Nepali (Devanagari)": "ne"
}

# ─────────────────────────────────────────────
# Language Selection
# ─────────────────────────────────────────────
st.sidebar.title("🌐 Language")
selected_language = st.sidebar.selectbox(
    "Select your preferred language",
    options=list(LANGUAGE_OPTIONS.keys()),
    index=list(LANGUAGE_OPTIONS.keys()).index(st.session_state.language)
)
if selected_language != st.session_state.language:
    st.session_state.language = selected_language
    st.session_state.messages = []  # Clear messages when language changes

# ─────────────────────────────────────────────
# Auto-create new session if not already started
# ─────────────────────────────────────────────
if st.session_state.session_id is None:
    res = requests.post(f"{API_URL}/new_session")
    if res.ok:
        st.session_state.session_id = res.json()["session_id"]
        st.session_state.messages = []

# ─────────────────────────────────────────────
# Sidebar: Session List + New Chat Button
# ─────────────────────────────────────────────
st.sidebar.title("🗂️ Conversations")

# Load session list from backend
def load_sessions():
    res = requests.get(f"{API_URL}/sessions")
    return res.json() if res.ok else []

sessions = load_sessions()

# Show session list in sidebar
for s in sessions:
    label = f"{s['created_at'][:16]}..."  # show date
    if st.sidebar.button(label, key=s['session_id']):
        st.session_state.session_id = s["session_id"]
        st.session_state.messages = []
        res = requests.get(f"{API_URL}/history/{s['session_id']}")
        if res.ok:
            for item in res.json():
                st.session_state.messages.append({
                    "role": "user",
                    "text": item["question"]
                })
                st.session_state.messages.append({
                    "role": "assistant",
                    "text": item["answer"],
                    "sources": item["sources"]
                })

# Start new session manually
if st.sidebar.button("➕ New Conversation"):
    res = requests.post(f"{API_URL}/new_session")
    if res.ok:
        sid = res.json()["session_id"]
        st.session_state.session_id = sid
        st.session_state.messages = []

# ─────────────────────────────────────────────
# Main Chat Window
# ─────────────────────────────────────────────
st.title("📘 Locally run NFRS / IFRS Assistant")

# Show language selection reminder
if st.session_state.language != "English":
    st.info(f"💡 You are chatting in {st.session_state.language}. Your messages will be automatically translated.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("📎 Sources"):
                for ref in msg["sources"]:
                    st.write(f"- {ref['source']} (Page {ref['page']})")

# Input box with language-specific placeholder
placeholders = {
    "English": "Ask your financial question...",
    "Nepali (Romanized)": "Aafno financial prashna sodhnus...",
    "Nepali (Devanagari)": "आफ्नो financial प्रश्न सोध्नुहोस्..."
}
user_input = st.chat_input(placeholders[st.session_state.language])

if user_input and st.session_state.session_id:
    # Show user message
    st.session_state.messages.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send to backend with language preference
    with st.spinner("Thinking..."):
        try:
            res = requests.post(f"{API_URL}/query", json={
                "question": user_input,
                "session_id": st.session_state.session_id,
                "language": LANGUAGE_OPTIONS[st.session_state.language]
}, timeout=300)

            if res.ok:
                data = res.json()
                answer = data["answer"]
                sources = data["sources"]

                st.session_state.messages.append({
                    "role": "assistant",
                    "text": answer,
                    "sources": sources
                })

                with st.chat_message("assistant"):
                    st.markdown(answer)
                    with st.expander("📎 Sources"):
                        for ref in sources:
                            st.write(f"- {ref['source']} (Page {ref['page']})")
            else:
                st.error("❌ Failed to get response from backend.")
                st.code(res.text)

        except Exception as e:
            st.error("❌ Error communicating with backend.")
            st.code(str(e))