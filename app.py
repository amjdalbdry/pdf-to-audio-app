import streamlit as st
import fitz
import easyocr
from PIL import Image
import numpy as np
from gtts import gTTS

st.title("🎧 محول الملفات والصور إلى صوت")

# حل مشكلة الذاكرة: تحميل النموذج فقط عند الحاجة الفعلية
def get_reader():
    if 'reader' not in st.session_state:
        # استخدام gpu=False ضروري جداً
        st.session_state.reader = easyocr.Reader(['ar', 'en'], gpu=False)
    return st.session_state.reader

option = st.radio("اختر الوسيلة:", ("رفع ملف PDF", "التقاط صورة"))

text = ""

if option == "رفع ملف PDF":
    uploaded_file = st.file_uploader("ارفع ملف PDF", type=["pdf"])
    if uploaded_file:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "".join([page.get_text() for page in doc])

elif option == "التقاط صورة":
    camera_image = st.file_uploader("التقط صورة", type=["jpg", "jpeg", "png"])
    if camera_image:
        with st.spinner('جاري تحميل النموذج ومعالجة الصورة...'):
            reader = get_reader() # يتم التحميل هنا فقط عند الضغط
            image = Image.open(camera_image)
            results = reader.readtext(np.array(image), detail=0)
            text = " ".join(results)

if text:
    st.text_area("النص:", text, height=150)
    if st.button("تحويل لصوت"):
        tts = gTTS(text=text, lang='ar')
        tts.save("output.mp3")
        st.audio("output.mp3")
