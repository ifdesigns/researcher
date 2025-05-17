import streamlit as st
import openai
import os

# API key (use secret manager in production)
openai.api_key = st.secrets["openai"]["api_key"]


SYSTEM_PROMPT = """
Sən bir istifadəçi təcrübəsi (UX) tədqiqatçısısan. Məqsədin istifadəçidən məhsul və ya xidmətlə bağlı təcrübəsini anlamaqdır...
"""

st.title("💬 UX Tədqiqatçı (Azərbaycan dili)")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

user_input = st.chat_input("İstifadəçi cavabınızı yazın...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Tədqiqatçı cavab verir..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state.messages,
            temperature=0.7
        )
        reply = response["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": reply})

for msg in st.session_state.messages[1:]:
    role = "İstifadəçi" if msg["role"] == "user" else "Tədqiqatçı"
    with st.chat_message(role):
        st.markdown(msg["content"])
