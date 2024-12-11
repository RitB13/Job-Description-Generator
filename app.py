import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate job description using Gemini API
def generate_job_description(job_title, department, work_mode, experience_range,experience_level,employement_type):
    prompt = f"""
    Generate a job description for a {job_title} in the {department} department. 
    The work mode for this role is {work_mode}. 
    The candidate should have {experience_range} years of experience.
    The candidate should be having experience of {experience_level} level.
    Theemployemet type for thid role id {employement_type}.
    Include responsibilities, mandatory skills, required qualifications, and preferred skills.
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
    job_title = st.text_input("Job Title", placeholder="Enter job title (e.g., Data Scientist)")

    departments = [
        "IT", "Marketing", "Finance", "HR", "Sales", "Engineering", "Operations", 
        "Legal", "Product Management", "Customer Support", "Design", "R&D"
    ]
    department = st.selectbox("Department", options=departments)

    work_mode = st.radio("Your Role is", options=["In-Office", "Hybrid", "Remote"])



    # Work experience range
    col1, col2 = st.columns(2)
    with col1:
        experience_start = st.number_input("Minimum Experience (Years)", min_value=0, step=1, value=0)
    with col2:
        experience_end = st.number_input("Maximum Experience (Years)", min_value=experience_start, step=1, value=experience_start + 1)
    #experience level
    experience_levels = [
        'entry','associate','mid-senior','director/vp','executive/president'
    ]
    experience_level = st.selectbox("Expereince Level", options=experience_levels)

    #Emptype
    employement_types=['full','part','contract','internship','freelance'

    ]
    employement_type=st.selectbox("Employment Type", options=employement_types)
    # Generate button
    if st.button("Generate Job Description"):
        if job_title and department and work_mode and experience_start <= experience_end and experience_level and employement_type:
            st.info("Generating job description...")
            # Format experience range
            experience_range = f"{experience_start}-{experience_end}"
            # Generate the job description
            job_description = generate_job_description(job_title, department, work_mode, experience_range,experience_level,employement_type)
            st.subheader("Generated Job Description:")
            st.text_area("Output", value=job_description, height=300)
        else:
            st.error("Please fill out all the fields (Job Title, Department, Work Mode, and Experience Range).")

if __name__ == "__main__":
    main()
