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

# Function to generate job title suggestions based on input
def generate_job_title_suggestions(input_text):
    prompt = f"""
    Based on the input '{input_text}', generate a list of relevant job titles.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text.split('\n')  # Split the response into a list of job titles
    except Exception as e:
        return []

# Function to generate skills suggestions based on input
def generate_skills_suggestions(input_text):
    prompt = f"""
    Based on the input '{input_text}', generate a list of relevant skills.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text.split('\n')  # Split the response into a list of skills
    except Exception as e:
        return []

# Streamlit App
def main():
    st.title("Job Description Generator")
    
    # Input for Job Title with dynamic suggestions
    role_input_key = "role_input_"  # Prefix for the role input key to avoid duplication
    role_input = st.text_input("Job Title Keywords", placeholder="Enter job title (e.g., Data Scientist)", key=role_input_key)
    if role_input:
        job_titles = generate_job_title_suggestions(role_input)
        job_titles = [title.strip() for title in job_titles if title.strip()]  # Clean up any empty entries
        if job_titles:
            role = st.selectbox("Select Job Title", job_titles, key=f"{role_input_key}_select")
        else:
            role = st.text_input("Job Title (Enter a valid title)", key=f"{role_input_key}_fallback")
    else:
        role = st.text_input("Job Title", placeholder="Enter job title (e.g., Data Scientist)", key=f"{role_input_key}_fallback")
    
    # Input for Skills with dynamic suggestions
    skills_input_key = "skills_input_"  # Prefix for the skills input key to avoid duplication
    skills_input = st.text_input("Skills Keywords", placeholder="Enter skills (e.g., Python, SQL)", key=skills_input_key)
    if skills_input:
        skills_list = generate_skills_suggestions(skills_input)
        skills_list = [skill.strip() for skill in skills_list if skill.strip()]  # Clean up empty entries
        if skills_list:
            skills = st.multiselect("Select Skills", skills_list, key=f"{skills_input_key}_select")
        else:
            skills = st.text_area("Skills (Enter comma-separated skills)", key=f"{skills_input_key}_area")
    else:
        skills = st.text_area("Skills", placeholder="Enter skills (e.g., Python, SQL)", key=f"{skills_input_key}_area")
    
    # Input for Experience and Location
    experience = st.text_input("Experience", placeholder="Enter experience (e.g., 3-5 years)", key="experience_input")
    location = st.text_input("Location", placeholder="Enter job location (e.g., Remote)", key="location_input")
    
    # Generate button for job description
    if st.button("Generate Job Description", key="generate_button"):
        if role and experience and skills:
            st.info("Generating job description...")
            # Generate the job description
            job_description = generate_job_description(role, experience, ', '.join(skills), location or "Not specified")
            st.subheader("Generated Job Description:")
            st.text_area("Output", value=job_description, height=300, key="job_description_output")
        else:
            st.error("Please fill out the required fields (Job Title, Experience, and Skills).")

if __name__ == "__main__":
    main()
