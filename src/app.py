import os
import PyPDF2
import streamlit as st
from groq import Groq

# Configure page
st.set_page_config(
    page_title="ATS Resume Expert",
    page_icon="📄",
    layout="wide"
)

# Initialize Groq client from secrets
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_API_KEY)
except (KeyError, AttributeError) as e:
    st.error("❌ Error: API key not configured in secrets. Please contact the administrator.")
    st.stop()

# Header
st.title("📝 ATS Resume Expert")
st.write("Optimize your resume for Applicant Tracking Systems")

# Sidebar - Configuration
with st.sidebar:
    st.success("✅ Secure API configuration active")
    
    st.header("ℹ️ How It Works")
    st.write("""
    1. 📋 Enter Job Description (optional)
    2. 📤 Upload Your Resume (PDF)
    3. 🔍 Choose Analysis Type:
       - **Resume Evaluation**: Get detailed feedback
       - **Compare with Sample**: See ideal format comparison
    """)

# Main content
SAMPLE_RESUME_PATH = r"Reference Resume- Fresher.pdf"  

# File upload section
st.header("📁 Upload Your Resume")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    st.success("✅ Resume uploaded successfully!")

# Job description section
st.header("📄 Job Description (Optional)")
input_text = st.text_area(
    "Paste the job description here:",
    placeholder="Enter job description for tailored feedback..."
)

# Analysis options
st.header("🔎 Analysis Options")
col1, col2 = st.columns(2)
with col1:
    analyze_btn = st.button("🔍 Analyze Resume or Compare With Given JD")
with col2:
    compare_btn = st.button("🔄 Compare with Sample Resume")

def extract_text_from_pdf(pdf_path_or_file):
    text = ""
    if isinstance(pdf_path_or_file, str):  
        with open(pdf_path_or_file, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    else:  
        pdf_reader = PyPDF2.PdfReader(pdf_path_or_file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return text[:5000]

def get_groq_response(input_text, pdf_text, prompt):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": input_text},
        {"role": "user", "content": pdf_text}
    ]
    try:
        completion = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=messages,
            temperature=0.1,
            max_tokens=8192,
            top_p=0.9
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Response handling
if analyze_btn or compare_btn:
    if not uploaded_file:
        st.error("❌ Please upload your resume first")
        st.stop()
    
    with st.spinner("🔍 Analyzing..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
        
        if analyze_btn:
            st.header("📊 Analysis Results")
            prompt = """You are an experienced Technical HR Manager. Provide detailed evaluation:
            1. ATS Score (0-100) with explanation
            2. Key strengths
            3. Areas for improvement
            4. Specific recommendations
            5. Match % with job description (if provided)"""
            response = get_groq_response(input_text, pdf_text, prompt)
            st.write(response)
        
        elif compare_btn:
            if not os.path.exists(SAMPLE_RESUME_PATH):
                st.error("❌ Sample resume file not found")
                st.stop()
                
            st.header("🆚 Comparison Results")
            sample_text = extract_text_from_pdf(SAMPLE_RESUME_PATH)
            prompt = """Compare the uploaded resume with sample resume:
            1. ATS Score comparison
            2. Missing sections
            3. Formatting differences
            4. Content improvements
            5. Actionable checklist"""
            response = get_groq_response(
                f"Sample Resume:\n{sample_text}\n\nUploaded Resume:\n{pdf_text}",
                "",
                prompt
            )
            st.write(response)

# Footer
st.write("---")
st.write("© ATS Resume Expert | Powered by Groq AI")