import streamlit as st


def show_tabs(data):
    """
    Displays all study material tabs.
    """

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📄 Transcript",
            "📝 Study Notes",
            "📌 Key Points",
            "❓ MCQs",
            "🎤 Viva Questions",
        ]
    )

    # -----------------------------
    # Transcript
    # -----------------------------
    with tab1:

        st.markdown(
            """
            <div class="section-title">
                📄 Lecture Transcript
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("View Full Transcript", expanded=True):

            st.text_area(
                "",
                data["transcript"],
                height=450,
                disabled=True,
            )

    # -----------------------------
    # Study Notes
    # -----------------------------
    with tab2:

        st.markdown(
            """
            <div class="section-title">
                📝 AI Study Notes
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(data["summary"])

    # -----------------------------
    # Key Points
    # -----------------------------
    with tab3:

        st.markdown(
            """
            <div class="section-title">
                📌 Key Points
            </div>
            """,
            unsafe_allow_html=True,
        )

        for point in data["key_points"]:

            st.success(point)

    # -----------------------------
    # MCQs
    # -----------------------------
    with tab4:

        st.markdown(
            """
            <div class="section-title">
                ❓ Practice MCQs
            </div>
            """,
            unsafe_allow_html=True,
        )

        for i, mcq in enumerate(data["mcqs"], start=1):

            with st.container():

                st.markdown(f"### Question {i}")

                st.write(mcq["question"])

                for option in mcq["options"]:

                    st.write(f"• {option}")

                st.success(f"✅ Correct Answer: {mcq['answer']}")

                st.divider()

    # -----------------------------
    # Viva Questions
    # -----------------------------
    with tab5:

        st.markdown(
            """
            <div class="section-title">
                🎤 Viva Questions
            </div>
            """,
            unsafe_allow_html=True,
        )

        for i, question in enumerate(data["viva"], start=1):

            st.info(f"Q{i}. {question}")