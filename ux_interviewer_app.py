import streamlit as st
import openai
from gtts import gTTS
import os

# Make sure API key is loaded securely
openai.api_key = st.secrets["openai"]["api_key"]

# Intro script
intro_script = """
Salam! Mən Süni İntellekt dəstəkli istifadəçi təcrübəsi (UX) tədqiqatçısıyam. 
Bu qısa müsahibə istifadəçilərin təcrübələrini daha yaxşı anlamaq üçün nəzərdə tutulub.

Müsahibə zamanı sizdən məhsul və ya xidmətlə bağlı təcrübələrinizi paylaşmağınızı istəyəcəyəm.
Məlumatlar anonim saxlanacaq və yalnız tədqiqat məqsədilə istifadə olunacaq.

Hazırsınızsa, başlayaq!

Sual 1: Zəhmət olmasa özünüzü təqdim edin və gündəlik texnologiya istifadəniz haqqında qısa məlumat verin.
"""

# Run intro only once
if "intro_done" not in st.session_state:
    st.session_state.intro_done = True
    st.markdown(intro_script)

    # Text-to-speech
    tts = gTTS(intro_script, lang='az')
    tts.save("intro.mp3")
    st.audio("intro.mp3", format="audio/mp3")

# Text input area for user response
user_input = st.text_area("Cavabınızı buraya yazın və ya dikta edin:", "")

if user_input:
    # Pass to GPT for follow-up or summarization
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Sən UX tədqiqatçısısan. Qısa, aydın və təhrik edici suallar ver."},
            {"role": "user", "content": user_input}
        ]
    )
    reply = response.choices[0].message.content
    st.write("AI cavabı:", reply)

    # Optional: speak the next AI question
    tts = gTTS(reply, lang='az')
    tts.save("ai_reply.mp3")
    st.audio("ai_reply.mp3", format="audio/mp3")

