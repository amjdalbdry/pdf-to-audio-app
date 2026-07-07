import streamlit as st
from gtts import gTTS
import fitz
import easyocr
from PIL import Image
import numpy as np

st.title("🎧 محول الملفات والصور إلى صوت")

# تحميل القارئ (استخدام الكاش لتسريع الأداء)
@st.cache_resource
def load_reader():
    return easyocr.Reader(['ar', 'en'])

reader = load_reader()

option = st.radio("اختر وسيلة الإدخال:", ("رفع ملف PDF", "التقاط صورة بالكاميرا"))
text = ""

if option == "رفع ملف PDF":
    uploaded_file = st.file_uploader("ارفع ملف PDF", type=["pdf"])
    if uploaded_file:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()

elif option == "التقاط صورة بالكاميرا":
    camera_image = st.camera_input("التقط صورة للنص")
    if camera_image:
        image = Image.open(camera_image)
        # تحويل الصورة إلى مصفوفة لقراءتها عبر الذكاء الاصطناعي
        img_array = np.array(image)
        with st.spinner('جاري قراءة الصورة...'):
            results = reader.readtext(img_array, detail=0)
            text = " ".join(results)

if text:
    st.write("تم استخراج النص بنجاح:")
    st.text_area("النص المستخرج:", text, height=200)
    
    if st.button("تحويل إلى صوت"):
        with st.spinner('جاري تحويل النص إلى صوت...'):
            tts = gTTS(text=text, lang='ar')
            tts.save("output.mp3")
            st.audio("output.mp3")
            with open("output.mp3", "rb") as file:
                st.download_button("تحميل الملف الصوتي", file, "output.mp3")
