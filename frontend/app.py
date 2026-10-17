
import os
import html

import requests
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ECE Smart Lecture Assistant",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# BACKEND CONFIGURATION
# --------------------------------------------------

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://ece-smart-lecture-backend.onrender.com"
).rstrip("/")


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
.metric-card {
    padding: 15px;
    border-radius: 12px;
    background: #f7f7f7;
    border: 1px solid #ddd;
}

.chat-user {
    background: #dbeaaf;
    color: #202020;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 8px;
    overflow-wrap: anywhere;
}

.chat-ai {
    background: #f3f4f6;
    color: #202020;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 15px;
    overflow-wrap: anywhere;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "data" not in st.session_state:
    st.session_state.data = None

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def upload_audio(uploaded_file):
    """Upload audio and generate study material."""

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

        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        st.error(
            "The request timed out. Your audio may be long. "
            "Please try again."
        )

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to the backend. Please check the "
            "Render service and try again."
        )

    except requests.exceptions.HTTPError:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text

        st.error(f"Lecture processing failed: {detail}")

    except (requests.exceptions.RequestException, ValueError) as exc:
        st.error(f"Could not process the response: {exc}")

    return None


def download_pdf():
    """Retrieve the PDF from the backend over HTTPS."""

    try:
        response = requests.get(
            f"{BACKEND_URL}/pdf",
            timeout=60
        )

        response.raise_for_status()

        content_type = response.headers.get("content-type", "")

        if "application/pdf" not in content_type.lower():
            st.error("The backend did not return a PDF file.")
            return None

        return response.content

    except requests.exceptions.Timeout:
        st.error("PDF download timed out. Please try again.")

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the backend to download the PDF.")

    except requests.exceptions.HTTPError:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text

        st.error(f"PDF download failed: {detail}")

    except requests.exceptions.RequestException as exc:
        st.error(f"PDF download failed: {exc}")

    return None


def ask_ai(question):
    """Send a question to the deployed backend."""

    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"question": question},
            timeout=120
        )

        response.raise_for_status()
        return response.json().get("answer")

    except requests.exceptions.Timeout:
        st.error("The AI response timed out. Please try again.")

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the backend. Please try again.")

    except requests.exceptions.HTTPError:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text

        st.error(f"Chat request failed: {detail}")

    except (requests.exceptions.RequestException, ValueError) as exc:
        st.error(f"Chat request failed: {exc}")

    return None


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("📚 Navigation")

    st.success("Project Progress")
    st.progress(0.80)
    st.caption("80% Complete")

    st.write("✅ Upload Audio")
    st.write("✅ AI Transcription")
    st.write("✅ AI Study Notes")
    st.write("✅ Key Points")
    st.write("✅ MCQs")
    st.write("✅ Viva Questions")
    st.write("✅ PDF Export")
    st.write("✅ AI Chat")


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.title("🎓 ECE Smart Lecture Assistant")

st.write(
    "Convert lecture recordings into AI-powered study material."
)

st.divider()


# --------------------------------------------------
# AUDIO UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Lecture Audio",
    type=["mp3", "wav", "m4a"],
    help="Upload an MP3, WAV, or M4A lecture recording."
)

if uploaded_file:
    st.success(f"Selected File: {uploaded_file.name}")

    if st.button(
        "🚀 Generate AI Study Material",
        use_container_width=True
    ):
        with st.spinner(
            "Processing audio, generating study material, and creating PDF..."
        ):
            result = upload_audio(uploaded_file)

            if result is not None:
                st.session_state.data = result
                st.session_state.uploaded = True
                st.session_state.chat_history = []
                st.session_state.pdf_bytes = None

                st.rerun()


# --------------------------------------------------
# DISPLAY GENERATED STUDY MATERIAL
# --------------------------------------------------

if st.session_state.uploaded and st.session_state.data:

    data = st.session_state.data

    word_count = len(data.get("transcript", "").split())
    key_count = len(data.get("key_points", []))
    mcq_count = len(data.get("mcqs", []))
    viva_count = len(data.get("viva", []))

    st.success("Lecture processed successfully!")

    # Dashboard metrics
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📝 Words", word_count)
    c2.metric("📌 Key Points", key_count)
    c3.metric("❓ MCQs", mcq_count)
    c4.metric("🎤 Viva", viva_count)

    st.divider()

    # --------------------------------------------------
    # PDF EXPORT
    # --------------------------------------------------

    st.subheader("📄 Export Study Material")

    if st.session_state.pdf_bytes is None:
        if st.button(
            "Prepare PDF Download",
            use_container_width=True
        ):
            with st.spinner("Fetching your PDF from the backend..."):
                pdf_content = download_pdf()

                if pdf_content is not None:
                    st.session_state.pdf_bytes = pdf_content
                    st.rerun()

    if st.session_state.pdf_bytes is not None:
        st.download_button(
            label="📄 Download PDF Notes",
            data=st.session_state.pdf_bytes,
            file_name="Lecture_Notes.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.divider()

    # --------------------------------------------------
    # CONTENT TABS
    # --------------------------------------------------

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📄 Transcript",
        "📝 Study Notes",
        "📌 Key Points",
        "❓ MCQs",
        "🎤 Viva",
        "💬 AI Chat"
    ])

    # Transcript
    with tab1:
        st.subheader("Lecture Transcript")

        with st.expander("View Transcript", expanded=True):
            st.text_area(
                "Transcript",
                value=data.get("transcript", ""),
                height=400,
                label_visibility="collapsed"
            )

    # Study Notes
    with tab2:
        st.subheader("AI-Generated Study Notes")
        st.markdown(data.get("summary", "No study notes available."))

    # Key Points
    with tab3:
        st.subheader("Important Key Points")

        for index, point in enumerate(
            data.get("key_points", []),
            start=1
        ):
            st.success(f"{index}. {point}")

    # MCQs
    with tab4:
        st.subheader("Multiple-Choice Questions")

        for index, mcq in enumerate(
            data.get("mcqs", []),
            start=1
        ):
            st.markdown(f"### Question {index}")
            st.write(mcq.get("question", ""))

            for option in mcq.get("options", []):
                st.write(f"• {option}")

            st.success(f"Answer: {mcq.get('answer', 'Not provided')}")
            st.divider()

    # Viva
    with tab5:
        st.subheader("Viva Questions")

        for index, question in enumerate(
            data.get("viva", []),
            start=1
        ):
            st.write(f"🎤 **{index}.** {question}")

    # AI Chat
    with tab6:
        st.subheader("💬 Ask Questions About This Lecture")

        st.caption(
            "Ask questions about the uploaded lecture and its concepts."
        )

        with st.form("chat_form", clear_on_submit=True):
            question = st.text_input(
                "Ask your question",
                placeholder="e.g. Explain the main concepts in this lecture",
                key="chat_question"
            )

            submitted = st.form_submit_button(
                "Ask AI",
                use_container_width=True
            )

        if submitted:
            if question.strip():
                with st.spinner("Generating your answer..."):
                    answer = ask_ai(question.strip())

                if answer:
                    st.session_state.chat_history.append({
                        "question": question.strip(),
                        "answer": answer
                    })
            else:
                st.warning("Please enter a question.")

        # Display chat history
        for chat in st.session_state.chat_history:
            safe_question = html.escape(chat["question"])
            safe_answer = html.escape(str(chat["answer"])).replace(
                "\n", "<br>"
            )

            st.markdown(
                f"""
                <div class="chat-user">
                    <b>🙋 You</b><br>{safe_question}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="chat-ai">
                    <b>🤖 AI</b><br>{safe_answer}
                </div>
                """,
                unsafe_allow_html=True
            )
