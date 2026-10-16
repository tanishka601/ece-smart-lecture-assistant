import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def ask_question(
    transcript: str,
    question: str
):

    prompt = f"""
You are an engineering professor.

Answer ONLY using the lecture transcript.

If the answer is not present in the lecture,
reply:

"This topic was not covered in today's lecture."

Lecture:

{transcript}

Student Question:

{question}
"""

    response = model.generate_content(prompt)

    return response.text