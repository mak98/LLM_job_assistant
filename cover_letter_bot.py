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
        ret["Cover Letter"]=ret["Cover Letter"].replace("\\n","\n")
        print(ret,type(ret))
        return ret
class CoverLetterBot():
    def __init__(self,name):
        chat_model=ChatOpenAI(model_name=name,api_key=st.secrets.OPENAI_API_KEY)
        system_template=open('Prompts/prompt1.txt', 'r').read()
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
        self.resume=""
        self.file_name=""
    def parse_resume(self,pdf_file):
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            self.resume += page.extract_text()
        print(self.resume)
    def generate_cover_letter(self,job_description):
        self.bot_response=self.chain.run(resume=self.resume,job_description=job_description)
        self.cover_letter=self.bot_response.get("Cover Letter")
        self.file_name=f'Cover Letter-{self.bot_response.get("Job Title")}.docx'
        print(self.file_name)
    def create_word_doc(self):
        document = Document()
        print(self.cover_letter)
        paragraphs = self.cover_letter.split('\n')
        for paragraph in paragraphs:
            document.add_paragraph(paragraph)
        doc_buffer = BytesIO()
        document.save(doc_buffer)
        doc_buffer.seek(0)
        return doc_buffer
