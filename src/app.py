import os
import PyPDF2
import streamlit as st
from groq import Groq

# Configure page with mobile-friendly settings
st.set_page_config(
    page_title="ATS Resume Expert",
    page_icon="📄",
    layout="centered"
)

# Mobile-responsive CSS
st.markdown("""
<style>
    /* [Previous CSS styles remain exactly the same] */
</style>
""", unsafe_allow_html=True)

def initialize_groq_client():
    """Initialize Groq client with proper error handling"""
    try:
        if 'GROQ_API_KEY' not in st.secrets:
            raise KeyError("API key not found in secrets")
        
        if not st.secrets["GROQ_API_KEY"]:
            raise ValueError("Empty API key in secrets")
        
        return Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    except ImportError:
        st.error("❌ Failed to import Groq library. Please ensure it's installed.")
        st.stop()
    except KeyError as e:
        st.error(f"❌ Configuration error: {str(e)}. Please contact support.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Unexpected error initializing API client: {str(e)}")
        st.stop()

# Initialize Groq client
try:
    client = initialize_groq_client()
except Exception as e:
    st.error(f"❌ Critical initialization error: {str(e)}")
    st.stop()

# Header
try:
    st.markdown('<div class="centered"><h1>📝 ATS Resume Expert</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="centered"><p>Optimize your resume for Applicant Tracking Systems</p></div>', unsafe_allow_html=True)
except Exception as e:
    st.error("❌ Error rendering application header")

# Sidebar
try:
    with st.sidebar:
        st.success("✅ Secure configuration active")
        st.markdown("### ℹ️ How It Works")
        st.markdown("""
        1. **Upload** your resume (PDF)
        2. **Add** job description (optional)
        3. **Choose** analysis type:
           - Evaluate resume quality or evaluate based on JD
           - Compare with ideal format
        """)
except Exception as e:
    st.error("❌ Error rendering sidebar content")

# Main application functions
def safe_extract_text(pdf_path_or_file):
    """Extract text from PDF with comprehensive error handling"""
    try:
        text = ""
        if isinstance(pdf_path_or_file, str):  
            if not os.path.exists(pdf_path_or_file):
                raise FileNotFoundError(f"File not found: {pdf_path_or_file}")
            
            with open(pdf_path_or_file, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                if len(pdf_reader.pages) == 0:
                    raise ValueError("PDF contains no readable pages")
                
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        
        else:  # File upload object
            pdf_reader = PyPDF2.PdfReader(pdf_path_or_file)
            if len(pdf_reader.pages) == 0:
                raise ValueError("Uploaded PDF contains no readable pages")
            
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        if not text.strip():
            raise ValueError("No readable text could be extracted from PDF")
        
        return text[:5000]  # Limit to first 5000 characters
    
    except PyPDF2.PdfReadError:
        raise Exception("Invalid PDF file - cannot be read")
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")

def safe_get_groq_response(input_text, pdf_text, prompt):
    """Get response from Groq API with error handling"""
    try:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_text},
            {"role": "user", "content": pdf_text}
        ]
        
        completion = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=messages,
            temperature=0.1,
            max_tokens=8192,
            top_p=0.9,
            timeout=30  # Added timeout
        )
        
        if not completion.choices:
            raise Exception("No response from API")
        
        return completion.choices[0].message.content
    
    except Exception as e:
        raise Exception(f"API request failed: {str(e)}")

# File upload section
try:
    st.markdown("## 📁 Upload Your Resume")
    uploaded_file = st.file_uploader("Select PDF file", type=["pdf"], label_visibility="collapsed")
    if uploaded_file:
        st.success("✅ Resume uploaded successfully!")
except Exception as e:
    st.error("❌ Error in file upload section")

# Job description section
try:
    st.markdown("## 📄 Job Description")
    input_text = st.text_area(
        "Paste job description here for tailored feedback",
        placeholder="(Optional) Example: Seeking software engineer with 3+ years Python experience...",
        label_visibility="collapsed"
    )
except Exception as e:
    st.error("❌ Error in job description section")

# Analysis options
try:
    st.markdown("## 🔍 Choose Analysis")
    col1, col2 = st.columns(2)
    with col1:
        analyze_btn = st.button("Analyze My Resume", use_container_width=True)
    with col2:
        compare_btn = st.button("Compare with Sample", use_container_width=True)
except Exception as e:
    st.error("❌ Error rendering analysis options")

# Response handling
if analyze_btn or compare_btn:
    try:
        if not uploaded_file:
            raise Exception("No resume uploaded")
        
        with st.spinner("Analyzing your resume..."):
            try:
                pdf_text = safe_extract_text(uploaded_file)
                
                if analyze_btn:
                    st.markdown("## 📊 Analysis Results")
                    prompt = """As an ATS expert, provide:
                    1. ATS Score (0-100) with explanation
                    2. JD match percentage (if provided)
                    3. Key strengths
                    4. Improvement areas
                    5. Specific recommendations
                    """
                    
                    try:
                        response = safe_get_groq_response(input_text, pdf_text, prompt)
                        st.write(response)
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
                
                elif compare_btn:
                    sample_path = 'Reference Resume- Fresher.pdf'
                    if not os.path.exists(sample_path):
                        raise FileNotFoundError("Sample resume file not found")
                    
                    st.markdown("## 🆚 Comparison Results")
                    try:
                        sample_text = safe_extract_text(sample_path)
                        prompt = """Compare uploaded resume with sample:
                        1. ATS Score difference
                        2. Missing sections
                        3. Format issues
                        4. Content gaps
                        5. Improvement checklist"""
                        
                        response = safe_get_groq_response(
                            f"Sample Resume:\n{sample_text}\n\nUploaded Resume:\n{pdf_text}",
                            "",
                            prompt
                        )
                        st.write(response)
                    except Exception as e:
                        st.error(f"❌ Comparison failed: {str(e)}")
            
            except Exception as e:
                st.error(f"❌ Error processing your resume: {str(e)}")
    
    except Exception as e:
        st.error(f"❌ Error in analysis process: {str(e)}")

# Footer
try:
    st.markdown("---")
    st.markdown('<div class="footer centered">© ATS Resume Expert | Powered by Groq AI</div>', unsafe_allow_html=True)
except Exception:
    pass  # Footer error is non-critical