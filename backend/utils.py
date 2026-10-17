
import os
import uuid
from pathlib import Path


# Project root: the directory containing backend/ and frontend/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Use the configured upload directory if available; otherwise use uploads/
try:
    from backend.config import UPLOAD_DIR as CONFIG_UPLOAD_DIR
    UPLOAD_DIR = Path(CONFIG_UPLOAD_DIR)
    if not UPLOAD_DIR.is_absolute():
        UPLOAD_DIR = PROJECT_ROOT / UPLOAD_DIR
except (ImportError, AttributeError, TypeError):
    UPLOAD_DIR = PROJECT_ROOT / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_file(uploaded_file):
    """
    Save a FastAPI UploadFile to the uploads directory.
    Returns the saved file's path as a string.
    """

    original_name = getattr(uploaded_file, "filename", None) or "lecture_audio"
    safe_name = os.path.basename(original_name)
    extension = Path(safe_name).suffix

    # Avoid collisions when different users upload files with the same name.
    unique_name = f"{uuid.uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / unique_name

    try:
        # FastAPI UploadFile exposes a file-like object.
        file_object = getattr(uploaded_file, "file", uploaded_file)

        # Handle both file objects and byte content.
        if isinstance(file_object, bytes):
            file_bytes = file_object
        else:
            file_object.seek(0)
            file_bytes = file_object.read()

        with file_path.open("wb") as output:
            output.write(file_bytes)

        return str(file_path)

    except Exception:
        # Remove an incomplete file if saving fails.
        if file_path.exists():
            file_path.unlink()
        raise
