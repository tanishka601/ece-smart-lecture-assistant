
import streamlit as st
import requests
import os

BACKEND_URL = st.secrets.get(
    "BACKEND_URL",
    os.getenv(
        "BACKEND_URL",
        "http://127.0.0.1:8000"
    )
).rstrip("/")


def show_chat(chat_history):
    st.markdown(
        """
        <div class="section-title">
            💬 AI Lecture Assistant
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Ask questions only related to the uploaded lecture.")

    if chat_history:
        for chat in chat_history:
            st.markdown(
                f"""
                <div class="user-bubble">
                    <b>👤 You</b><br><br>
                    {chat["question"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="ai-bubble">
                    <b>🤖 AI Assistant</b><br><br>
                    {chat["answer"]}
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("Start the conversation by asking a question.")

    st.divider()

    question = st.text_input(
        "Ask a question",
        placeholder="Example: Explain Nyquist Sampling Theorem",
        key="chat_question",
    )

    ask = st.button(
        "🚀 Ask AI",
        use_container_width=True,
    )

    if ask:
        if not question.strip():
            st.warning("Please enter a question.")
            return

        try:
            with st.spinner("AI is thinking..."):
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"question": question},
                    timeout=300,
                )

            if response.status_code == 200:
                answer = response.json()["answer"]

                st.session_state.chat_history.append(
                    {
                        "question": question,
                        "answer": answer,
                    }
                )

                st.rerun()
            else:
                st.error(
                    f"Backend error ({response.status_code}): "
                    f"{response.text}"
                )

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the backend: {e}")
