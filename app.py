import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate job description using Gemini API
def generate_job_description(job_title, department, work_mode):
    prompt = f"""
    Generate a job description for a {job_title} in the {department} department. 
    The work mode for this role is {work_mode}. 
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

    # Generate button
    if st.button("Generate Job Description"):
        if job_title and department and work_mode:
            st.info("Generating job description...")
            # Generate the job description
            job_description = generate_job_description(job_title, department, work_mode)
            st.subheader("Generated Job Description:")
            st.text_area("Output", value=job_description, height=300)
        else:
            st.error("Please fill out all the fields (Job Title, Department, and Work Mode).")

if __name__ == "__main__":
    main()
