import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
import json

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from auth import authenticate_user, register_user  # Import authentication functions

# Load environment variables
load_dotenv()


# st.set_page_config(page_title="Skill Gap Analyzer", page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQG0T4AvexPec4TiMn26zZw0QVkr5GAoG5MYQ&s")  # Set the favicon here


# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt template for skill gap analysis
prompt_template = """
You are an AI specializing in skill gap analysis. You will receive a list of skills required for a specific job 
and a list of skills the user currently possesses. Your task is to identify the skill gaps and suggest resources or 
courses to help the user acquire the missing skills. Provide the analysis in the following format:
{
  "Required Skills": ["skill1", "skill2", ...],
  "Current Skills": ["skillA", "skillB", ...],
  "Missing Skills": ["skillX", "skillY", ...],
  "Suggested Resources": [
    {
      "skill": "skillX",
      "resources": [
        {"name": "Resource 1", "link": "https://example.com/resource1"},
        {"name": "Resource 2", "link": "https://example.com/resource2"}
      ]
    },
    ...
  ]
}
"""

def generate_skill_gap_analysis(required_skills, current_skills):
    input_data = {
        "Required Skills": required_skills,
        "Current Skills": current_skills
    }
    prompt = prompt_template + str(input_data)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

def display_analysis_result(analysis_result):
    try:
        analysis_json = json.loads(analysis_result)
        
        st.subheader("Required Skills")
        st.write(", ".join(analysis_json["Required Skills"]))
        
        st.subheader("Current Skills")
        st.write(", ".join(analysis_json["Current Skills"]))
        
        st.subheader("Missing Skills")
        st.write(", ".join(analysis_json["Missing Skills"]))
        
        st.subheader("Suggested Resources")
        for resource in analysis_json["Suggested Resources"]:
            st.write(f"**{resource['skill']}**")
            for res in resource["resources"]:
                st.markdown(f"- [{res['name']}]({res['link']})")
    except Exception as e:
        st.error(f"Error parsing analysis result: {e}")

# Function to show the login page
def show_login_page():

    st.title("Welcome to the Skill Gap Analyzer!")
    st.subheader("Log in to identify and address skill gaps in your expertise. Enhance your skills and stay ahead in your career journey!")

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
    st.set_page_config(page_title="Skill Gap Analyzer", layout="wide")
    st.title("Skill Gap Analyzer")
    st.subheader("Identify and bridge your skill gaps")

    st.markdown("### Enter the required and current skills to find out what you're missing and get suggestions to improve!")

    required_skills = st.text_area("Enter the required skills for the job (comma-separated):", key="required_skills")
    current_skills = st.text_area("Enter your current skills (comma-separated):", key="current_skills")

    if st.button("Analyze Skill Gap"):
        if required_skills and current_skills:
            required_skills_list = [skill.strip() for skill in required_skills.split(",")]
            current_skills_list = [skill.strip() for skill in current_skills.split(",")]
            
            if not required_skills_list or not current_skills_list:
                st.warning("Please enter both required skills and current skills.")
            else:
                with st.spinner("Analyzing..."):
                    try:
                        analysis_result = generate_skill_gap_analysis(required_skills_list, current_skills_list)
                        st.subheader("Skill Gap Analysis Result:")
                        display_analysis_result(analysis_result)
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter both required skills and current skills.")

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
