import streamlit as st
import google.genai as genai
from google.genai import types
import os

st.set_page_config(page_title="SSC AI Paper Analyzer", page_icon="📚", layout="centered")

st.title("📚 १० वी महाराष्ट्र बोर्ड - AI सर्व-विषय प्रश्नपत्रिका विश्लेषक")
st.write("मागील वर्षांच्या कोणत्याही विषयाच्या प्रश्नपत्रिका एकत्र अपलोड करा आणि जेमिनी AI कडून महा-विश्लेषण मिळवा!")

# स्ट्रीमलिटच्या सुरक्षित तिजोरीतून की मिळवणे
MY_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=MY_API_KEY)

# =========================================================================
# 📥 थेट पीडीएफ डाऊनलोड विभाग (Direct PDF Download Section)
# =========================================================================
st.markdown("---")
st.subheader("📥 मागील वर्षांच्या प्रश्नपत्रिका थेट डाऊनलोड करा")
st.write("खालील बटणावर क्लिक करून तुम्ही विषयानुसार पीडीएफ थेट तुमच्या डिव्हाइसवर डाऊनलोड करू शकता:")

col1, col2, col3 = st.columns(3)

# १. मराठी पेपर डाऊनलोड
with col1:
    marathi_path = "papers/marathi.pdf"
    if os.path.exists(marathi_path):
        with open(marathi_path, "rb") as file:
            st.download_button(
                label="📁 मराठी पेपर",
                data=file,
                file_name="Marathi_SSC_Paper.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.caption("⏳ मराठी पीडीएफ लवकरच येत आहे...")

# २. गणित पेपर डाऊनलोड
with col2:
    maths_path = "papers/maths.pdf"
    if os.path.exists(maths_path):
        with open(maths_path, "rb") as file:
            st.download_button(
                label="📁 गणित पेपर",
                data=file,
                file_name="Maths_SSC_Paper.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.caption("⏳ गणित पीडीएफ लवकरच येत आहे...")

# ३. विज्ञान पेपर डाऊनलोड
with col3:
    science_path = "papers/2026.pdf"
    if os.path.exists(science_path):
        with open(science_path, "rb") as file:
            st.download_button(
                label="📁 विज्ञान पेपर",
                data=file,
                file_name="Science_SSC_Paper.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.caption("⏳ विज्ञान पीडीएफ लवकरच येत आहे...")

st.markdown("---")

# =========================================================================
# 📊 AI विश्लेषण विभाग
# =========================================================================
uploaded_files = st.file_uploader("विश्लेषण करण्यासाठी प्रश्नपत्रिकांच्या PDF फाईल्स इथे अपलोड करा", type=["pdf"], accept_multiple_files=True)

if st.button("📊 महा-विश्लेषण सुरू करा"):
    if not uploaded_files:
        st.warning("⚠️ कृपया आधी किमान १ किंवा २ PDF फाईल्स अपलोड करा!")
    else:
        with st.spinner("🧠 AI एजंट सर्व स्कॅन पेपर्स आणि इमेजेसचे विश्लेषण करत आहे..."):
            contents_payload = []
            
            for uploaded_file in uploaded_files:
                file_bytes = uploaded_file.read()
                media_part = types.Part.from_bytes(
                    data=file_bytes,
                    mime_type="application/pdf"
                )
                contents_payload.append(media_part)
            
            prompt = (
                "तुम्ही महाराष्ट्र बोर्डाच्या दहावीच्या विद्यार्थ्यांसाठी एक तज्ज्ञ मार्गदर्शक आहात. "
                "दिलेल्या सर्व प्रश्नपत्रिकांच्या स्कॅन कॉपीज किंवा डिजिटल पीडीएफ काळजीपूर्वक पहा आणि वाचा. "
                "या प्रश्नपत्रिका कोणत्या विषयाच्या आहेत ते ओळखा आणि वारंवार येणारे प्रश्न, "
                "गुणविभागणीनुसार महत्त्वाची प्रकरणे, आणि बोर्ड परीक्षेत उत्तम गुण मिळवण्यासाठीची रणनीती मराठीत सखोल सांगा."
            )
            contents_payload.append(prompt)
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents_payload
            )
            
            st.success("🎉 विश्लेषण पूर्ण झाले!")
            st.markdown("### 🌟 AI एजंटचे महा-विश्लेषण 🌟")
            st.write(response.text)
