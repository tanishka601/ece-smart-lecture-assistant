import os
import json

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_study_material(transcript: str):

    prompt = f"""
You are an expert engineering professor.

Read the following lecture transcript carefully.

Return ONLY valid JSON.

The JSON must follow exactly this format:

{{
  "summary": "Detailed study notes in Markdown",

  "key_points": [
    "Point 1",
    "Point 2",
    "Point 3",
    "Point 4",
    "Point 5",
    "Point 6",
    "Point 7",
    "Point 8"
  ],

  "mcqs": [
    {{
      "question": "",
      "options": [
        "",
        "",
        "",
        ""
      ],
      "answer": ""
    }}
  ],

  "viva": [
    "",
    "",
    "",
    "",
    ""
  ]
}}

Lecture Transcript:

{transcript}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")

    return json.loads(text)