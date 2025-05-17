import streamlit as st
import openai
import os
from gtts import gTTS
import tempfile

# Set your OpenAI API key (in production use environment variables or Streamlit secrets)
openai.api_key = "sk-..."  # Replace with your real key or use `st.secrets["openai_api_key"]`

# AI system prompt: defines the assistant's role and tone
SYSTEM_PROMPT = """
Sən bir istifadəçi təcrübəsi (UX) tədqiqatçısısan. Məqsədin istifadəçilərlə müsahibə aparmaq və onların məhsulla bağlı təcrübələrini başa düşməkdir. 
Dəqiq, səmimi və mehriban tonla danış. Sual verdikdən sonra cavab gözlə.
"""

# Intro message and first UX interview question
intro_message = (
    "Salam! Mən istifadəçi təcrübəsi üzrə süni intellekt tədqiqatçısıyam. "
    "Bu müsahibədə sizdən məhsul və ya xidmətlə bağlı təcrübələrinizi eşitmək istəyirəm. "
    "İcazənizlə başlayaq. İlk sualım budur:"
)

first_question = "Bu məhsulu və ya xidməti sonuncu dəfə nə vaxt istifadə etdiniz və hansı məqsədlə?"

def speak(text):
    """Convert text to speech using gTTS and play it in Streamlit."""
    tts = gTTS(text, lang="az")
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")

# Streamlit UI setup
st.set_page_config(page_title="AI UX Tədqiqatçı", page_icon="🧠")
st.title("🧠 UX Süni İntellekt Müsahibəsi")

# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Start conversation with system prompt and intro
    st.session_state.messages.append({"role": "system", "content": SYSTEM_PROMPT})
    st.session_state.messages.append({"role": "assistant", "content": intro_message})
    st.session_state.messages.append({"role": "assistant", "content": first_question})
    speak(intro_message)
    speak(first_question)

# Display the conversation history
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# Chat input
prompt = st.chat_input("Cavabınızı yazın və ya sual verin...")

# If user submits a message
if prompt:
    # Show user message
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call OpenAI chat completion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    assistant_reply = response.choices[0].message["content"]

    # Show and store AI reply
    st.chat_message("assistant").write(assistant_reply)
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    speak(assistant_reply)
