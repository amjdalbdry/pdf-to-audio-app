import streamlit as st
import fitz
from gtts import gTTS
from PIL import Image
import numpy as np

st.title("🎧 محول الملفات والصور")

# تقليل الاستيراد داخل الدالة لتوفير الذاكرة
def process_image(image_file):
    import easyocr
    reader = easyocr.Reader(['ar', 'en'], gpu=False)
    image = Image.open(image_file)
    results = reader.readtext(np.array(image), detail=0)
    return " ".join(results)

option = st.radio("اختر الوسيلة:", ("رفع ملف PDF", "التقاط صورة"))

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
        with st.spinner('جاري تحليل الصورة...'):
            text = process_image(camera_image)
            st.text_area("النص المستخرج:", text)
            if st.button("تحويل لصوت"):
                tts = gTTS(text=text, lang='ar')
                tts.save("output.mp3")
                st.audio("output.mp3")
