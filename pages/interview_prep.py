import streamlit as st
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import PyPDF2
from utils.auth import authenticate_user, register_user  # Import authentication functions

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Interview Preparation AI", page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJL_4deHMJLHCB-63srdgaBe2JZmiOSxlnEg&s")  # Set the favicon here

# Configure Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "login"

# Function to generate interview preparation materials
def generate_interview_preparation(job_role, resume_text, job_description, num_questions):
    prompt_template = """
    You are an AI assistant specializing in interview preparation. You will provide a list of common interview questions 
    for a given job role, and also offer detailed answers based on the provided resume and job description. Provide the 
    questions and answers in the following format:
    {
      "Interview Questions": ["question1", "question2", ...],
      "Detailed Answers": {
        "question1": "answer1",
        "question2": "answer2",
        ...
      }
    }
    """
    input_data = {
        "Job Role": job_role,
        "Resume": resume_text,
        "Job Description": job_description,
        "Number of Questions": num_questions
    }
    prompt = prompt_template + json.dumps(input_data)
    response = genai.generate_text(model="models/text-bison-001", prompt=prompt)
    return response.result

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Function to show the login page
def show_login_page():

    st.title("Welcome to the Interview Preparation Tool!")
    st.subheader("Log in to access tailored resources and practice questions. Boost your confidence and ace your next interview!")

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

# Function to show the signup page
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

# Function to show the main content page
def show_main_page():
    st.title("Interview Preparation Module")
    st.subheader("Get ready for your next job interview with tailored questions and answers")

    st.markdown("### Enter the job role, upload your resume, and paste the job description to receive customized interview questions and answers")

    job_role = st.text_input("Job Role", key="job_role")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", key="resume_file")
    job_description = st.text_area("Paste the Job Description", key="job_description")
    num_questions = st.number_input("Number of Questions", min_value=1, max_value=50, value=10, step=1, key="num_questions")

    if st.button("Generate Interview Questions and Answers"):
        if job_role and uploaded_file and job_description:
            with st.spinner("Generating interview preparation materials..."):
                try:
                    resume_text = extract_text_from_pdf(uploaded_file)
                    preparation_materials = generate_interview_preparation(job_role, resume_text, job_description, num_questions)
                    st.subheader("Interview Preparation Materials:")

                    # Parse the response to display questions and answers
                    questions_and_answers = json.loads(preparation_materials)

                    # Display questions and answers one by one
                    interview_questions = questions_and_answers["Interview Questions"][:num_questions]
                    detailed_answers = questions_and_answers["Detailed Answers"]

                    for i, question in enumerate(interview_questions, start=1):
                        st.write(f"**Question {i}:** {question}")
                        st.write(f"**Answer:** {detailed_answers[question]}")
                        st.write("---")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter the job role, upload your resume, and paste the job description.")

# Display the appropriate page based on login status
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
