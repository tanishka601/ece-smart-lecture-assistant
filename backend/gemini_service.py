
import os
import json
import re

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Set it in your .env file locally "
        "or in Render's environment variables."
    )

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={
        "response_mime_type": "application/json",
        "temperature": 0.3,
    },
)


def _parse_json_response(text: str) -> dict:
    """Parse Gemini's response and validate its structure."""

    if not text or not text.strip():
        raise ValueError("Gemini returned an empty response.")

    text = text.strip()

    # Remove Markdown code fences, if present.
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)

    # First, try parsing the complete response.
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # If extra text surrounds the JSON, extract the JSON object.
        start = text.find("{")
        if start == -1:
            raise ValueError(
                "Gemini did not return a JSON object. Please try again."
            )

        try:
            data, _ = json.JSONDecoder().raw_decode(text[start:])
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Gemini returned invalid JSON. Please retry with a "
                "shorter transcript if the problem persists."
            ) from exc

    if not isinstance(data, dict):
        raise ValueError("Gemini response must be a JSON object.")

    required_fields = ("summary", "key_points", "mcqs", "viva")
    missing = [field for field in required_fields if field not in data]

    if missing:
        raise ValueError(
            f"Gemini response is missing required fields: {', '.join(missing)}"
        )

    if not isinstance(data["summary"], str):
        raise ValueError("The generated summary must be text.")

    if not isinstance(data["key_points"], list):
        raise ValueError("The generated key_points must be a list.")

    if not isinstance(data["mcqs"], list):
        raise ValueError("The generated mcqs must be a list.")

    if not isinstance(data["viva"], list):
        raise ValueError("The generated viva questions must be a list.")

    # Validate each MCQ before the frontend or PDF service uses it.
    for index, mcq in enumerate(data["mcqs"], start=1):
        if not isinstance(mcq, dict):
            raise ValueError(f"MCQ {index} is not a JSON object.")

        if not all(key in mcq for key in ("question", "options", "answer")):
            raise ValueError(
                f"MCQ {index} must contain question, options, and answer."
            )

        if not isinstance(mcq["options"], list):
            raise ValueError(f"Options for MCQ {index} must be a list.")

    return data


def generate_study_material(transcript: str) -> dict:
    """Generate study notes, key points, MCQs, and viva questions."""

    if not transcript or not transcript.strip():
        raise ValueError("The lecture transcript is empty.")

    prompt = """
You are an expert engineering professor.

Create accurate, useful study material from the lecture transcript.
Do not invent facts that are unsupported by the lecture.

Return a JSON object with exactly these four fields:

{
  "summary": "Detailed study notes in Markdown",
  "key_points": [
    "Important point 1",
    "Important point 2"
  ],
  "mcqs": [
    {
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": "The correct option text"
    }
  ],
  "viva": [
    "Viva question 1",
    "Viva question 2"
  ]
}

Requirements:
- Provide around 8 key points.
- Provide 5 multiple-choice questions, each with 4 options.
- Provide 5 viva questions.
- Ensure every MCQ has one clearly correct answer.
- Use double quotes for JSON strings.
- Escape special characters correctly.
- Do not add comments or text outside the JSON object.
- Put the study notes in the summary field.

LECTURE TRANSCRIPT:
"""

    full_prompt = prompt + "\n" + transcript

    try:
        response = model.generate_content(full_prompt)
        response_text = getattr(response, "text", None)

        if not response_text:
            raise ValueError(
                "Gemini returned no text. The response may have been blocked."
            )

        return _parse_json_response(response_text)

    except Exception as exc:
        # Preserve a useful error message for the backend.
        raise RuntimeError(
            f"Failed to generate study material: {exc}"
        ) from exc
