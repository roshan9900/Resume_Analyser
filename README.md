# ATS Resume Expert

## Overview
ATS Resume Expert is an AI-powered tool that analyzes and compares resumes using Groq's language model. It provides feedback on resume quality, job description alignment, and ATS compatibility.

## Features
- Extracts text from uploaded PDF resumes.
- Compares resumes with a sample reference.
- Evaluates resumes against job descriptions.
- Provides professional feedback with strengths and weaknesses.
- Displays match percentage for job suitability.

## Technologies Used
- Python
- Streamlit
- PyPDF2
- Groq API
- Dotenv

## Project Structure
```
.
├── .vscode                 # VS Code settings
├── src                     # Source code directory
│   ├── main.py             # Streamlit application
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
├── Reference Resume- Fresher.pdf  # Sample resume for comparison
├── requirement.txt         # Dependencies
```

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/roshan9900/Resume_Analyser
   cd Resume_Analyser
   ```
2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirement.txt
   ```
4. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add the following line and replace `YOUR_GROQ_API_KEY` with your actual API key:
     ```sh
     GROQ_API_KEY=YOUR_GROQ_API_KEY
     ```

## Usage
1. Run the Streamlit application:
   ```sh
   streamlit run src/main.py
   ```
2. Upload a resume PDF.
3. Enter a job description for analysis.
4. Click "Tell Me About the Resume" for feedback.
5. Click "Compare with Sample Resume" to check formatting and structure against the reference resume.

## Notes
- Ensure the sample resume file (`Reference Resume- Fresher.pdf`) is present in the root directory.
- The tool uses Groq's language model to provide AI-based insights.

## License
This project is licensed under the MIT License.



