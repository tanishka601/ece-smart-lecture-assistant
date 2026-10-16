import requests
import streamlit as st

# ----------------------------------
# Backend Configuration
# ----------------------------------

BACKEND_URL = "http://127.0.0.1:8000"


# ----------------------------------
# Upload Lecture Audio
# ----------------------------------

def upload_audio(uploaded_file):
    """
    Upload the selected lecture audio file to the backend.
    """

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
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

        st.error(response.text)
        return None

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to the backend.\n\n"
            "Make sure FastAPI is running on http://127.0.0.1:8000"
        )

        return None

    except Exception as e:

        st.error(f"Error: {e}")

        return None


# ----------------------------------
# Chat with AI
# ----------------------------------

def ask_ai(question):
    """
    Send a question to the AI chat endpoint.
    """

    try:

        response = requests.post(

            f"{BACKEND_URL}/chat",

            json={
                "question": question
            },

            timeout=300

        )

        if response.status_code == 200:

            return response.json()["answer"]

        st.error(response.text)

        return None

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to backend."
        )

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