import streamlit as st
from openai import OpenAI


st.title("Student Doubt Solver")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= "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",
)

def doubt_solver(student_class,subject_name,student_doubt):
    prompt = f"""
    You are a highly adaptive doubt-solving AI assistant. Your task is to provide clear, well-structured answers tailored to the student's academic level, making complex concepts easy to understand. 

    ### **Guidelines:**
    1. **Adapt responses based on the student's academic level:**
    - If the student is in primary or secondary school (e.g., Class 1-10), give simple explanations with relatable examples.
    - If the student is in higher secondary (Class 11-12), provide a slightly deeper understanding with conceptual clarity.
    - If the student is in college or university (e.g., "3rd semester", "undergrad"), give a more detailed, technical explanation with in-depth reasoning.

    2. **Enhance answers for numericals (Math, Physics, etc.):**
    - When answering numericals, focus on intuitive problem-solving approaches.
    - Provide step-by-step explanations with relevant formulas and examples.
    - If possible, include real-world applications to help the student relate to the concept.

    3. **Answer concisely but effectively:** 
    - Keep responses around 5-6 lines for school students.
    - Expand to 8-10 lines for college-level queries when necessary.
    - Use bullet points or stepwise explanations for clarity.

    ### **Student Query Details:**
    - **Standard:** {student_class}
    - **Subject:** {subject_name}
    - **Doubt:** {student_doubt}

    ### **Provide your response in this format:**
    **Answer:** <Tailored explanation based on the student’s level, with examples if needed>
    """


    convo = client.chat.completions.create(
        model="openchat/openchat-7b:free",
        messages=[{"role": "system", "content": prompt}],
        temperature=1,
    )
    
    output = convo.choices[0].message.content.strip()

    return output

st.title("Ask you doubt")

form_values = {
    "subject" : None,
    "class" : None,
    "doubt" : None
}


with st.form(key="user_info"):
    form_values["subject"] = st.text_input("Enter your subject name:")
    form_values["class"] = st.text_input("Enter your class (e.g., 9, 10, or 3rd semester):")
    form_values["doubt"] = st.text_area("Enter your doubt:")

    submit_button = st.form_submit_button("Submit")
    if submit_button:
        if not all(form_values.values()):
            st.warning("Please fill up all the values!")
        else:
            with st.spinner("Generating answer..."):
                response = doubt_solver(form_values["class"], form_values["subject"], form_values["doubt"])
                st.subheader("Answer:")
                st.write(response)
