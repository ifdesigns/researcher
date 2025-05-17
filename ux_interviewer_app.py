import streamlit as st
from openai import OpenAI
from gtts import gTTS
import os
import tempfile
from io import BytesIO

# Set your OpenAI key
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # or replace with your key directly (not recommended for production)
)

st.set_page_config(page_title="UX Tədqiqatçı", page_icon="💬", layout="centered")
st.title("💬 UX Tədqiqatçı (Azərbaycan dili)")

# Initialize chat state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "initiated" not in st.session_state:
    st.session_state.initiated = False

SYSTEM_PROMPT = """
Sən bir istifadəçi təcrübəsi (UX) tədqiqatçısısan. Məqsədin istifadəçi ilə səmimi söhbət şəklində müsahibə aparmaqdır.
Müsahibəyə özünü təqdim edərək və məqsədi izah edərək başla. Sonra ilk UX sualını ver.
"""

def speak(text):
    tts = gTTS(text, lang="az")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")

def get_openai_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message["content"]

# Trigger first message automatically
if not st.session_state.initiated:
    st.session_state.messages.append({"role": "system", "content": SYSTEM_PROMPT})
    first_response = get_openai_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": first_response})
    st.session_state.initiated = True
    with st.chat_message("assistant"):
        st.markdown(first_response)
        speak(first_response)

# Display past messages
for msg in st.session_state.messages[1:]:  # Skip system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("İstifadəçi cavabınızı yazın...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = get_openai_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
        speak(response)
