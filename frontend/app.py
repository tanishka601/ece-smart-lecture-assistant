
import streamlit as st
import requests

st.set_page_config(
    page_title="ECE Smart Lecture Assistant",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
.metric-card{
    padding:15px;
    border-radius:12px;
    background:#f7f7f7;
    border:1px solid #ddd;
}
.chat-user{
    background:#dbeaafe;
    padding:12px;
    border-radius:10px;
    margin-bottom:8px;
}
.chat-ai{
    background:#f3f4f6;
    padding:12px;
    border-radius:10px;
    margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

if "data" not in st.session_state:
    st.session_state.data=None
if "uploaded" not in st.session_state:
    st.session_state.uploaded=False
if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

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

st.title("🎓 ECE Smart Lecture Assistant")
st.write("Convert lecture recordings into AI-powered study material.")
st.divider()

uploaded_file = st.file_uploader(
    "Upload Lecture Audio",
    type=["mp3","wav","m4a"]
)

if uploaded_file:
    st.success(f"Selected File: {uploaded_file.name}")

    if st.button("🚀 Generate AI Study Material", use_container_width=True):
        progress = st.progress(0)
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        progress.progress(20)
        response = requests.post("http://127.0.0.1:8000/upload", files=files)
        progress.progress(100)

        if response.status_code == 200:
            st.session_state.data = response.json()
            st.session_state.uploaded = True
            st.session_state.chat_history = []
            st.rerun()
        else:
            st.error(response.text)

if st.session_state.uploaded:

    data = st.session_state.data

    word_count = len(data["transcript"].split())
    key_count = len(data["key_points"])
    mcq_count = len(data["mcqs"])
    viva_count = len(data["viva"])

    st.success("Lecture processed successfully!")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("📝 Words", word_count)
    c2.metric("📌 Key Points", key_count)
    c3.metric("❓ MCQs", mcq_count)
    c4.metric("🎤 Viva", viva_count)

    with open(data["pdf"], "rb") as pdf:
        st.download_button(
            "📄 Download PDF Notes",
            pdf,
            file_name="Lecture_Notes.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.divider()

    tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs([
        "📄 Transcript",
        "📝 Study Notes",
        "📌 Key Points",
        "❓ MCQs",
        "🎤 Viva",
        "💬 AI Chat"
    ])

    with tab1:
        with st.expander("View Transcript", expanded=True):
            st.text_area("", data["transcript"], height=400)

    with tab2:
        st.markdown(data["summary"])

    with tab3:
        for p in data["key_points"]:
            st.success(p)

    with tab4:
        for i,mcq in enumerate(data["mcqs"],1):
            st.markdown(f"### Question {i}")
            st.write(mcq["question"])
            for option in mcq["options"]:
                st.write("•", option)
            st.success(f"Answer: {mcq['answer']}")
            st.divider()

    with tab5:
        for q in data["viva"]:
            st.write("🎤", q)

    with tab6:
        st.subheader("💬 Ask Questions About This Lecture")

        question = st.text_input("Ask your question", key="chat_question")

        if st.button("Ask AI", use_container_width=True):
            if question.strip():
                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={"question":question}
                )
                if response.status_code==200:
                    ans=response.json()["answer"]
                    st.session_state.chat_history.append({
                        "question":question,
                        "answer":ans
                    })
                    st.rerun()
                else:
                    st.error(response.text)
            else:
                st.warning("Please enter a question.")

        for chat in st.session_state.chat_history:
            st.markdown(f"<div class='chat-user'><b>🙋 You</b><br>{chat['question']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='chat-ai'><b>🤖 AI</b><br>{chat['answer']}</div>", unsafe_allow_html=True)
