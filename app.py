import os

import streamlit as st
import google.genai as genai
from google.genai import types

# =============================================================================
# 1. PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="SSC AI Paper Analyzer",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# 2. PREMIUM DESIGN SYSTEM — CSS INJECTION
#    Apple / Vercel inspired. Fully theme-aware (light + dark), token-driven.
# =============================================================================
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* -------------------------------------------------------------------
       DESIGN TOKENS — Light mode defaults, overridden below for dark mode
    ------------------------------------------------------------------- */
    :root {
        --bg-primary: #FFFFFF;
        --bg-canvas: #FFFFFF;
        --text-primary: #0F172A;
        --text-secondary: #475569;
        --text-tertiary: #64748B;
        --accent: #2563EB;
        --accent-soft: rgba(37, 99, 235, 0.08);
        --accent-soft-strong: rgba(37, 99, 235, 0.14);
        --border-color: #E2E8F0;
        --border-soft: rgba(15, 23, 42, 0.06);
        --card-bg: rgba(255, 255, 255, 0.72);
        --card-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.05), 0 8px 10px -6px rgba(15, 23, 42, 0.03);
        --input-bg: #F8FAFC;
        --success-bg: #ECFDF5;
        --success-text: #047857;
        --success-border: #A7F3D0;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #0B0F19;
            --bg-canvas: #0B0F19;
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
            --text-tertiary: #64748B;
            --accent: #60A5FA;
            --accent-soft: rgba(96, 165, 250, 0.10);
            --accent-soft-strong: rgba(96, 165, 250, 0.18);
            --border-color: #1E293B;
            --border-soft: rgba(248, 250, 252, 0.07);
            --card-bg: rgba(17, 24, 39, 0.65);
            --card-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.35), 0 8px 10px -6px rgba(0, 0, 0, 0.25);
            --input-bg: #111827;
            --success-bg: rgba(16, 185, 129, 0.08);
            --success-text: #34D399;
            --success-border: rgba(52, 211, 153, 0.25);
        }
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* Force Background globally on all Streamlit container layers */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stMainBlockContainer"],
    [data-testid="stMain"],
    [data-testid="stBottomBlockContainer"],
    body {
        background-color: var(--bg-canvas) !important;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 4rem;
        max-width: 760px;
    }

    /* -------------------------------------------------------------------
       HEADER
    ------------------------------------------------------------------- */
    .brand-badge-wrap {
        display: flex;
        justify-content: center;
        margin-bottom: 22px;
    }
    .brand-badge {
        background: var(--accent-soft);
        color: var(--accent);
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding: 7px 18px;
        border-radius: 100px;
        border: 1px solid var(--accent-soft-strong);
        display: inline-block;
    }

    .main-title {
        color: var(--text-primary);
        font-size: 44px;
        font-weight: 800;
        letter-spacing: -0.8px;
        line-height: 1.15;
        margin-bottom: 10px;
        text-align: center;
    }

    .sub-title {
        color: var(--text-secondary);
        font-size: 18px;
        font-weight: 500;
        line-height: 1.6;
        margin-bottom: 40px;
        text-align: center;
        max-width: 560px;
        margin-left: auto;
        margin-right: auto;
    }

    /* -------------------------------------------------------------------
       GLASSMORPHIC VALUE-PROP CARD
    ------------------------------------------------------------------- */
    .vp-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        padding: 30px 32px;
        border-radius: 20px;
        box-shadow: var(--card-shadow);
        margin-bottom: 40px;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    }
    .vp-title {
        color: var(--text-primary);
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 20px;
        letter-spacing: -0.2px;
    }
    .vp-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .vp-list-item {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        font-size: 15px;
        color: var(--text-secondary);
        line-height: 1.65;
        margin-bottom: 16px;
    }
    .vp-list-item:last-child {
        margin-bottom: 0;
    }
    .vp-check {
        flex: 0 0 auto;
        width: 20px;
        height: 20px;
        margin-top: 2px;
        border-radius: 6px;
        background: var(--accent-soft);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .vp-check svg {
        width: 12px;
        height: 12px;
    }
    .vp-list-item strong {
        color: var(--text-primary);
        font-weight: 650;
    }

    /* -------------------------------------------------------------------
       SECTION HEADINGS
    ------------------------------------------------------------------- */
    .section-head {
        color: var(--text-primary);
        font-size: 24px;
        font-weight: 700;
        margin-top: 36px;
        margin-bottom: 16px;
        letter-spacing: -0.3px;
    }
    .section-subtext {
        color: var(--text-tertiary);
        font-size: 14.5px;
        margin-bottom: 18px;
        line-height: 1.6;
    }

    /* -------------------------------------------------------------------
       EXPANDER (SUBJECT CONTAINERS) — premium collapsible list items
    ------------------------------------------------------------------- */
    .stExpander {
        border: 1px solid var(--border-color) !important;
        border-radius: 14px !important;
        background: var(--card-bg) !important;
        backdrop-filter: blur(10px);
        margin-bottom: 12px !important;
        overflow: hidden;
        transition: all 0.25s ease;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.02);
    }
    .stExpander:hover {
        border-color: var(--accent) !important;
        box-shadow: 0 8px 20px -8px rgba(37, 99, 235, 0.18);
    }
    .stExpander summary {
        padding: 18px 20px !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        font-size: 15px !important;
    }
    .stExpander [data-testid="stExpanderDetails"] {
        padding: 6px 20px 20px 20px !important;
    }

    /* -------------------------------------------------------------------
       CAPTION / PENDING STATE
    ------------------------------------------------------------------- */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: var(--text-tertiary) !important;
    }

    /* -------------------------------------------------------------------
       DOWNLOAD BUTTONS
    ------------------------------------------------------------------- */
    .stDownloadButton button {
        border-radius: 12px !important;
        border: 1px solid var(--border-color) !important;
        background: var(--input-bg) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        padding: 10px 16px !important;
        transition: all 0.25s ease !important;
    }
    .stDownloadButton button:hover {
        border-color: var(--accent) !important;
        color: var(--accent) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px -6px rgba(37, 99, 235, 0.35);
    }

    /* -------------------------------------------------------------------
       FILE UPLOADER
    ------------------------------------------------------------------- */
    [data-testid="stFileUploaderDropzone"] {
        background: var(--input-bg) !important;
        border: 1.5px dashed var(--border-color) !important;
        border-radius: 16px !important;
        transition: all 0.25s ease !important;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--accent) !important;
        background: var(--accent-soft) !important;
    }

    /* -------------------------------------------------------------------
       PRIMARY CTA BUTTON
    ------------------------------------------------------------------- */
    .stButton button {
        border-radius: 12px !important;
        border: none !important;
        background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        padding: 14px 20px !important;
        letter-spacing: -0.1px;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 20px -8px rgba(37, 99, 235, 0.45);
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 28px -8px rgba(37, 99, 235, 0.55);
        filter: brightness(1.05);
    }
    .stButton button:active {
        transform: translateY(0);
    }

    @media (prefers-color-scheme: dark) {
        .stButton button {
            background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
        }
    }

    /* -------------------------------------------------------------------
       ALERTS
    ------------------------------------------------------------------- */
    [data-testid="stAlert"] {
        border-radius: 14px !important;
        border: 1px solid var(--border-color) !important;
    }

    hr {
        border-color: var(--border-color) !important;
        opacity: 0.6;
    }
