import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

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
    
    # Input fields
    role = st.text_input("Job Title", placeholder="Enter the job role (e.g., Data Scientist)")
    experience = st.text_input("Experience", placeholder="Enter experience (e.g., 3-5 years)")
    skills = st.text_area("Skills", placeholder="Enter required skills (e.g., Python, SQL, Machine Learning)")
    location = st.text_input("Location", placeholder="Enter job location (e.g., Remote)")
    
    # Generate button
    if st.button("Generate Job Description"):
        if role and experience and skills:
            st.info("Generating job description...")
            # Generate the job description
            job_description = generate_job_description(role, experience, skills, location or "Not specified")
            st.subheader("Generated Job Description:")
            st.text_area("Output", value=job_description, height=300)
        else:
            st.error("Please fill out the required fields (Job Title, Experience, and Skills).")

if __name__ == "__main__":
    main()