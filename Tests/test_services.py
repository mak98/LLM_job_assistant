import pytest
from io import BytesIO
from bot_services.job_bot import JobBot

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
