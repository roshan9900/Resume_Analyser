import os
import io
import base64
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from PIL import Image
import PyPDF2  
from groq import Groq  

_=load_dotenv(find_dotenv())
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")


GROQ_API_KE = st.text_input('Enter your api key')
client = Groq(api_key=str(GROQ_API_KE))

SAMPLE_RESUME_PATH = r"Reference Resume- Fresher.pdf"  

def extract_text_from_pdf(pdf_path_or_file):
    """Extracts text from a PDF file or uploaded file."""
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
    """Send extracted text to Groq API for evaluation."""
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
        return f"Error: {e}"


input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Compare with Sample Resume")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role also add the match percentage of resume with job description. 
Highlight the strengths and weaknesses in detail of the applicant in relation to the specified job requirements.
If the job description is not provided, just review the resume based on your experience and give feedback.
Also tell ATS Score of the resume.
"""

input_prompt2 = """
You are an ATS resume expert. Compare the uploaded resume with the provided sample resume.
- Identify missing sections (e.g., Summary, Skills, Experience, Education, Certifications).
- Highlight any differences in structure, formatting, and content.
- Provide suggestions to make the uploaded resume closer to the sample format.
- Also tell ATS Score of the resume.
- If the job description is not given, just analyse the resume and give summary.
"""

if submit1:
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)  # Extract text from uploaded resume
        response = get_groq_response(input_text, pdf_text, input_prompt1)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("Please upload the resume")

elif submit2:
    if uploaded_file is not None and os.path.exists(SAMPLE_RESUME_PATH):
        uploaded_text = extract_text_from_pdf(uploaded_file)
        sample_text = extract_text_from_pdf(SAMPLE_RESUME_PATH)
        
       
        comparison_prompt = input_prompt2 + f"\n\nUploaded Resume:\n{uploaded_text}\n\nSample Resume:\n{sample_text}"
        response = get_groq_response(input_text, comparison_prompt, input_prompt2)

        st.subheader("Comparison Result:")
        st.write(response)
    else:
        st.warning("Please upload a resume and ensure the sample resume exists.")
