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
# 📥 वर्षानुसार सर्व-विषय पीडीएफ डाऊनलोड विभाग (All 6 Subjects Download Section)
# =========================================================================
st.markdown("---")
st.subheader("📥 मागील वर्षांच्या प्रश्नपत्रिका वर्षानुसार डाऊनलोड करा")
st.write("विषयावर क्लिक करून तुम्हाला हवे असलेल्या वर्षाचा पेपर थेट डाऊनलोड करा:")

# ----------------- विषय १: मराठी -----------------
with st.expander("📁 १. मराठी प्रश्नपत्रिका (Marathi Papers)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        p_marathi_2026 = "papers/marathi_2026.pdf"
        if os.path.exists(p_marathi_2026):
            with open(p_marathi_2026, "rb") as file:
                st.download_button("📄 २०२६ मराठी पेपर", data=file, file_name="Marathi_2026.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.caption("⏳ २०२६ पेपर लवकरच येईल...")
    with col2:
        st.caption("⏳ इतर वर्षांचे पेपर्स लवकरच येतील...")

# ----------------- विषय २: इंग्रजी -----------------
with st.expander("📁 २. इंग्रजी प्रश्नपत्रिका (English Papers)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        p_english_2026 = "papers/english_2026.pdf"
        if os.path.exists(p_english_2026):
            with open(p_english_2026, "rb") as file:
                st.download_button("📄 २०२६ इंग्रजी पेपर", data=file, file_name="English_2026.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.caption("⏳ २०२६ पेपर लवकरच येईल...")
    with col2:
        st.caption("⏳ इतर वर्षांचे पेपर्स लवकरच येतील...")

# ----------------- विषय ३: हिंदी -----------------
with st.expander("📁 ३. हिंदी प्रश्नपत्रिका (Hindi Papers)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        p_hindi_2026 = "papers/hindi_2026.pdf"
        if os.path.exists(p_hindi_2026):
            with open(p_hindi_2026, "rb") as file:
                st.download_button("📄 २०२६ हिंदी पेपर", data=file, file_name="Hindi_2026.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.caption("⏳ २०२६ पेपर लवकरच येईल...")
    with col2:
        st.caption("⏳ इतर वर्षांचे पेपर्स लवकरच येतील...")

# ----------------- विषय ४: गणित (भाग १ आणि २) -----------------
with st.expander("📁 ४. गणित प्रश्नपत्रिका - भाग १ व २ (Maths Papers)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        p_maths1_2026 = "papers/maths1_2026.pdf"
        if os.path.exists(p_maths1_2026):
            with open(p_maths1_2026, "rb") as file:
                st.download_button("📄 २०२६ गणित भाग-१", data=file, file_name="Maths_Part1_2026.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.caption("⏳ २०२६ गणित भाग-१ लवकरच येईल...")
    with col2:
        p_maths2_2026 = "papers/maths2_2026.pdf"
        if os.path.exists(p_maths2_2026):
            with open(p_maths2_2026, "rb") as file:
                st.download_button("📄 २०२६ गणित भाग-२", data=file, file_name="Maths_Part2_2026.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.caption("⏳ २०२६ गणित भाग-२ लवकरच येईल...")

# ----------------- विषय ५: विज्ञान (भाग १ आणि २) -----------------
with st.expander("📁 ५. विज्ञान प्रश्नपत्रिका - भाग १ व २ (Science Papers)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        p_science1_2026 = "papers/science1_2026.pdf"
        if os.path.exists(p_science1_2026):
            with open(p_science1_2026, "rb") as file:
                st.download_button("📄 २०२६ विज्ञान भाग-१", data=file, file_name="Science_Part1_2026.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.caption("⏳ २०२६ विज्ञान भाग-१ लवकरच येईल...")
    with col2:
        # तुमचा आधीचा मुख्य २०२६ चा विज्ञान पेपर
        p_science_2026 = "papers/2026.pdf"
        if os.path.exists(p_science_2026):
            with open(p_science_2026, "rb") as file:
                st.download_button("📄 २०२६ विज्ञान भाग-२", data=file, file_name="Science_Part2_2026.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.caption("⏳ २०२६ विज्ञान भाग-२ लवकरच येईल...")

# ----------------- विषय ६: समाजशास्त्र -----------------
with st.expander("📁 ६. समाजशास्त्र प्रश्नपत्रिका (Social Science Papers)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        p_social_2026 = "papers/social_2026.pdf"
        if os.path.exists(p_social_2026):
            with open(p_social_2026, "rb") as file:
                st.download_button("📄 २०२६ समाजशास्त्र पेपर", data=file, file_name="SocialScience_2026.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.caption("⏳ २०२६ पेपर लवकरच येईल...")
    with col2:
        st.caption("⏳ इतर वर्षांचे पेपर्स लवकरच येतील...")

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
                "तुम्ही महाराष्ट्र board चे दहावीचे तज्ज्ञ शिक्षक आहात. "
                "दिलेल्या सर्व प्रश्नपत्रिकांच्या स्कॅन किंवा डिजिटल फाईल्स व्यवस्थित वाचा. "
                "या पेपर्सचा नेमका विषय ओळखून त्यातील महत्त्वाचे प्रश्न, प्रकरणांनुसार गुणविभागणी "
                "आणि बोर्ड परीक्षेत जास्तीत जास्त गुण मिळवण्यासाठी कोणती रणनीती अवलंबावी, हे मराठीत सविस्तर सांगा."
            )
            contents_payload.append(prompt)
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents_payload
            )
            
            st.success("🎉 विश्लेषण पूर्ण झाले!")
            st.markdown("### 🌟 AI एजंटचे महा-विश्लेषण 🌟")
            st.write(response.text)
