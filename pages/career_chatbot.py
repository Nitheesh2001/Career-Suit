import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from utils.auth import authenticate_user, register_user  # Import your authentication functions

# Load environment variables
load_dotenv()


# st.set_page_config(page_title="Career Counseling Chatbot", page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTV6dZlfp_dO11YAIx0RinVqx60NOpRgZvNmw&s")  # Set the favicon here

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to check login status and redirect to login if not logged in
def check_login_status():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.error("You need to log in to access this page.")
        st.write("Click below to go to the login or signup page.")
        if st.button("Go to Login Page"):
            st.session_state["page"] = "login"
            st.experimental_rerun()  # Refresh to redirect to the login page
        if st.button("Go to Signup Page"):
            st.session_state["page"] = "signup"
            st.experimental_rerun()  # Refresh to redirect to the signup page
        st.stop()

# Handle page state
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Display login page if needed
if st.session_state["page"] == "login":
   
    st.title("Welcome to Career Chatbot!")
    st.subheader("Log in to explore career resources and tools designed for your success. Discover how Career Chatbot can assist you on your professional journey!")
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):  # Check credentials
            st.session_state["logged_in"] = True
            st.session_state["page"] = "home"
            st.experimental_rerun()  # Refresh to show the home page
        else:
            st.error("Invalid credentials. Please try again.")

    if st.button("Sign Up"):
        st.session_state["page"] = "signup"
        st.experimental_rerun()  # Refresh to redirect to the signup page

# Display signup page if needed
if st.session_state["page"] == "signup":
    st.title("Signup Page")
    username = st.text_input("Username", key="signup_username")
    password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

    if st.button("Signup"):
        if password == confirm_password:
            if register_user(username, password):
                st.success("Signup successful! You can now log in.")
                st.session_state["page"] = "login"
                st.experimental_rerun()  # Refresh to show the login page
            else:
                st.error("Signup failed. Username might already exist.")
        else:
            st.error("Passwords do not match.")

    if st.button("Go to Login Page"):
        st.session_state["page"] = "login"
        st.experimental_rerun()  # Refresh to redirect to the login page

# Display home page if logged in
if st.session_state["page"] == "home":
    check_login_status()

    # Function to get career path recommendation
    def get_career_recommendation(education, goals):
        prompt = f"""
        You are a career counselor. Based on the following details, provide a detailed career roadmap for the student.
        Education: {education}
        Goals: {goals}

        Provide a step-by-step guide on how the student can achieve their career goals.
        """
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text

    # Streamlit app
    st.set_page_config(page_title="Career Counseling Chatbot", layout="wide")
    st.title("Career Counseling Chatbot")

    # Collect user input
    st.header("Tell us about yourself")
    education = st.text_area("Education Background", placeholder="e.g., Computer Science, Commerce, Biology, Chemistry, Physics, etc.")
    goals = st.text_area("Career Goals", placeholder="e.g., Machine Learning Engineer, Software Engineer, Data Scientist, etc.")

    # Button to submit the form
    if st.button("Get Career Roadmap"):
        if education and goals:
            with st.spinner("Generating your career roadmap..."):
                try:
                    recommendation = get_career_recommendation(education, goals)
                    st.subheader("Your Career Roadmap")
                    st.write(recommendation)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please fill out all the fields.")
