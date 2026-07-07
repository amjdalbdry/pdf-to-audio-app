import streamlit as st
import fitz
from gtts import gTTS

st.title("🎧 محول ملفات PDF إلى صوت")

uploaded_file = st.file_uploader("ارفع ملف PDF", type=["pdf"])

if uploaded_file:
    with st.spinner('جاري قراءة الملف...'):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        
        st.text_area("النص المستخرج:", text, height=200)
        
        if st.button("تحويل إلى صوت"):
            tts = gTTS(text=text, lang='ar')
            tts.save("output.mp3")
            st.audio("output.mp3")
            with open("output.mp3", "rb") as file:
                st.download_button("تحميل الملف الصوتي", file, "output.mp3")
                
