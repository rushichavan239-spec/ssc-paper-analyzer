import streamlit as st
import google.genai as genai
import pdfplumber

st.set_page_config(page_title="SSC AI Paper Analyzer", page_icon="📚", layout="centered")
st.title("📚 १० वी महाराष्ट्र बोर्ड - AI सर्व-विषय प्रश्नपत्रिका विश्लेषक")
st.write("मागील वर्षांच्या कोणत्याही विषयाच्या प्रश्नपत्रिका (PDF) एकत्र अपलोड करा आणि जेमिनी AI कडून विश्लेषण मिळवा!")

MY_API_KEY = "AQ.Ab8RN6J5N2HpehyTUKcK57FhXSq1omH1z62WiCV6DVBu29jkDg"
client = genai.Client(api_key=MY_API_KEY)

uploaded_files = st.file_uploader("तुमच्या प्रश्नपत्रिकांच्या PDF फाईल्स इथे अपलोड करा", type=["pdf"], accept_multiple_files=True)

if st.button("📊 महा-विश्लेषण सुरू करा"):
    if not uploaded_files:
        st.warning("⚠️ कृपया आधी किमान १ किंवा २ PDF फाईल्स अपलोड करा!")
    else:
        with st.spinner("🧠 AI सर्व प्रश्नपत्रिका वाचून विषयाचे विश्लेषण करत आहे..."):
            all_text = ""
            for uploaded_file in uploaded_files:
                with pdfplumber.open(uploaded_file) as pdf:
                    all_text += f"\n\n=== प्रश्नपत्रिका: {uploaded_file.name} ===\n"
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text: all_text += text + "\n"
            
            prompt = f"तुम्ही महाराष्ट्र बोर्डाच्या दहावीच्या विद्यार्थ्यांसाठी एक तज्ज्ञ मार्गदर्शक आहात. खालील प्रश्नपत्रिकांचा मजकूर वाचा, विषय ओळखा आणि वारंवार येणारे प्रश्न, महत्त्वाची प्रकरणे, आणि रणनीती मराठीत सखोल सांगा:\n\nडेटा:\n{all_text}"
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            st.success("🎉 विश्लेषण पूर्ण झाले!")
            st.markdown("### 🌟 AI एजंटचे महा-विश्लेषण 🌟")
            st.write(response.text)
