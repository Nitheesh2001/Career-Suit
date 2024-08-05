import streamlit as st
from utils.auth import authenticate_user, register_user

def main():
    # Set page configuration with favicon
    st.set_page_config(page_title="Career Suite", page_icon="https://uxwing.com/wp-content/themes/uxwing/download/business-professional-services/briefcase-bag-color-icon.png")  # Set the favicon here

    # Initialize session state for login status and page redirection
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    # Display the appropriate page based on the session state
    if st.session_state["logged_in"]:
        if st.session_state["page"] == "home":
            show_home_page()
        else:
            st.session_state["page"] = "home"
            st.experimental_rerun()  # Refresh the page to reflect the new state
    else:
        if st.session_state["page"] == "login":
            show_auth_page()
        else:
            st.session_state["page"] = "login"
            st.experimental_rerun()  # Refresh the page to reflect the new state

def show_auth_page():
    st.title("Login or Signup")
    auth_option = st.selectbox("Choose an option:", ["Login", "Signup"])

    if auth_option == "Login":
        show_login_page()
    elif auth_option == "Signup":
        show_signup_page()

def show_login_page():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state["logged_in"] = True
            st.session_state["page"] = "home"
            st.experimental_rerun()  # Refresh the page to reflect the new state
        else:
            st.error("Invalid credentials. Please try again.")

def show_signup_page():
    st.subheader("Signup")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Signup"):
        if password == confirm_password:
            if register_user(username, password):
                st.success("Signup successful! Please log in.")
                st.session_state["page"] = "login"
                st.experimental_rerun()  # Refresh the page to reflect the new state
            else:
                st.error("Signup failed. Username might already exist.")
        else:
            st.error("Passwords do not match.")

def show_home_page():
    st.title("Welcome to Career suits!")
    
    # Sidebar with logout button
    with st.sidebar:
        if st.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["page"] = "login"
            st.experimental_rerun()  # Refresh the page to reflect the new state

    # Main content area
    st.write("Welcome! You are now logged in and can access the following mini projects:")

    # Project summaries
    st.subheader("Project Summaries")

    
    # st.write("**1. Career Chatbot:**")
    # st.write("A virtual assistant providing personalized career advice and guidance to help users navigate their professional journey.")

    # st.write("**2. Cover Letter Generator:**")
    # st.write("Generates tailored cover letters to enhance job applications, making it easier to create impactful introductions.")

    # st.write("**3. Interview Preparation:**")
    # st.write("Offers resources and practice questions to help users prepare effectively for interviews and boost their confidence.")

    # st.write("**4. Mock Interview:**")
    # st.write("Simulates real interview scenarios and provides feedback, allowing users to practice and refine their interview skills.")

    # st.write("**5. PDF Genius:**")
    # st.write("Interacts with PDFs using LLMs to enable content extraction and summarization, streamlining document management.")

    # st.write("**6. Resume Builder:**")
    # st.write("Facilitates the creation of professional and polished resumes, helping users highlight their skills and experience effectively.")

    # st.write("**7. Skill Gap Analyzer:**")
    # st.write("Identifies discrepancies between current and required skills for specific job roles, and suggests resources to bridge those gaps.")

    # st.write("**8. Smart ATS:**")
    # st.write("Optimizes resumes using AI-driven insights to improve visibility and increase chances of passing Applicant Tracking Systems.")

    # st.write("**9. Soft Skills Assessment:**")
    # st.write("Evaluates and provides feedback on essential soft skills, helping users develop interpersonal effectiveness for career advancement.")

    col1, col2, col3 = st.columns(3)

    # First row
    with col1:
        st.write("**1. Career Chatbot:**")
        st.write("A virtual assistant providing personalized career advice and guidance to help users navigate their professional journey.")

    with col2:
        st.write("**2. Cover Letter Generator:**")
        st.write("Generates tailored cover letters to enhance job applications, making it easier to create impactful introductions.")

    with col3:
        st.write("**3. Interview Preparation:**")
        st.write("Offers resources and practice questions to help users prepare effectively for interviews and boost their confidence.")

    # Define columns for the second row
    col4, col5, col6 = st.columns(3)

    # Second row
    with col4:
        st.write("**4. Mock Interview:**")
        st.write("Simulates real interview scenarios and provides feedback, allowing users to practice and refine their interview skills.")

    with col5:
        st.write("**5. PDF Genius:**")
        st.write("Interacts with PDFs using LLMs to enable content extraction and summarization, streamlining document management.")

    with col6:
        st.write("**6. Resume Builder:**")
        st.write("Facilitates the creation of professional and polished resumes, helping users highlight their skills and experience effectively.")

    # Define columns for the third row
    col7, col8, col9 = st.columns(3)

    # Third row
    with col7:
        st.write("**7. Skill Gap Analyzer:**")
        st.write("Identifies discrepancies between current and required skills for specific job roles, and suggests resources to bridge those gaps.")

    with col8:
        st.write("**8. Smart ATS:**")
        st.write("Optimizes resumes using AI-driven insights to improve visibility and increase chances of passing Applicant Tracking Systems.")

    with col9:
        st.write("**9. Soft Skills Assessment:**")
        st.write("Evaluates and provides feedback on essential soft skills, helping users develop interpersonal effectiveness for career advancement.")



if __name__ == "__main__":
    main()
