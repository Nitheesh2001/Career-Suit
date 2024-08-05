import streamlit as st
import pyttsx3
import speech_recognition as sr
import os
from dotenv import load_dotenv
import google.generativeai as genai
import threading
import queue
from utils.auth import authenticate_user, register_user  # Import your authentication functions

# Load environment variables
load_dotenv()

# st.set_page_config(page_title="Mock Interview with AI Feedback", page_icon="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAgVBMVEX///8AAACDg4P39/eJiYmqqqpeXl4EBAT8/Pz5+fn09PStra08PDxaWlrAwMC7u7s2Njbm5uYjIyPGxsZ1dXXu7u4lJSUaGhrLy8vV1dXc3NwMDAwsLCzo6OgyMjJsbGwcHByamppSUlJKSkpDQ0NnZ2egoKCRkZGFhYV0dHQUFBTmUSIUAAAKc0lEQVR4nO2ci3aqOhCGE1EJeEFQUMHWW9XK+z/gyUyCtw0ETyli13xr110h1vxMMplJAowRBEEQBEEQBEEQBEEQBEEQBEEQBEEQBEEQBEEQBEEQBEEQBPH3EIIxx/eOp05nO5iGeOjVdaoZa9DnV6LO4tUVqhl/diOP2/AyP/4hI7p3+i4q7cGrK1YL0lAeKrKV6S4C5QG+D/9Ed+xcdW1GnW539nVpqZxP31+h6EtroZyR95EdjLcBmlUef/eW6rCdaqF87d+fmU7U8beXOEOXwoOlGhIz4PeebrpvPG5IGT1lwXXu+XiurPjxxn3RVxb8LjgdRuhw9m+scA+jAp8Vnnfn6FXftyuOsf77khIx9sTkbW04wfqHxQWgo0I7PTZXpxoRbFGl9ngVkmaqVDOCrUFh6pQXm2JLfs8RQ2Ab3ZqKraBUsTNqM0tU+FHuRQTbQqmgoTrVyxaa38RYLDa5o/ayhpp3zeV0jvGGfIINPXO5PSjs/X596ietGFbjBMDp9+tTP5gUxuZymCF3fr8+taMGC99c8PtdFapWujSXQxsWpR+tJoKaj83lDpUCgzayq1hzyKCq+Nz20YWa943FXF7RI7UPD6cMjfm7hxlIezJEcf3FVKmQV+qIfbgQozZNZITLxWLpmyskGM787gzFfMyeWhHSgKZFd59NX6/WA9fwCZW/G6IataRh+lPN4H/zB0blTdDBQpPSBqgyi/zZxoYJz5mubIkFXielOcEJy5YOGJ84ZdoGT3rkV4HXVxgOSjI7S5UrWn2RR884YXz+pUo/gRjxu7Wxq1y7JDDLZtKKTXRS18p9uSP9SDOzDbcLtQYfDw5aIKytFNZwpC7E4m7RQiGP6I79+njGzyx2vjOGe2m5vUKJbqJK5PVFd6fOvT6tcLUBd/80NtHVjbfYCr72TMPF42rvUX92VH+Nn+Wr2AxsqW1U1BcdPeMm2d0OLeExyA6bg6Pf5ltZcJrTlSThBC2RFnxYfiROskVgfjhOY99feqcvrleA+YHl/90GiVVbKlxvtyZ4BTrFlnALHTFM+b/agNBGbfQl+VURKsAuGbThY4O70cW+bMsYxi0QqBbI1mU1mXLd3Ipxutlwc0P0+lECUG7GLVEocOrX5h+FJaCnub3Jvb7DtB1bafwqC2QfqLBrqnDodXcr6Xs3w/62PWtNW1RoGUrNcLuFQaE6KyzDaluzYBJrG4MOsWxNgvA0Fq+yfCkYepFW5OnPskCnYHYImDs+scopXh/IaHAg+zSXw+1NXwUnhfP67KiQE2YU5nKwGM83+eeUa/EXx26/o7Plxfq8HSxbMTdTddEEw+u8DRXQGsPpabdSg2CKxpzqITFd92Lx4lGx6qKJyiDzxoGwd+DzZJVEKmTD/OKQxW+g8uy9XuGtDQtqE+fYUMDu9T3nQZSkwUYbERWOHiLwwwuXuB/7oWPlS8zthz5en/QzjaJgE5QolB/dvqpToi8dXt+7bn5481hOsuxLq8Lh1SpNpb5Nat8olCEQ121VJxqd1+zBVOPh9b1r5SucPbbmeCdrH0Xao+xO45AN7204YLE3yxJ9FDl7xY4TC79eTVEIy3XQhg68CMtSw4DjSNUqpnHkyIfN2D3zNEiTTbBJZS/zVM33KU8zhbLRqgjI7+0vCtV2haYz/uHFOMK1XBdsaMlfHCnQRYkuKJVxKd/w2IGDLm4MXiV2ZG8433suXBqZPbGhHW2450gB/U1ys6c0PK4uqeN80XhTPV2GARAINgTjWSAM3goQ5bKOzaXBHNeRClkso/WNHURzeWliaXAwsizH9hue2mPhwmgRrC5RLC749Hl2B8balMfUTZzlhyBMgDAHTQf2lJVnUqAj88OAz2UTgzdODz4QJdJ+3VA2OceRDtiVn2bDJI2kDeVfGW3mm4d9wfE6s2PSqBlln8BmKmNvR0pjSqHUJBueC/YCUdLPyPFcNlJUeObgXiL0G/ISCPkPFDrQSjdSoZAtdjePkqR3/z3om1SHbHjzkJqnOYMhVANFDyNc7IwM7bMAx5H08U3EYWTgyT7Gt5b+QYVQzIMoXNoQPI1w7o01nesZxl2zSfIQBy2PyUaJPkb5UAtsiv3LCaVLkapi6YOcMZ9LhXO7Jxz0Teh5LEcrnGuFBx4FyYC5YXgrUYaw39qMq5I5n/pR+bvMgkOUyLAfCvClgPx/KJ1MJJNDVw4cHp/PI77zGYYoDl4S2Vi1wkD3w/4cfWnoho89bplqMzY4XyAwNrVBorKeUIM+GAiqb30lAd8kiW670uHzLjhPpiUqW8ofaKUp2BDGwyCQCq3w31DN6muH0+RUlZio63pkOYF3HCj92bpF2J3lraQBDzFN7pyHwC3DdtMSQ718NHrYhScd7EkPY1VuCfknastFoG9rVqLA3AjN2LnT6AxSfb23N8YtHMyqKWTsslpVYVtjbfhpFlZ9HZc46eL43uESM1ebZEOFmAn2yxUyX39Zk5G4exsfp5NJpDMfrmpdKQhBhdFkMhmmBoXZonOzGxi2/LIKeAUOjKrmrsP7z5Z2XR//dIVJvvoQzD/wHKJx5XTnCYVCptQ2r3AnQ83Es4vltDV3z6yPHdDtZhhuP/BeolD6l2lnldkgOQyei6385NaEpcuN+gb3xhXqOMVfTqdLX+2qeSrPEYvphaXBO71GYZOQwvfn7yscN61QuQU39o5bnzkYdA9Og+lHQTIen0f9n7Fv3obL3kHP76rlIrVHI/nqev9Gjx95scGT2I2Oh+5NlK13LC9udsesTpjoXN3/oGAP1FMKeWNRm/B299+Newm9+2NJ53ba4eHk/8Z8N8qPxckG951dUgzU4AW/d6zfqKdCAJPB1Yhf9SiscFfYT4n7Od870gr/bYinLM0Q497PGfz+YhRkE9eM6XPm+UeczNAKOR+6i2Nfm1j9dGut068KFMzNHn4ENe8P0GMObm2YLRguT5/8atFjO3arVQC8hbbfUN0cI/IUqtg7Pl2b6mcDvefHyHRX+QpcDLrxkrk2VHiX24V4x3n5tl8j3qXVde5ywEKFoGixy65KYMqNXgrsx1png8D6IV4psSGwwDUOMHyb73mVLTRL4yfLR69hUHgz1vdbtcfyBpHFY3butlmjQmbNdHQQNbp8VB1xecTYMG/G2ayQsWk2HdPSzrjVBuzmDmtmhbCje6RH0RY+zONyq1XRzbtVbMj0Y1s43CvUMisKvCNSksQFA1o1hXr5qHVWFELdDWjzYeGGj4o2xJ18ehGwRT5V3w5p831xpVAhZk/TcoXsI1ESm1whMzJVC6Fld5ejwslxu92eDQpZqNYWV3XX8ifgYzjhZrliBvwSztkGhTBZo5762B7woUdfpe4PV4RsO8s6yhQKvZTbpmY6UQ6+jMF9Yl/+uITKT+BpjAoKLX5HeWHnHRXCZpIrhs0S76nwnvKx7i8oLIcUNs+k4iPyKtNOhYdubXy3UuGPF1TugCCwTQo/a1WX0SaF+7pNiIFpm55LOjbX+Hla8XgkjWCLbqduSp5cQxAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRBEa/kPzguByO8kbRAAAAAASUVORK5CYII=")  # Set the favicon here

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to get feedback from Gemini API
def get_feedback(answer, context):
    prompt = f"""
    Context: {context}
    Answer: {answer}

    Provide feedback on the answer and suggest areas of improvement.
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

# Function to generate follow-up question based on previous answer
def generate_followup_question(previous_answer):
    prompt = f"""
    Based on the following answer, generate a follow-up question.
    Answer: {previous_answer}
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

