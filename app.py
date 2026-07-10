import streamlit as st
import google.genai as genai
from google.genai import types

st.set_page_config(page_title="SSC AI Paper Analyzer", page_icon="📚", layout="centered")

st.title("📚 १० वी महाराष्ट्र बोर्ड - AI सर्व-विषय प्रश्नपत्रिका विश्लेषक")
st.write("मागील वर्षांच्या कोणत्याही विषयाच्या प्रश्नपत्रिका एकत्र अपलोड करा आणि जेमिनी AI कडून महा-विश्लेषण मिळवा!")

# स्ट्रीमलिटच्या सुरक्षित तिजोरीतून की मिळवणे
MY_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=MY_API_KEY)

# --- पेमेंट सेक्शन (Payment Section) ---
st.markdown("---")
st.subheader("🔑 प्रीमियम ॲक्सेस (Premium Access)")
st.write("हे ॲप वापरण्यासाठी कृपया **₹४९** चे पेमेंट करा आणि ॲक्सेस मिळवा.")

# तुमचा UPI ID इथे टाका (उदा. तुमच्या गुगलपे/फोनपे चा आयडी)
st.info("💡 **UPI ID वर पेमेंट करा:** `rushichavan239@oksbi`
st.write("किंवा तुमच्या मोबाईलमधील कोणत्याही ॲपने (GPay, PhonePe, Paytm) स्कॅन करून पेमेंट करा.")

# पेमेंट केल्यानंतर व्हेरिफिकेशनसाठी पासवर्ड विचारणे
access_key = st.text_input("पेमेंट केल्यानंतर मिळालेला 'Access Key' किंवा 'Transaction ID' इथे टाका:", type="password")
st.markdown("---")

# फाईल अपलोडर
uploaded_files = st.file_uploader("तुमच्या प्रश्नपत्रिकांच्या PDF फाईल्स इथे अपलोड करा", type=["pdf"], accept_multiple_files=True)

if st.button("📊 महा-विश्लेषण सुरू करा"):
    # आधी पासवर्ड/की तपासणे (हा पासवर्ड तुम्ही खाली स्ट्रीमलिट सिक्रेट्समध्ये सेट करणार आहात)
    if access_key != st.secrets["APP_ACCESS_KEY"]:
        st.error("❌ चुकीचा Access Key/Transaction ID! कृपया आधी पेमेंट करा किंवा योग्य की टाका.")
    elif not uploaded_files:
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
