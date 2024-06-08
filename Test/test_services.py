import pytest
from io import BytesIO
from langchain.schema import BaseOutputParser
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (SystemMessagePromptTemplate,HumanMessagePromptTemplate,ChatPromptTemplate)
from langchain.chains import LLMChain
from docx import Document
import PyPDF2
import json
from io import BytesIO
import streamlit as st


class OutputParser(BaseOutputParser):
    def parse(self,text:str):
        ret=json.loads(text.strip())
        for i in ret.keys():
            ret[i]=ret[i].replace("\\n","\n")
        return ret
class JSONOutputParser(BaseOutputParser):
    def parse(self,text:str):
        ret=json.loads(text.strip())
        return ret
class JobBot():
    def __init__(self):
        self.resume=""
    def parse_resume(self,pdf_file):
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            self.resume += page.extract_text()
    
    class CoverLetterBot():
        def __init__(self,name,job_bot):
            self.job_bot=job_bot
            chat_model=ChatOpenAI(model_name=name,api_key=st.secrets.OPENAI_API_KEY)
            system_template=open('Prompts/prompt_cover_letter.txt', 'r').read()
            human_template="Resume:{resume}\nJob Description:{job_description}"
            system_message_prompt=SystemMessagePromptTemplate.from_template(system_template)
            human_message_prompt=HumanMessagePromptTemplate.from_template(human_template)
            chat_prompt=ChatPromptTemplate.from_messages([system_message_prompt,human_message_prompt])
            self.chain=LLMChain(
                                llm=chat_model,
                                prompt=chat_prompt,
                                output_parser=OutputParser()
                                )
            self.bot_response=""
            self.cover_letter=""
            self.file_name=""
        def generate_cover_letter(self,job_description):
            self.bot_response=self.chain.run(resume=self.job_bot.resume,job_description=job_description)
            self.cover_letter=self.bot_response.get("Cover Letter")
            self.file_name=f'Cover Letter-{self.bot_response.get("Job Title")}.docx'
        def create_word_doc(self):
            document = Document()
            paragraphs = self.cover_letter.split('\n')
            for paragraph in paragraphs:
                document.add_paragraph(paragraph)
            doc_buffer = BytesIO()
            document.save(doc_buffer)
            doc_buffer.seek(0)
            return doc_buffer

    class RecruiterMessage():
        def __init__(self,name,job_bot):
            self.job_bot=job_bot
            chat_model=ChatOpenAI(model_name=name,api_key=st.secrets.OPENAI_API_KEY)
            system_template=open('Prompts/prompt_recruiter_message.txt', 'r').read()
            human_template="Resume:{resume}\nContext:{context}"
            system_message_prompt=SystemMessagePromptTemplate.from_template(system_template)
            human_message_prompt=HumanMessagePromptTemplate.from_template(human_template)
            chat_prompt=ChatPromptTemplate.from_messages([system_message_prompt,human_message_prompt])
            self.chain=LLMChain(
                                llm=chat_model,
                                prompt=chat_prompt,
                                output_parser=OutputParser()
                                )
            self.context=""
            self.message=""
            self.bot_response=""
        def generate_message(self,context):
            self.context+="\nUser message:"+context
            self.bot_response=self.chain.run(resume=self.job_bot.resume,context=self.context)
            self.message=self.bot_response["message"]
            self.context+="\n Bot response:"+self.message
    
    class OptimizeResume():
        def __init__(self,name,job_bot):
            self.job_bot=job_bot
            chat_model=ChatOpenAI(model_name=name,api_key=st.secrets.OPENAI_API_KEY)
            system_template=open('Prompts/prompt_resume_optimize.txt', 'r').read()
            human_template="Resume:{resume}\nJob Description:{job_description}"
            system_message_prompt=SystemMessagePromptTemplate.from_template(system_template)
            human_message_prompt=HumanMessagePromptTemplate.from_template(human_template)
            chat_prompt=ChatPromptTemplate.from_messages([system_message_prompt,human_message_prompt])
            self.chain=LLMChain(
                                llm=chat_model,
                                prompt=chat_prompt,
                                output_parser=JSONOutputParser()
                                )
            self.job_description=""
            self.bot_response=""
        def optimize_resume(self,job_description):
            self.job_description=job_description
            self.bot_response=self.chain.run(resume=self.job_bot.resume,job_description=job_description)
        def render_output(self):
            st.header(f'Job Match:{self.bot_response["Job match score"]}')
            skills_found_html = "<h2>Skills Found:</h2><ul>"
            for item in self.bot_response["Skills Found"]:
                skills_found_html += f"<li>{item}</li>"
            skills_found_html += "</ul>"

            skills_description_html = "<h2>Skills in Job Description:</h2><ul>"
            for item in self.bot_response["Job keywords"]:
                skills_description_html += f"<li>{item}</li>"
            skills_description_html += "</ul>"

            st.markdown(
                f"""
                <div style="display:flex">
                    <div style="flex:50%; padding-right:10px;">
                        {skills_found_html}
                    </div>
                    <div style="flex:50%;">
                        {skills_description_html}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.header("Missing Skills")
            list_html = "<ul>"
            for item in self.bot_response["missing skills"]:
                list_html += f"<li>{item}</li>"
            list_html += "</ul>"
            st.markdown(list_html, unsafe_allow_html=True)
            st.header("Suggested Resume Changes:")
            for i in self.bot_response["Suggestions"]:
                st.header(i)
                list_html = "<ul>"
                for item in self.bot_response["Suggestions"][i]:
                    list_html += f"<li>{item}</li>"
                list_html += "</ul>"
                st.markdown(list_html, unsafe_allow_html=True)


def test_parse_resume():
    job_bot = JobBot()
    with open('sample_resume.pdf', 'rb') as f:
        job_bot.parse_resume(BytesIO(f.read()))
    assert job_bot.resume != ""

def test_generate_cover_letter():
    job_bot = JobBot()
    job_bot.parse_resume(open('sample_resume.pdf', 'rb'))
    cover_letter_bot = JobBot.CoverLetterBot('gpt-3.5-turbo', job_bot)
    cover_letter_bot.generate_cover_letter('sample job description')
    assert cover_letter_bot.cover_letter != ""
    assert cover_letter_bot.file_name.endswith('.docx')
