import streamlit as st
from gtts import gTTS
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="PDF to Audio", page_icon="🎧")
st.title("🎧 محول الملفات إلى صوت")

uploaded_file = st.file_uploader("ارفع ملف PDF هنا", type=['pdf'])

if uploaded_file is not None:
    # 1. استخراج النص من الـ PDF
    with st.spinner('جاري استخراج النص...'):
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf_document:
            text += page.get_text()
        
    if text.strip() == "":
        st.error("لم نتمكن من استخراج نص من هذا الملف (قد يكون ملف صور).")
    else:
        st.success("تم استخراج النص بنجاح!")
        st.text_area("النص المستخرج:", text[:1000] + "...", height=200)

        # 2. تحويل النص إلى صوت
        if st.button("تحويل إلى صوت"):
            with st.spinner('جاري إنشاء الملف الصوتي...'):
                tts = gTTS(text=text, lang='ar') # 'ar' للغة العربية، استخدم 'en' للإنجليزية
                audio_file = io.BytesIO()
                tts.write_to_fp(audio_file)
                audio_file.seek(0)
                
                # 3. عرض زر التحميل
                st.audio(audio_file, format='audio/mp3')
                st.download_button(
                    label="تحميل الملف الصوتي",
                    data=audio_file,
                    file_name="converted_audio.mp3",
                    mime="audio/mp3"
                )