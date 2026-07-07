import streamlit as st
import fitz
import requests
from gtts import gTTS
import io

st.title("🎧 محول الملفات والصور إلى صوت")

# ضع المفتاح هنا مباشرة لتجاوز مشكلة الـ Secrets
API_KEY = 'K89501552688957' 

def ocr_space_file(file):
    payload = {'apikey': API_KEY, 'language': 'ara', 'isOverlayRequired': False}
    response = requests.post('https://api.ocr.space/parse/image', files={'file': file}, data=payload)
    result = response.json()
    if 'ParsedResults' in result:
        return result['ParsedResults'][0]['ParsedText']
    return None

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
    img_file = st.file_uploader("التقط صورة للنص", type=["jpg", "png", "jpeg"])
    if img_file and st.button("استخراج وتحويل"):
        with st.spinner('جاري المعالجة السحابية...'):
            text = ocr_space_file(img_file)
            if text:
                st.text_area("النص المستخرج:", text)
                tts = gTTS(text=text, lang='ar')
                tts.save("output.mp3")
                st.audio("output.mp3")
            else:
                st.error("لم يتم العثور على نص. تأكد من وضوح الصورة.")