</style>
""",
    unsafe_allow_html=True,
)


def check_svg() -> str:
    """Returns a crisp inline SVG checkmark that inherits the accent color via currentColor."""
    return (
        '<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">'
        '<path d="M5 13L9 17L19 7" stroke="var(--accent)" stroke-width="2.5" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>'
    )


# =============================================================================
# 3. HEADER
# =============================================================================
st.markdown('<div class="brand-badge-wrap"><div class="brand-badge">✨ Next-Gen AI Learning</div></div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">१० वी महाराष्ट्र बोर्ड</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-संचलित सर्व-विषय प्रश्नपत्रिका विश्लेषक</div>', unsafe_allow_html=True)

# =============================================================================
# 4. VALUE PROPOSITION CARD
# =============================================================================
vp_items = [
    ("वेळेची १००% बचत", "इंटरनेटवर विखुरलेले पेपर्स शोधण्यात वेळ वाया घालवू नका. सर्व अधिकृत पेपर्स आता एकाच ठिकाणी स्ट्रक्चर्ड फॉरमॅटमध्ये उपलब्ध आहेत."),
    ("Imp प्रश्नांचे अचूक वर्गीकरण", "Board परीक्षेत वारंवार रिपीट होणारे प्रश्न आमचे ऍडव्हान्स जेमिनी AI मॉडेल एका क्लिकवर अचूक शोधून देते."),
    ("प्रकरणांनुसार गुणविभागणी", "कोणत्या धड्यावर किती गुणांचे प्रश्न येतात आणि उत्तर लिहिण्याची योग्य पद्धत काय, याचे सखोल विश्लेषण थेट मराठीत मिळवा."),
    ("जाहिरातमुक्त डायरेक्ट डाऊनलोड", "कोणत्याही गुगल ड्राईव्ह किंवा पॉप-अप जाहिरातींशिवाय वर्षानुसार प्रश्नपत्रिका थेट डिव्हाइसवर डाऊनलोड करा."),
]

vp_html = '<div class="vp-card"><div class="vp-title">🎯 हे टूल तुमच्या अभ्यासाची रणनीती कशी बदलेल?</div><ul class="vp-list">'
for title, desc in vp_items:
    vp_html += (
        f'<li class="vp-list-item"><span class="vp-check">{check_svg()}</span>'
        f'<span><strong>{title}:</strong> {desc}</span></li>'
    )
vp_html += "</ul></div>"

st.markdown(vp_html, unsafe_allow_html=True)

# =============================================================================
# 5. GEMINI CLIENT INITIALIZATION
# =============================================================================
MY_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=MY_API_KEY)

# =============================================================================
# 6. OFFICIAL QUESTION PAPERS — DOWNLOAD SECTION (6 SUBJECTS)
# =============================================================================
st.markdown('<div class="section-head">📥 अधिकृत प्रश्नपत्रिका वर्षानुसार डाऊनलोड करा</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtext">विषय निवडा आणि उपलब्ध वर्षाची प्रश्नपत्रिका थेट डाऊनलोड करा.</div>', unsafe_allow_html=True)


def render_download(path: str, label: str, file_name: str) -> None:
    """Renders a download button if the file exists, otherwise a pending caption."""
    if os.path.exists(path):
        with open(path, "rb") as file:
            st.download_button(
                label,
                data=file,
                file_name=file_name,
                mime="application/pdf",
                use_container_width=True,
            )
    else:
        st.caption("⏳ पेपर लवकरच येईल...")


# विषय १: मराठी
with st.expander("📁 १. मराठी प्रश्नपत्रिका (Marathi)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        render_download("papers/marathi_2026.pdf", "📄 २०२६ मराठी पेपर", "Marathi_2026.pdf")
    with col2:
        st.caption("⏳ इतर वर्षांचे पेपर्स लवकरच येतील...")

# विषय २: इंग्रजी
with st.expander("📁 २. इंग्रजी प्रश्नपत्रिका (English)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        render_download("papers/english_2026.pdf", "📄 २०२६ इंग्रजी पेपर", "English_2026.pdf")
    with col2:
        st.caption("⏳ इतर वर्षांचे पेपर्स लवकरच येतील...")

# विषय ३: हिंदी
with st.expander("📁 ३. हिंदी प्रश्नपत्रिका (Hindi)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        render_download("papers/hindi_2026.pdf", "📄 २०२६ हिंदी पेपर", "Hindi_2026.pdf")
    with col2:
        st.caption("⏳ इतर वर्षांचे पेपर्स लवकरच येतील...")

# विषय ४: गणित (भाग १ आणि २)
with st.expander("📁 ४. गणित प्रश्नपत्रिका - भाग १ व २ (Mathematics)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        render_download("papers/maths1_2026.pdf", "📄 २०२६ गणित भाग-१", "Maths_Part1_2026.pdf")
    with col2:
        render_download("papers/maths2_2026.pdf", "📄 २०२६ गणित भाग-२", "Maths_Part2_2026.pdf")

# विषय ५: विज्ञान (भाग १ आणि २)
with st.expander("📁 ५. विज्ञान प्रश्नपत्रिका - भाग १ व २ (Science)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        render_download("papers/science1_2026.pdf", "📄 २०२६ विज्ञान भाग-१", "Science_Part1_2026.pdf")
    with col2:
        render_download("papers/2026.pdf", "📄 २०२६ विज्ञान भाग-२", "Science_Part2_2026.pdf")

# विषय ६: समाजशास्त्र
with st.expander("📁 ६. समाजशास्त्र प्रश्नपत्रिका (Social Science)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        render_download("papers/social_2026.pdf", "📄 २०२६ समाजशास्त्र पेपर", "SocialScience_2026.pdf")
    with col2:
        st.caption("⏳ इतर वर्षांचे पेपर्स लवकरच येतील...")

# =============================================================================
# 7. AI MEGA-ANALYSIS SECTION
# =============================================================================
st.markdown('<div class="section-head">📊 AI प्रश्नपत्रिका महा-विश्लेषण</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtext">तुमच्या प्रश्नपत्रिकांची PDF अपलोड करा आणि आमचे AI एजंट क्षणार्धात सखोल अहवाल तयार करेल.</div>',
    unsafe_allow_html=True,
)

uploaded_files = st.file_uploader(
    "तुमच्या प्रश्नपत्रिकांच्या पीडीएफ (किंवा स्कॅन कॉपी) इथे अपलोड करा:",
    type=["pdf"],
    accept_multiple_files=True,
)

ANALYSIS_PROMPT = (
    "तुम्ही महाराष्ट्र board चे दहावीचे तज्ज्ञ शिक्षक आहात. "
    "दिलेल्या सर्व प्रश्नपत्रिकांच्या स्कॅन किंवा digital फाईल्स व्यवस्थित वाचा. "
    "या पेपर्सचा नेमका विषय ओळखून त्यातील महत्त्वाचे प्रश्न, प्रकरणांनुसार गुणविभागणी "
    "आणि board परीक्षेत जास्तीत जास्त गुण मिळवण्यासाठी कोणती रणनीती अवलंबावी, हे मराठीत सविस्तर सांगा."
)

if st.button("📊 महा-विश्लेषण सुरू करा", use_container_width=True):
    if not uploaded_files:
        st.warning("⚠️ कृपया आधी किमान १ किंवा २ PDF फाईल्स अपलोड करा!")
    else:
        with st.spinner("🧠 आमचे AI एजंट सर्व पेपर्स वाचून सखोल अहवाल तयार करत आहे..."):
            try:
                contents_payload = []

                for uploaded_file in uploaded_files:
                    file_bytes = uploaded_file.read()
                    media_part = types.Part.from_bytes(
                        data=file_bytes,
                        mime_type="application/pdf",
                    )
                    contents_payload.append(media_part)

                contents_payload.append(ANALYSIS_PROMPT)

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents_payload,
                )

                st.success("🎉 विश्लेषण यशस्वीरीत्या पूर्ण झाले!")
                st.markdown("### 🌟 AI एजंटचे महा-विश्लेषण अहवाल 🌟")
                st.write(response.text)

            except Exception as exc:  # noqa: BLE001
                st.error(f"❌ विश्लेषण करताना त्रुटी आली: {exc}")
