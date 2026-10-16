from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from backend.utils import save_uploaded_file
from backend.whisper_service import transcribe_audio
from backend.gemini_service import generate_study_material
from backend.pdf_service import create_pdf
from backend.models import StudyMaterialResponse
from backend.chat_service import ask_question

app = FastAPI()

# Store the latest transcript in memory
latest_transcript = ""


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "ECE Smart Lecture Assistant Backend Running!"
    }


@app.post("/upload", response_model=StudyMaterialResponse)
def upload_audio(file: UploadFile = File(...)):

    global latest_transcript

    try:

        # Save uploaded file
        file_path = save_uploaded_file(file)

        # Transcribe audio
        transcript = transcribe_audio(file_path)

        # Save transcript for chat
        latest_transcript = transcript

        # Generate AI study material
        study_material = generate_study_material(transcript)

        summary = study_material["summary"]
        key_points = study_material["key_points"]
        mcqs = study_material["mcqs"]
        viva = study_material["viva"]

        # Create PDF
        pdf_path = create_pdf(
            filename=file.filename.split(".")[0],
            transcript=transcript,
            summary=summary,
            key_points=key_points,
            mcqs=mcqs,
            viva=viva
        )

        return StudyMaterialResponse(
            message="Upload Successful!",
            filename=file.filename,
            transcript=transcript,
            summary=summary,
            key_points=key_points,
            mcqs=mcqs,
            viva=viva,
            pdf=pdf_path
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing lecture: {str(e)}"
        )


@app.post("/chat")
def chat(request: ChatRequest):

    global latest_transcript

    if latest_transcript == "":
        raise HTTPException(
            status_code=400,
            detail="Please upload a lecture first."
        )

    answer = ask_question(
        latest_transcript,
        request.question
    )

    return {
        "question": request.question,
        "answer": answer
    }