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
# 📥 वर्षानुसार पीडीएफ डाऊनलोड विभाग (Year-wise PDF Download Section)
# =========================================================================
st.markdown("---")
st.subheader("📥 मागील वर्षांच्या प्रश्नपत्रिका वर्षानुसार डाऊनलोड करा")
st.write("खालील बटणावर क्लिक करून तुम्ही २०२६ चा विज्ञान पेपर थेट डाऊनलोड करू शकता:")

# विज्ञान विषयासाठी डाऊनलोड बॉक्स
with st.expander("📁 विज्ञान प्रश्नपत्रिका (Science Papers)", expanded=True):
    col1, col2, col3 = st.columns(3)
    
    # २०२६ चा विज्ञान पेपर (नवीन पाथनुसार)
    with col1:
        science_2026_path = "papers/2026.pdf"
        if os.path.exists(science_2026_path):
            with open(science_2026_path, "rb") as file:
                st.download_button(
                    label="📄 २०२६ विज्ञान पेपर",
                    data=file,
                    file_name="Science_2026_Paper.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.caption("⏳ २०२६ विज्ञान पेपर लवकरच येईल...")
            
    # भविष्यात इतर वर्षे जोडण्यासाठी मोकळी जागा
    with col2:
        st.caption("⏳ इतर पेपर्स लवकरच येतील...")
    with col3:
        st.caption("⏳ इतर पेपर्स लवकरच येतील...")

st.markdown("---")

# =========================================================================
# 📊 AI विश्लेषण विभाग (स्कॅन केलेल्या आणि डिजिटल फाईल्ससाठी)
# =========================================================================
uploaded_files = st.file_uploader("विश्लेषण करण्यासाठी प्रश्नपत्रिकांच्या PDF फाईल्स इथे अपलोड करा", type=["pdf"], accept_multiple_files=True)

if st.button("📊 महा-विश्लेषण सुरू करा"):
    if not uploaded_files:
        st.warning("⚠️ कृपया आधी किमान १ किंवा २ PDF फाईल्स अपलोड करा!")
    else:
        with st.spinner("🧠 AI एजंट सर्व स्कॅन पेपर्स आणि इमेजेसचे विश्लेषण करत आहे..."):
            contents_payload = []
            
            # सर्व अपलोड केलेल्या फाईल्स जेमिनीसाठी तयार करणे
            for uploaded_file in uploaded_files:
                file_bytes = uploaded_file.read()
                media_part = types.Part.from_bytes(
                    data=file_bytes,
                    mime_type="application/pdf"
                )
                contents_payload.append(media_part)
            
            # मुख्य सूचना (Prompt)
            prompt = (
                "तुम्ही महाराष्ट्र बोर्डाच्या दहावीच्या विद्यार्थ्यांसाठी एक तज्ज्ञ मार्गदर्शक आहात. "
                "दिलेल्या सर्व प्रश्नपत्रिकांच्या स्कॅन कॉपीज किंवा डिजिटल पीडीएफ काळजीपूर्वक पहा आणि वाचा. "
                "या प्रश्नपत्रिका कोणत्या विषयाच्या आहेत ते ओळखा आणि वारंवार येणारे प्रश्न, "
                "गुणविभागणीनुसार महत्त्वाची प्रकरणे, आणि बोर्ड परीक्षेत उत्तम गुण मिळवण्यासाठीची रणनीती मराठीत सखोल सांगा."
            )
            contents_payload.append(prompt)
            
            # जेमिनी मॉडेलकडून उत्तर मिळवणे
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents_payload
            )
            
            st.success("🎉 विश्लेषण पूर्ण झाले!")
            st.markdown("### 🌟 AI एजंटचे महा-विश्लेषण 🌟")
            st.write(response.text)
