import streamlit as st
from fpdf import FPDF
import os
from dotenv import load_dotenv
import google.generativeai as genai

from utils.auth import authenticate_user, register_user  # Import authentication functions

# Load environment variables
load_dotenv()


# st.set_page_config(page_title="Resume Builder", page_icon="data:image/png;base64,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")  # Set the favicon here


# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get resume content
def get_resume_content(name, email, phone, education, experience, skills, projects):
    prompt = f"""
    You are a professional resume builder. Based on the following details, create a well-structured resume.
    Name: {name}
    Email: {email}
    Phone: {phone}
    Education: {education}
    Experience: {experience}
    Skills: {skills}
    Projects: {projects}
    
    Provide a detailed and formatted resume.
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

# Function to generate PDF
def generate_pdf(resume_content, filename="resume.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in resume_content.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True, align='L')

    pdf.output(filename)
    return filename

# Function to show the login page
def show_login_page():

    st.title("Welcome to the Resume Builder!")
    st.subheader("Log in to craft impressive resumes effortlessly. Highlight your skills and experience to make a standout impression on employers!")

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
    st.set_page_config(page_title="Resume Builder", layout="wide")
    st.title("Resume Builder")

    # Collect user input
    st.header("Enter your details")
    name = st.text_input("Full Name", placeholder="e.g., John Doe")
    email = st.text_input("Email", placeholder="e.g., john.doe@example.com")
    phone = st.text_input("Phone", placeholder="e.g., +1234567890")
    education = st.text_area("Education", placeholder="e.g., B.Sc. in Computer Science from XYZ University")
    experience = st.text_area("Experience", placeholder="e.g., Software Engineer at ABC Corp. (2018-2022)")
    skills = st.text_area("Skills", placeholder="e.g., Python, Machine Learning, Data Analysis")
    projects = st.text_area("Projects", placeholder="e.g., AI Chatbot, E-commerce Website")

    # Button to submit the form
    if st.button("Generate Resume"):
        if name and email and phone and education and experience and skills and projects:
            with st.spinner("Generating your resume..."):
                try:
                    resume_content = get_resume_content(name, email, phone, education, experience, skills, projects)
                    st.subheader("Your Resume")
                    st.text(resume_content)
                    
                    # Generate and provide download link for PDF
                    pdf_filename = generate_pdf(resume_content)
                    with open(pdf_filename, "rb") as file:
                        st.download_button(
                            label="Download Resume as PDF",
                            data=file,
                            file_name="resume.pdf",
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please fill out all the fields.")

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "page" not in st.session_state:
        st.session_state["page"] = "login"

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

if __name__ == "__main__":
    main()
