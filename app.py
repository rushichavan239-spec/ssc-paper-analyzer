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

# --- डार्क आणि लाईट थीम दोन्हीसाठी युनिव्हर्सल प्रिमियम CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main .block-container {
        font-family: 'Inter', -apple-system, sans-serif;
        padding-top: 2.5rem;
        padding-bottom: 2.5rem;
        max-width: 720px;
    }
    
    /* मुख्य टायटल - डार्क थीमनुसार बदलणारा रंग */
    .brand-badge {
        background-color: rgba(37, 99, 235, 0.1);
        color: #3B82F6;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding: 6px 16px;
        border-radius: 100px;
        display: inline-block;
        margin-bottom: 15px;
    }
    
    /* मुख्य हेडर्स - डार्क आणि लाईट दोन्हीमध्ये चालणारे न्यूट्रल कलर्स */
    .main-title {
        color: #F8FAFC; /* डार्क मोडसाठी सुरक्षित पांढरा */
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -0.5px;
        line-height: 1.2;
        margin-bottom: 8px;
        text-align: center;
    }
    .sub-title {
        color: #94A3B8;
        font-size: 18px;
        font-weight: 500;
        line-height: 1.5;
        margin-bottom: 35px;
        text-align: center;
    }
    
    /* व्हॅल्यू कार्ड - जे डार्क बॅकग्राउंडवरही उठून दिसेल */
    .vp-card {
        background: rgba(30, 41, 59, 0.7); /* सेमी-ट्रान्सपरंट स्लेट */
        border: 1px solid #334155;
        padding: 26px;
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        margin-bottom: 35px;
        backdrop-filter: blur(5px);
    }
    .vp-title {
        color: #60A5FA; /* फिकट चमकदार निळा - डार्क मोडमध्ये बेस्ट दिसतो */
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 18px;
    }
    .vp-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .vp-list-item {
        font-size: 15px;
        color: #E2E8F0; /* वाचनीय फिकट करडा रंग */
        line-height: 1.6;
        margin-bottom: 14px;
        padding-left: 28px;
        position: relative;
    }
    .vp-list-item::before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #60A5FA;
        font-weight: 700;
        font-size: 16px;
    }
    .vp-list-item strong {
        color: #FFFFFF; /* महत्त्वाचे शब्द शुद्ध पांढऱ्या रंगात */
        font-weight: 650;
    }
    
    .section-head {
        color: #F1F5F9;
        font-size: 22px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 15px;
        letter-spacing: -0.3px;
    }

    /* जर युझरची सिस्टम लाईट मोडमध्ये असेल तर आपोआप खालील डिझाईन ऍक्टिव्हेट होईल */
    @media (prefers-color-scheme: light) {
        .main-title { color: #0F172A; }
        .sub-title { color: #475569; }
        .vp-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04);
        }
        .vp-title { color: #1E3A8A; }
        .vp-list-item { color: #475569; }
        .vp-list-item strong { color: #0F172A; }
        .section-head { color: #0F172A; }
    }
</style>
""", unsafe_allow_html=True)

# २. मुख्य युझर इंटरफेस (Header UI)
st.markdown('<center><div class="brand-badge">✨ Next-Gen AI Learning</div></center>', unsafe_allow_html=True)
st.markdown('<div class="main-title">१० वी महाराष्ट्र बोर्ड</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-संचलित सर्व-विषय प्रश्नपत्रिका विश्लेषक</div>', unsafe_allow_html=True)

# ३. प्रिमियम व्हॅल्यू प्रॉपोझिशन कार्ड
st.markdown("""
<div class="vp-card">
    <div class="vp-title">🎯 हे टूल तुमच्या अभ्यासाची रणनीती कशी बदलेल?</div>
    <ul class="vp-list">
        <li class="vp-list-item"><strong>वेळेची १००% बचत:</strong> इंटरनेटवर विखुरलेले पेपर्स शोधण्यात वेळ वाया घालवू नका. सर्व अधिकृत पेपर्स आता एकाच ठिकाणी स्ट्रक्चर्ड फॉरमॅटमध्ये उपलब्ध आहेत.</li>
        <li class="vp-list-item"><strong>Imp प्रश्नांचे अचूक वर्गीकरण:</strong> बोर्ड परीक्षेत वारंवार रिपीट होणारे प्रश्न आमचे ऍडव्हान्स जेमिनी AI मॉडेल एका क्लिकवर अचूक शोधून देते.</li>
        <li class="vp-list-item"><strong>प्रकरणांनुसार गुणविभागणी:</strong> कोणत्या धड्यावर किती गुणांचे प्रश्न येतात आणि उत्तर लिहिण्याची योग्य पद्धत काय, याचे सखोल विश्लेषण थेट मराठीत मिळवा.</li>
        <li class="vp-list-item"><strong>जाहिरातमुक्त डायरेक्ट डाऊनलोड:</strong> कोणत्याही गुगल ड्राईव्ह किंवा पॉप-अप जाहिरातींशिवाय वर्षानुसार प्रश्नपत्रिका थेट डिव्हाइसवर डाऊनलोड करा.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.write("📂 खालील ड्रापडाऊनमधून प्रश्नपत्रिका मिळवा किंवा फाईल्स अपलोड करून विश्लेषण सुरू करा:")

# जेमिनी API की सुरक्षितपणे मिळवणे
MY_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=MY_API_KEY)

# =========================================================================
# 📥 अधिकृत प्रश्नपत्रिका डाऊनलोड विभाग (All 6 Subjects)
# =========================================================================
st.markdown('<div class="section-head">📥 अधिकृत प्रश्नपत्रिका वर्षानुसार डाऊनलोड करा</div>', unsafe_allow_html=True)

# विषय १: मराठी
with st.expander("📁 १. मराठी प्रश्नपत्रिका (Marathi)", expanded=False):
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

# विषय २: इंग्रजी
with st.expander("📁 २. इंग्रजी प्रश्नपत्रिका (English)", expanded=False):
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

# विषय ३: हिंदी
with st.expander("📁 ३. हिंदी प्रश्नपत्रिका (Hindi)", expanded=False):
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

# विषय ४: गणित (भाग १ आणि २)
with st.expander("📁 ४. गणित प्रश्नपत्रिका - भाग १ व २ (Mathematics)", expanded=False):
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
with st.expander("📁 ५. विज्ञान प्रश्नपत्रिका - भाग १ व २ (Science)", expanded=False):
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
with st.expander("📁 ६. समाजशास्त्र प्रश्नपत्रिका (Social Science)", expanded=False):
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

# =========================================================================
# 📊 AI विश्लेषण विभाग
# =========================================================================
st.markdown('<div class="section-head">📊 AI प्रश्नपत्रिका महा-विश्लेषण</div>', unsafe_allow_html=True)
uploaded_files = st.file_uploader("तुमच्या प्रश्नपत्रिकांच्या पीडीएफ (किंवा स्कॅन कॉपी) इथे अपलोड करा:", type=["pdf"], accept_multiple_files=True)

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
                "दिलेल्या सर्व प्रश्नपत्रिकांच्या स्कॅन किंवा digital फाईल्स व्यवस्थित वाचा. "
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
