import streamlit as st
import fitz
import requests
from gtts import gTTS

st.title("🎧 محول الملفات والصور")

# 1. نحاول الحصول على المفتاح من الـ Secrets، إذا لم يوجد، نطلب من المستخدم إدخاله
if "OCR_API_KEY" in st.secrets:
    API_KEY = st.secrets["OCR_API_KEY"]
else:
    API_KEY = st.text_input("أدخل مفتاح OCR API الخاص بك هنا:", type="password")

def ocr_space_file(file, api_key):
    payload = {'apikey': api_key, 'language': 'ara', 'isOverlayRequired': False}
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
    if img_file and API_KEY:
        if st.button("استخراج وتحويل"):
            with st.spinner('جاري المعالجة السحابية...'):
                text = ocr_space_file(img_file, API_KEY)
                if text:
                    st.text_area("النص المستخرج:", text)
                    tts = gTTS(text=text, lang='ar')
                    tts.save("output.mp3")
                    st.audio("output.mp3")
                else:
                    st.error("خطأ: تأكد من مفتاح الـ API ومن وضوح الصورة.")
    elif img_file and not API_KEY:
        st.warning("يرجى إدخال مفتاح الـ API في الحقل بالأعلى للبدء.")
