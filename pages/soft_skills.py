import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
from auth import authenticate_user, register_user  # Import authentication functions

# Load environment variables
load_dotenv()


# st.set_page_config(page_title="Soft Skills Assessment", page_icon="data:image/png;base64,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")  # Set the favicon here


# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Questions for the quiz with placeholders
questions = {
    "Teamwork": ("Please rate your teamwork skills from 1 to 5 and provide a brief example of a team project you have worked on.", "Rate from 1 to 5, and describe a team project"),
    "Problem Solving": ("Please rate your problem-solving skills from 1 to 5 and describe a situation where you solved a difficult problem.", "Rate from 1 to 5, and describe a problem-solving situation"),
    "Communication": ("Please rate your communication skills from 1 to 5 and share an experience where effective communication was crucial.", "Rate from 1 to 5, and describe a communication experience"),
    "Adaptability": ("Please rate your adaptability from 1 to 5 and give an example of how you adapted to a new situation.", "Rate from 1 to 5, and describe an adaptable situation"),
    "Critical Thinking": ("Please rate your critical thinking skills from 1 to 5 and provide an example of a time you used critical thinking.", "Rate from 1 to 5, and describe a critical thinking example"),
    "Time Management": ("Please rate your time management skills from 1 to 5 and describe how you manage your time effectively.", "Rate from 1 to 5, and describe time management strategies"),
    "Interpersonal": ("Please rate your interpersonal skills from 1 to 5 and share an example of how you interact with others in a professional setting.", "Rate from 1 to 5, and describe an interpersonal interaction")
}

# Function to get feedback from Gemini API
def get_feedback(answers):
    questions_and_answers = "\n".join([f"Q: {q}\nA: {a}" for q, a in answers.items()])
    prompt = f"""
    Based on the following self-assessment of soft skills, provide a detailed analysis and suggestions for improvement.
    {questions_and_answers}
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

# Resources for improvement
resources = {
    "Teamwork": ["https://example.com/teamwork-video", "https://example.com/teamwork-document"],
    "Problem Solving": ["https://example.com/problem-solving-video", "https://example.com/problem-solving-document"],
    "Communication": ["https://example.com/communication-video", "https://example.com/communication-document"],
    "Adaptability": ["https://example.com/adaptability-video", "https://example.com/adaptability-document"],
    "Critical Thinking": ["https://example.com/critical-thinking-video", "https://example.com/critical-thinking-document"],
    "Time Management": ["https://example.com/time-management-video", "https://example.com/time-management-document"],
    "Interpersonal": ["https://example.com/interpersonal-video", "https://example.com/interpersonal-document"]
}

# Descriptions of why each skill is important
descriptions = {
    "Teamwork": "Teamwork is crucial for achieving collective goals, enhancing productivity, and fostering a collaborative environment.",
    "Problem Solving": "Problem-solving skills enable individuals to effectively tackle challenges and find innovative solutions.",
    "Communication": "Effective communication is essential for sharing information, building relationships, and ensuring clarity.",
    "Adaptability": "Adaptability helps individuals adjust to new circumstances, remain flexible, and thrive in changing environments.",
    "Critical Thinking": "Critical thinking involves analyzing situations, making informed decisions, and solving problems logically.",
    "Time Management": "Time management skills help prioritize tasks, meet deadlines, and maintain a healthy work-life balance.",
    "Interpersonal": "Interpersonal skills facilitate positive interactions, teamwork, and collaboration in professional settings."
}

def show_login_page():

    st.title("Welcome to the Soft Skills Assessment!")
    st.subheader("Log in to evaluate and enhance your soft skills. Gain valuable insights to boost your interpersonal effectiveness and career success!")

    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state["logged_in"] = True
            st.session_state["page"] = "main"
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

    if st.button("Sign Up"):
        st.session_state["page"] = "signup"
        st.experimental_rerun()

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

def show_main_page():
    st.set_page_config(page_title="Soft Skills Assessment", layout="wide")
    st.title("Soft Skills Assessment")

    # Collect user input
    st.header("Answer the following questions to assess your soft skills")
    answers = {}
    for skill, (question, placeholder) in questions.items():
        answer = st.text_area(skill, placeholder=placeholder)
        answers[skill] = answer

    # Button to submit the form
    if st.button("Get Feedback"):
        if all(answers.values()):
            with st.spinner("Generating your soft skills assessment..."):
                try:
                    feedback = get_feedback(answers)
                    st.subheader("Your Soft Skills Feedback")
                    st.write(feedback)
                    
                    # Display resources for improvement
                    st.subheader("Resources for Improvement")
                    for skill, answer in answers.items():
                        rating = int(answer.split()[0]) if answer.split() else 0
                        if rating < 4:  # Assuming a rating less than 4 indicates a need for improvement
                            st.markdown(f"### {skill}")
                            st.write(descriptions[skill])
                            for resource in resources[skill]:
                                st.write(resource)
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
        show_main_page()
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
