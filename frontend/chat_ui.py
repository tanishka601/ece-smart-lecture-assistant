import streamlit as st
import requests


def show_chat(chat_history):
    """
    Display AI chat interface.
    """

    st.markdown(
        """
        <div class="section-title">
            💬 AI Lecture Assistant
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Ask questions only related to the uploaded lecture.")

    # -----------------------
    # Display Chat History
    # -----------------------

    if chat_history:

        for chat in chat_history:

            # User Bubble
            st.markdown(
                f"""
                <div class="user-bubble">

                <b>👤 You</b><br><br>

                {chat["question"]}

                </div>
                """,
                unsafe_allow_html=True,
            )

            # AI Bubble
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

    # -----------------------
    # Input
    # -----------------------

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

        if question.strip() == "":

            st.warning("Please enter a question.")

            return

        with st.spinner("AI is thinking..."):

            response = requests.post(

                "http://127.0.0.1:8000/chat",

                json={
                    "question": question
                }

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

            st.error(response.text)