import streamlit as st


def show_dashboard(data):
    """
    Displays the analytics dashboard.
    """

    transcript = data["transcript"]

    word_count = len(transcript.split())
    keypoint_count = len(data["key_points"])
    mcq_count = len(data["mcqs"])
    viva_count = len(data["viva"])

    st.markdown(
        """
        <div class="section-title">
            📊 Lecture Analytics
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    cards = [
        ("📝", word_count, "Words"),
        ("📌", keypoint_count, "Key Points"),
        ("❓", mcq_count, "MCQs"),
        ("🎤", viva_count, "Viva Questions"),
    ]

    for col, (icon, value, label) in zip([col1, col2, col3, col4], cards):

        with col:
            st.markdown(
                f"""
                <div class="dashboard-card">

                    <div style="font-size:40px;">
                        {icon}
                    </div>

                    <div class="metric-value">
                        {value}
                    </div>

                    <div class="metric-label">
                        {label}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="download-card">

            <h3 style="margin-bottom:5px;">
                📄 Export Study Material
            </h3>

            <p style="color:gray;">
                Download your AI-generated lecture notes.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    with open(data["pdf"], "rb") as pdf:

        st.download_button(
            "⬇ Download PDF Notes",
            pdf,
            file_name="Lecture_Notes.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    st.divider()