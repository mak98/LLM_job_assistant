import streamlit as st
from streamlit_option_menu import option_menu
import PyPDF2
import os

from cover_letter_bot import CoverLetterBot
bot3=CoverLetterBot("gpt-3.5-turbo")
bot4=CoverLetterBot("gpt-4-turbo")
if not st.session_state.keys():
    st.session_state["gpt3"]=""
    st.session_state["gpt4"]=""


def upload_pdf():
    st.title("Upload Resume in PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file:
        bot3.parse_resume(uploaded_file)
        bot4.parse_resume(uploaded_file)
        st.success("PDF file uploaded successfully!")

def gpt3():
    st.write(st.session_state["gpt3"])
    prompt = st.chat_input("Enter Only The Job Description Here")
    if prompt:
        st.write(f"Job: {prompt}")
        bot3.generate_cover_letter(prompt)
        st.write(f"Cover Letter:{bot3.cover_letter}")
        st.session_state["gpt3"]+=f"Cover Letter:{bot3.cover_letter}"
        doc_buffer=bot3.create_word_doc()
        st.download_button(
        label="Download Cover Letter",
        data=doc_buffer,
        file_name=bot3.file_name,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

def gpt4():
    st.write(st.session_state["gpt4"])
    prompt = st.chat_input("Enter Only The Job Description Here")
    if prompt:
        st.write(f"Job: {prompt}")
        bot4.generate_cover_letter(prompt)
        st.write(f"Cover Letter:{bot4.cover_letter}")
        st.session_state["gpt4"]+=f"Cover Letter:{bot4.cover_letter}"
    if st.button("Export to docx"):
        bot4.create_word_doc()
def main():
    st.sidebar.title('Navigation')
    selected = st.sidebar.radio('Go to', ["Upload Resume","GPT3.5","GPT4"])
    if selected=="Upload Resume":
        upload_pdf()
    elif selected=="GPT3.5":
        gpt3()
    elif selected=="GPT4":
        gpt4()


if __name__ == "__main__":
    main()