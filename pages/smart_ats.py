import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
from utils.auth import authenticate_user, register_user  # Import authentication functions

# Load environment variables
load_dotenv()


st.set_page_config(page_title="Smart ATS (Applicant Tracking System)", page_icon="data:image/png;base64,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")  # Set the favicon here



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "login"

# Function to get Gemini response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Prompt Template
input_prompt = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, data analyst,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
the best assistance for improving the resumes. Assign the percentage Matching based 
on JD and
the missing keywords with high accuracy.
resume: {text}
description: {jd}

I want the response in one single string having the structure
{{"Job description Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

# Login page
def show_login_page():

    st.title("Welcome to Smart ATS!")
    st.subheader("Log in to optimize your resume with AI-powered insights. Tailor your application to stand out and get noticed by employers!")

    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state["logged_in"] = True
            st.session_state["page"] = "home"
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

    if st.button("Sign Up"):
        st.session_state["page"] = "signup"
        st.experimental_rerun()

# Signup page
def show_signup_page():
    st.title("Signup")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Signup"):
        if password == confirm_password:
            if register_user(username, password):
                st.success("Signup successful! Please log in.")
                st.session_state["page"] = "login"
                st.experimental_rerun()
            else:
                st.error("Signup failed. Username might already exist.")
        else:
            st.error("Passwords do not match.")

    if st.button("Back to Login"):
        st.session_state["page"] = "login"
        st.experimental_rerun()

# Main content page
def show_main_page():
    st.title("Smart ATS")
    st.text("Improve Your Resume ATS")
    jd = st.text_area("Paste the Job Description")
    uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

    if st.button("Submit"):
        if uploaded_file is not None:
            text = input_pdf_text(uploaded_file)
            formatted_prompt = input_prompt.format(text=text, jd=jd)
            response = get_gemini_response(formatted_prompt)
            st.subheader("ATS Evaluation Result")
            st.write(response)
        else:
            st.warning("Please upload a PDF resume")

# Display appropriate page based on login status
if st.session_state["logged_in"]:
    if st.session_state["page"] == "home":
        show_main_page()
    else:
        st.session_state["page"] = "home"
        st.experimental_rerun()
else:
    if st.session_state["page"] == "login":
        show_login_page()
    elif st.session_state["page"] == "signup":
        show_signup_page()
    else:
        st.session_state["page"] = "login"
        st.experimental_rerun()
