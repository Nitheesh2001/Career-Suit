import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from utils.auth import authenticate_user, register_user  # Import authentication functions

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Cover Letter Generator", page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQyaj0dXzDwohqdIgkw8r9o8X1YBmC7iWDdeA&s")  # Set the favicon here

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "login"

# Function to get cover letter from Gemini API
def generate_cover_letter(details):
    prompt = f"""
    Generate a professional cover letter based on the following details:

    1. Full Name: {details['full_name']}
    2. Email: {details['email']}
    3. Phone Number: {details['phone']}
    4. Address: {details['address']}
    5. Company Name: {details['company_name']}
    6. Job Title: {details['job_title']}
    7. Introduction: {details['introduction']}
    8. Relevant Experience: {details['experience']}
    9. Skills: {details['skills']}
    10. Closing Statement: {details['closing_statement']}
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

# Function to show the login page
def show_login_page():

    st.title("Welcome to the Cover Letter Generator!")
    st.subheader("Log in to create personalized cover letters with ease. Enhance your job applications and make a lasting impression!")

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
    st.title("Cover Letter Generator")
    st.header("Fill in the following details to generate your cover letter")

    details = {
        'full_name': st.text_input("Full Name", placeholder="Enter your full name"),
        'email': st.text_input("Email", placeholder="Enter your email address"),
        'phone': st.text_input("Phone Number", placeholder="Enter your phone number"),
        'address': st.text_area("Address", placeholder="Enter your address"),
        'company_name': st.text_input("Company Name", placeholder="Enter the company name"),
        'job_title': st.text_input("Job Title", placeholder="Enter the job title you are applying for"),
        'introduction': st.text_area("Introduction", placeholder="Write a brief introduction about yourself"),
        'experience': st.text_area("Relevant Experience", placeholder="Describe your relevant experience"),
        'skills': st.text_area("Skills", placeholder="List your skills"),
        'closing_statement': st.text_area("Closing Statement", placeholder="Write a closing statement"),
    }

    if st.button("Generate Cover Letter"):
        if all(details.values()):
            with st.spinner("Generating your cover letter..."):
                try:
                    cover_letter = generate_cover_letter(details)
                    st.subheader("Your Generated Cover Letter")
                    st.write(cover_letter)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please fill out all the fields.")

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
