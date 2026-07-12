import streamlit as st
import google.genai as genai
from google.genai import types
import os

# १. वेबसाईटचे प्रीमियम सेटिंग्ज
st.set_page_config(
    page_title="SSC AI Paper Analyzer", 
    page_icon="📚", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- प्रिमियम एज्युकेशनल डिझाईन आणि टायपोग्राफी (Custom CSS) ---
st.markdown("""
<style>
    /* मुख्य बॅकग्राउंड आणि फॉन्ट सुधारणा */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* मुख्य टायटल डिझाईन */
    .main-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #1E3A8A;
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
        line-height: 1.2;
    }
    .sub-title {
        color: #3B82F6;
        font-size: 20px;
        font-weight: 600;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* व्हॅल्यू प्रॉपोझिशन (Value Proposition Box) ची प्रिमियम टायपोग्राफी */
    .vp-container {
        background-color: #F8FAFC;
        border-left: 5px solid #3B82F6;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 35px;
    }
    .vp-header {
        color: #0F172A;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 15px;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 10px;
    }
    .vp-item {
        font-size: 16px;
        color: #334155;
        line-height: 1.6;
        margin-bottom: 12px;
        display: flex;
        align-items: flex-start;
    }
    .vp-icon {
        margin-right: 12px;
        font-size: 18px;
        margin-top: 2px;
    }
    .vp-text strong {
        color: #1E3A8A;
        font-weight: 600;
    }
</style>
""", unsafe_allow_index=True)

# २. मुख्य युझर इंटरफेस (UI)
st.markdown('<div class="main-title">📚 १० वी महाराष्ट्र बोर्ड</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI सर्व-विषय प्रश्नपत्रिका विश्लेषक</div>', unsafe_allow_html=True)

# ३. प्रिमियम टायपोग्राफीसह व्हॅल्यू प्रॉपोझिशन कॉलम
st.markdown("""
<div class="vp-container">
    <div class="vp-header">🎯 हे Advanced AI टूल तुमच्या अभ्यासाचा पॅटर्न कसे बदलेल?</div>
    <div class="vp-item">
        <span class="vp-icon">⚡</span>
        <span class="vp-text"><strong>वेळेची १००% बचत:</strong> इंटरनेटवर मागील वर्षांचे पेपर्स शोधण्यात वेळ घालवणे थांबवा. सर्व अधिकृत पेपर्स आता एकाच ठिकाणी उपलब्ध आहेत.</span>
    </div>
    <div class="vp-item">
        <span class="vp-icon">🧠</span>
        <span class="vp-text"><strong>Imp प्रश्नांचा शोध:</strong> बोर्ड परीक्षेत कोणते प्रश्न वारंवार रिपीट होतात, हे आमचे ऍडव्हान्स जेमिनी AI मॉडेल एका सेकंदात अचूक शोधून देते.</span>
    </div>
    <div class="vp-item">
        <span class="vp-icon">📈</span>
        <span class="vp-text"><strong>तज्ज्ञ रणनीती व गुणविभागणी:</strong> कोणत्या धड्याला किती वेटेज आहे आणि टॉपर मुलांसारखे उत्तर कसे लिहायचे, याचे सखोल मार्गदर्शन थेट मातृभाषेत (मराठीत) मिळवा.</span>
    </div>
    <div class="vp-item">
        <span class="vp-icon">📥</span>
        <span class="vp-text"><strong>वन-क्लिक डायरेक्ट डाऊनलोड:</strong> कोणतीही जाहिरात किंवा गुगल ड्राईव्हच्या त्रासाशिवाय वर्षानुसार अधिकृत पेपर्स थेट तुमच्या गॅलरीत डाऊनलोड करा.</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("👇 खालील विभागातून प्रश्नपत्रिका डाऊनलोड करा किंवा तुमच्या फाईल्स अपलोड करून **महा-विश्लेषण** सुरू करा:")

# जेमिनी API की सुरक्षितपणे मिळवणे
MY_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=MY_API_KEY)

# =========================================================================
# 📥 वर्षानुसार सर्व-विषय पीडीएफ डाऊनलोड विभाग (All 6 Subjects)
# =========================================================================
st.markdown("---")
st.subheader("📥 अधिकृत प्रश्नपत्रिका वर्षानुसार डाऊनलोड करा")

# विषय १: मराठी
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
        st.caption("⏳ इतर वर्षांचे पेपर्स लवकरच येथे येतील...")

# विषय २: इंग्रजी
with st.expander("📁 २. इंग्रजी प्रश्नपत्रिका (English Papers)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        p_english_2026 = "papers/english_2026.pdf"
        if os.path.exists(p_english_2026):
            with open(p_english_2026, "rb") as file:
                st.download_button("📄 २०२६ इंग्रजी paper", data=file, file_name="English_2026.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.caption("⏳ २०२६ पेपर लवकरच येईल...")
    with col2:
        st.caption("⏳ इतर वर्षांचे पेपर्स लवकरच येथे येतील...")

# विषय ३: हिंदी
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
        st.caption("⏳ इतर वर्षांचे पेपर्स लवकरच येथे येतील...")

# विषय ४: गणित (भाग १ आणि २)
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

# विषय ५: विज्ञान (भाग १ आणि २)
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
        p_science_2026 = "papers/2026.pdf"
        if os.path.exists(p_science_2026):
            with open(p_science_2026, "rb") as file:
                st.download_button("📄 २०२६ विज्ञान भाग-२", data=file, file_name="Science_Part2_2026.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.caption("⏳ २०२६ विज्ञान भाग-२ लवकरच येईल...")

# विषय ६: समाजशास्त्र
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
        st.caption("⏳ इतर वर्षांचे पेपर्स लवकरच येथे येतील...")

st.markdown("---")

# =========================================================================
# 📊 AI विश्लेषण विभाग
# =========================================================================
st.subheader("📊 AI प्रश्नपत्रिका महा-विश्लेषण")
uploaded_files = st.file_uploader("विश्लेषण करण्यासाठी प्रश्नपत्रिकांच्या PDF फाईल्स इथे अपलोड करा (स्कॅन कॉपी देखील चालेल)", type=["pdf"], accept_multiple_files=True)

if st.button("📊 महा-विश्लेषण सुरू करा", use_container_width=True):
    if not uploaded_files:
        st.warning("⚠️ कृपया आधी किमान १ किंवा २ PDF फाईल्स अपलोड करा!")
    else:
        with st.spinner("🧠 आमचे AI एजंट सर्व पेपर्स वाचून सखोल अहवाल तयार करत आहे..."):
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
            
            st.success("🎉 विश्लेषण यशस्वीरीत्या पूर्ण झाले!")
            st.markdown("### 🌟 AI एजंटचे महा-विश्लेषण अहवाल 🌟")
            st.write(response.text)
