import streamlit as st
from gtts import gTTS
import fitz
import easyocr
from PIL import Image
import numpy as np
import os

st.title("🎧 محول الملفات والصور")

# تقليل استهلاك الذاكرة عبر تحميل النموذج مرة واحدة فقط وبشكل مبسط
@st.cache_resource
def load_reader():
    # استخدام وحدة المعالجة المركزية (CPU) فقط وبدون GPU لتوفير الذاكرة
    return easyocr.Reader(['ar', 'en'], gpu=False)

try:
    reader = load_reader()
except Exception as e:
    st.error(f"خطأ في تحميل نموذج الذكاء الاصطناعي: {e}")

option = st.radio("اختر وسيلة الإدخال:", ("رفع ملف PDF", "التقاط صورة"))

if option == "رفع ملف PDF":
    uploaded_file = st.file_uploader("ارفع ملف PDF", type=["pdf"])
    if uploaded_file:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "".join([page.get_text() for page in doc])
        st.text_area("النص:", text)
        if st.button("تحويل لصوت"):
            tts = gTTS(text=text, lang='ar')
            tts.save("output.mp3")
            st.audio("output.mp3")

elif option == "التقاط صورة":
    camera_image = st.file_uploader("التقط صورة", type=["jpg", "jpeg", "png"])
    if camera_image:
        image = Image.open(camera_image)
        with st.spinner('جاري التحليل...'):
            results = reader.readtext(np.array(image), detail=0)
            text = " ".join(results)
            st.text_area("النص المستخرج:", text)
            if st.button("تحويل لصوت"):
                tts = gTTS(text=text, lang='ar')
                tts.save("output.mp3")
                st.audio("output.mp3")
