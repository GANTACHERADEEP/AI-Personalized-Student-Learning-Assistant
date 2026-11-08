"""app.py - Streamlit user interface."""
import os

# Optional: turn off CrewAI telemetry (set before importing crewai code)
os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")

from datetime import date, timedelta

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from crew import StudyCrewError, run_study_crew  # noqa: E402

st.set_page_config(page_title="Student Learning Assistant", page_icon="🎓", layout="wide")

st.title("🎓 AI Personalized Student Learning Assistant")
st.caption("Three CrewAI agents analyze your needs, plan your schedule and suggest resources.")

SUBJECTS = [
    "Mathematics", "Physics", "Chemistry", "Biology", "Computer Science",
    "Data Structures & Algorithms", "Machine Learning", "English",
    "History", "Economics", "Other",
]

with st.sidebar:
    st.header("How it works")
    st.markdown(
        "1. **Learning Analyzer** sets priorities and order\n"
        "2. **Study Planner** builds your daily schedule\n"
        "3. **Resource Advisor** suggests methods and quizzes"
    )
    if not (os.getenv("GEMINI_API_KEY") or os.getenv("LLM_API_KEY")):
        st.error("API key missing. Add GEMINI_API_KEY to your .env file.")

with st.form("student_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Student name")
        subject = st.selectbox("Subject", SUBJECTS)
        custom_subject = ""
        if subject == "Other":
            custom_subject = st.text_input("Enter your subject")
        level = st.select_slider(
            "Current knowledge level",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Beginner",
        )
    with col2:
        hours = st.number_input(
            "Available study hours per day", min_value=0.5, max_value=12.0,
            value=2.0, step=0.5,
        )
        exam_date = st.date_input(
            "Exam date",
            value=date.today() + timedelta(days=14),
            min_value=date.today() + timedelta(days=1),
        )

    topics = st.text_area("Topics to learn (comma-separated or one per line)", height=100)
    difficult = st.text_area("Difficult topics (optional)", height=80)
    submitted = st.form_submit_button("Generate Study Plan", type="primary")

if submitted:
    final_subject = custom_subject.strip() if subject == "Other" else subject
    if not name.strip() or not final_subject or not topics.strip():
        st.warning("Please fill in your name, subject and topics.")
    else:
        student = {
            "name": name.strip(),
            "subject": final_subject,
            "topics": topics.strip(),
            "difficult_topics": difficult.strip(),
            "knowledge_level": level,
            "hours_per_day": hours,
            "exam_date": exam_date,
        }
        try:
            with st.spinner("The agents are working... this can take 1-2 minutes."):
                st.session_state["result"] = run_study_crew(student)
                st.session_state["student_name"] = student["name"]
        except StudyCrewError as err:
            st.session_state.pop("result", None)
            st.error(str(err))

# Results stay visible after clicking download (Streamlit reruns the script)
result = st.session_state.get("result")
if result:
    st.success("Your study plan is ready!")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Full Plan", "🔍 Analysis", "📅 Schedule", "📚 Resources & Quizzes"]
    )
    with tab1:
        st.markdown(result["combined"])
    with tab2:
        st.markdown(result["analysis"])
    with tab3:
        st.markdown(result["schedule"])
    with tab4:
        st.markdown(result["resources"])

    file_name = f"study_plan_{st.session_state.get('student_name', 'student')}.md"
    st.download_button(
        "⬇️ Download study plan (.md)",
        data=result["combined"],
        file_name=file_name.replace(" ", "_"),
        mime="text/markdown",
    )