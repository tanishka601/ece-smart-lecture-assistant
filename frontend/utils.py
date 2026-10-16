
import os
import requests
import streamlit as st

# ----------------------------------
# Backend Configuration
# ----------------------------------

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


# ----------------------------------
# Upload Lecture Audio
# ----------------------------------

def upload_audio(uploaded_file):
    """Upload lecture audio to the backend."""

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type or "application/octet-stream"
        )
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/upload",
            files=files,
            timeout=300
        )

        if response.status_code == 200:
            return response.json()

        st.error(f"Upload failed: {response.text}")
        return None

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to the backend. "
            "Check that the backend is running and BACKEND_URL is correct."
        )
        return None

    except requests.exceptions.Timeout:
        st.error("The upload timed out. Please try again.")
        return None

    except Exception as e:
        st.error(f"Error: {e}")
        return None


# ----------------------------------
# Chat with AI
# ----------------------------------

def ask_ai(question):
    """Send a question to the AI chat endpoint."""

    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"question": question},
            timeout=300
        )

        if response.status_code == 200:
            return response.json()["answer"]

        st.error(f"Chat failed: {response.text}")
        return None

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the backend.")
        return None

    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again.")
        return None

    except Exception as e:
        st.error(f"Error: {e}")
        return None


# ----------------------------------
# Initialize Session State
# ----------------------------------

def initialize_session():

    if "uploaded" not in st.session_state:
        st.session_state.uploaded = False

    if "data" not in st.session_state:
        st.session_state.data = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
