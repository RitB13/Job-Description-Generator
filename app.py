import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate job description using Gemini API
def generate_job_description(role, experience, skills, location):
    prompt = f"""
    Generate a job description for a {role} with {experience} experience, requiring skills in {skills}. 
    Location: {location}. Include responsibilities, required qualifications, and skills.
    """
    try:
        # Create the generative model instance
        model = genai.GenerativeModel('gemini-pro')
        # Generate content using the API
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error occurred: {e}"

# Streamlit App
def main():
    st.title("Job Description Generator")

    # Load the uploaded CSV file
    uploaded_file = 'skills.csv'  # Path to the uploaded file
    try:
        df = pd.read_csv(uploaded_file)
        if 'role' not in df.columns or 'skills' not in df.columns:
            st.error("The CSV file must contain 'role' and 'skills' columns.")
            return
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return

    # Select job role
    selected_role = st.selectbox("Select Job Role", options=df['role'].unique())
    
    # Filter skill categories for the selected role
    related_skills = df[df['role'] == selected_role]['skills'].unique()
    
    # Multi-select for related skill categories
    selected_skills = st.multiselect("Select Skills", options=related_skills)

    # Input fields
    experience = st.text_input("Experience", placeholder="Enter experience (e.g., 3-5 years)")
    location = st.text_input("Location", placeholder="Enter job location (e.g., Remote)")

    # Generate button
    if st.button("Generate Job Description"):
        if selected_role and experience and selected_skills:
            st.info("Generating job description...")
            # Generate the job description
            skills_string = ", ".join(selected_skills)
            job_description = generate_job_description(selected_role, experience, skills_string, location or "Not specified")
            st.subheader("Generated Job Description:")
            st.text_area("Output", value=job_description, height=300)
        else:
            st.error("Please fill out the required fields (Job Role, Experience, and Skills).")

if __name__ == "__main__":
    main()