# Function to capture audio response and convert to text
def get_audio_response(q):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        st.write("Listening for your response...")
        audio = recognizer.listen(source)
        try:
            response = recognizer.recognize_google(audio)
            q.put(response)
        except sr.UnknownValueError:
            q.put("Could not understand audio")
        except sr.RequestError as e:
            q.put(f"Could not request results; {e}")

# Function to generate initial questions based on user input
def generate_initial_questions(job_type, experience_level, interview_format, focus_areas):
    initial_questions = [
        f"Tell me about your experience in {job_type}.",
        f"What are your strengths and weaknesses as a {experience_level} professional?",
        f"How do you prepare for a {interview_format} interview?",
        f"What are the key focus areas in {focus_areas}?"
    ]
    return initial_questions

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

    st.title("Welcome to the Mock Interview!")
    st.subheader("Log in to simulate real interview scenarios and receive feedback. Sharpen your skills and get ready to impress!")

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

    if st.button("Back to Login"):
        st.session_state["page"] = "login"
        st.experimental_rerun()  # Refresh to redirect to the login page

# Display home page if logged in
if st.session_state["page"] == "home":
    check_login_status()

    # Streamlit app
    st.set_page_config(page_title="Mock Interview with AI Feedback", layout="wide")
    st.title("Mock Interview with AI Feedback")

    # Collect user input
    st.header("Tell us about yourself")
    job_type = st.text_area("Job or Industry", placeholder="e.g., software engineering, marketing, finance, healthcare, etc.")
    experience_level = st.text_area("Current Level of Experience", placeholder="e.g., entry-level, mid-level, senior-level, executive-level")
    interview_format = st.text_area("Preferred Interview Format", placeholder="e.g., behavioral, technical, case study, panel interview")
    focus_areas = st.text_area("Specific Focus Areas", placeholder="e.g., common interview questions, salary negotiation, body language")

    # Initialize session state
    if 'questions' not in st.session_state:
        st.session_state.questions = generate_initial_questions(job_type, experience_level, interview_format, focus_areas)
        st.session_state.current_question = 0
        st.session_state.responses = []
        st.session_state.current_response = ""
        st.session_state.recording = False
        st.session_state.total_feedback = []
        st.session_state.interview_started = False

    # Button to start the mock interview
    if st.button("Start Mock Interview"):
        if job_type and experience_level and interview_format and focus_areas:
            st.session_state.questions = generate_initial_questions(job_type, experience_level, interview_format, focus_areas)
            st.session_state.current_question = 0
            st.session_state.responses = []
            st.session_state.current_response = ""
            st.session_state.recording = False
            st.session_state.total_feedback = []
            st.session_state.interview_started = True

    # Function to handle recording and feedback loop
    def handle_question():
        if st.session_state.current_question < len(st.session_state.questions):
            question = st.session_state.questions[st.session_state.current_question]
            st.write(f"Question {st.session_state.current_question + 1}: {question}")

            q = queue.Queue()
            if st.session_state.recording:
                st.write("Recording...")
                response_thread = threading.Thread(target=get_audio_response, args=(q,))
                response_thread.start()
                response_thread.join()
                if not q.empty():
                    st.session_state.current_response = q.get()
                st.session_state.recording = False  # Stop recording after getting response
            else:
                if st.button("Double click to Start Recording Your Answer", key=f"stop_recording_{st.session_state.current_question}"):
                    st.session_state.recording = True

            if st.session_state.current_response:
                st.write(f"Recorded Answer: {st.session_state.current_response}")
                feedback = get_feedback(st.session_state.current_response, st.session_state.questions[st.session_state.current_question])
                st.write(f"Feedback: {feedback}")

                # Calculate feedback score
                score = min(max(len(st.session_state.current_response.split()) // 5, 1), 10)
                st.session_state.total_feedback.append(score)

                followup_question = generate_followup_question(st.session_state.current_response)
                st.session_state.questions.append(followup_question)
                st.session_state.current_question += 1
                st.session_state.current_response = ""
                handle_question()  # Recursive call to handle the next question

    # Loop through questions and feedback until "Finish" is clicked
    if 'interview_started' in st.session_state and st.session_state.interview_started:
        handle_question()

    # Finish button to end the mock interview
    finish_button_placeholder = st.empty()
    if finish_button_placeholder.button("Finish"):
        st.write("Mock Interview Finished")
        st.session_state.current_question = len(st.session_state.questions)
        st.session_state.interview_started = False

        # Calculate total feedback score
        if st.session_state.total_feedback:
            total_score = sum(st.session_state.total_feedback) // len(st.session_state.total_feedback)
        else:
            total_score = 0

        if total_score >= 7:
            st.write(f"Overall Feedback Score: {total_score}/10")
            st.write("Great job! Keep it up!")
        elif 4 <= total_score < 7:
            st.write(f"Overall Feedback Score: {total_score}/10")
            st.write("Good effort, but there's room for improvement.")
        else:
            st.write(f"Overall Feedback Score: {total_score}/10")
            st.write("Consider reviewing the feedback and practicing more.")

        st.session_state.total_feedback = []  # Reset feedback for future sessions
