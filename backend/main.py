
import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.utils import save_uploaded_file
from backend.whisper_service import transcribe_audio
from backend.gemini_service import generate_study_material
from backend.pdf_service import create_pdf
from backend.models import StudyMaterialResponse
from backend.chat_service import ask_question


app = FastAPI(title="ECE Smart Lecture Assistant")

# Store the latest transcript and PDF path in memory.
latest_transcript = ""
latest_pdf_path = ""


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "ECE Smart Lecture Assistant Backend Running!"
    }


@app.post("/upload", response_model=StudyMaterialResponse)
def upload_audio(file: UploadFile = File(...)):
    global latest_transcript, latest_pdf_path

    try:
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Please upload a valid audio file."
            )

        # 1. Save uploaded audio
        file_path = save_uploaded_file(file)

        # 2. Transcribe audio
        transcript = transcribe_audio(file_path)

        # 3. Save transcript for AI chat
        latest_transcript = transcript

        # 4. Generate AI study material
        study_material = generate_study_material(transcript)

        summary = study_material["summary"]
        key_points = study_material["key_points"]
        mcqs = study_material["mcqs"]
        viva = study_material["viva"]

        # 5. Generate PDF on the backend server
        pdf_path = create_pdf(
            filename=os.path.splitext(
                os.path.basename(file.filename)
            )[0],
            transcript=transcript,
            summary=summary,
            key_points=key_points,
            mcqs=mcqs,
            viva=viva
        )

        # Store the absolute path for the download endpoint
        latest_pdf_path = os.path.abspath(pdf_path)

        if not os.path.isfile(latest_pdf_path):
            raise FileNotFoundError(
                f"PDF generation completed, but file was not found: "
                f"{latest_pdf_path}"
            )

        # 6. Return study material and PDF download URL
        return StudyMaterialResponse(
            message="Upload Successful!",
            filename=file.filename,
            transcript=transcript,
            summary=summary,
            key_points=key_points,
            mcqs=mcqs,
            viva=viva,
            pdf="/pdf"
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing lecture: {str(e)}"
        ) from e

    finally:
        file.file.close()


@app.get("/pdf")
def download_pdf():
    """Serve the most recently generated PDF to the frontend."""
    if not latest_pdf_path or not os.path.isfile(latest_pdf_path):
        raise HTTPException(
            status_code=404,
            detail="PDF not found. Please upload a lecture again."
        )

    return FileResponse(
        path=latest_pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(latest_pdf_path),
        content_disposition_type="attachment"
    )


@app.post("/chat")
def chat(request: ChatRequest):
    if not latest_transcript:
        raise HTTPException(
            status_code=400,
            detail="Please upload a lecture first."
        )

    try:
        answer = ask_question(
            latest_transcript,
            request.question
        )

        return {
            "question": request.question,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat question: {str(e)}"
        ) from e
