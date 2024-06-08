import streamlit as st
from services.job_bot import JobBot


if not st.session_state.keys():
    st.session_state.job_bot=JobBot()


def upload_pdf():
    st.title("Upload Resume in PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file:
        st.session_state.job_bot.parse_resume(uploaded_file)
        st.success("PDF file uploaded successfully!")
    st.header("Parsed Resume:")
    st.write(st.session_state.job_bot.resume)

def cover_letter_gpt3():
    st.title("Cover Letter GPT3")
    st.header("Enter Job Description:")
    prompt = st.chat_input("Enter Only The Job Description Here")
    if prompt:
        st.write(f"Job: {prompt}")
        st.session_state.cover_letter_gpt3.generate_cover_letter(prompt)
        st.header("Cover Letter:")
        st.write(st.session_state.cover_letter_gpt3.cover_letter)
        doc_buffer=st.session_state.cover_letter_gpt3.create_word_doc()
        st.download_button(
        label="Download Cover Letter",
        data=doc_buffer,
        file_name=st.session_state.cover_letter_gpt3.file_name,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

def cover_letter_gpt4():
    st.title("Cover Letter GPT4")
    st.header("Enter Job Description:")
    prompt = st.chat_input("Enter Only The Job Description Here")
    if prompt:
        st.write(f"Job: {prompt}")
        st.session_state.cover_letter_gpt4.generate_cover_letter(prompt)
        st.header("Cover Letter:")
        st.write(st.session_state.cover_letter_gpt4.cover_letter)
        doc_buffer=st.session_state.cover_letter_gpt4.create_word_doc()
        st.download_button(
        label="Download Cover Letter",
        data=doc_buffer,
        file_name=st.session_state.cover_letter_gpt4.file_name,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
def recruiter_message():
    st.title("Recruiter Message")
    st.header("Bot:")
    st.write("Give context for message or paste job description")
    prompt = st.chat_input("Enter Here")
    if prompt:
        st.header("User:")
        st.write(prompt)
        st.session_state.recruiter_message_gpt4.generate_message(prompt)
        st.header("Bot:")
        st.code(f"{st.session_state.recruiter_message_gpt4.message}",language="text")

def optimize_resume():
    st.title("Optimize Resume for a job")
    st.header("Bot:")
    st.write("Paste job description")
    prompt = st.chat_input("Enter Job Description Here")
    if prompt:
        st.header("User:")
        st.write(prompt)
        st.session_state.optimize_resume_gpt4.optimize_resume(prompt)
        st.header("Bot:")
        st.session_state.optimize_resume_gpt4.render_output()
def main():
    st.sidebar.title('Navigation')
    selected = st.sidebar.radio('Go to', ["Upload Resume","Cover Letter - GPT3.5","Cover Letter - GPT4","Recruiter Message - GPT4","Optimize Resume - GPT4"])
    if selected=="Upload Resume":
        upload_pdf()
    elif selected=="Cover Letter - GPT3.5":
        if 'cover_letter_gpt3' not in st.session_state.keys():
            st.session_state.cover_letter_gpt3=st.session_state.job_bot.CoverLetterBot("gpt-3.5-turbo",st.session_state.job_bot)
        cover_letter_gpt3()
    elif selected=="Cover Letter - GPT4":
        if 'cover_letter_gpt4' not in st.session_state.keys():
            st.session_state.cover_letter_gpt4=st.session_state.job_bot.CoverLetterBot("gpt-4-turbo",st.session_state.job_bot)
        cover_letter_gpt4()
    elif selected=="Recruiter Message - GPT4":
        if 'recruiter_message_gpt4' not in st.session_state.keys():
            st.session_state.recruiter_message_gpt4=st.session_state.job_bot.RecruiterMessage("gpt-4-turbo",st.session_state.job_bot)
        recruiter_message()
    elif selected=="Optimize Resume - GPT4":
        if 'optimize_resume_gpt4' not in st.session_state.keys():
            st.session_state.optimize_resume_gpt4=st.session_state.job_bot.OptimizeResume("gpt-4-turbo",st.session_state.job_bot)
        optimize_resume()


if __name__ == "__main__":
    main()