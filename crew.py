"""crew.py - builds the Crew and runs the sequential workflow."""
from datetime import date

from crewai import Crew, Process

from agents import build_llm, create_agents
from tasks import create_tasks


class StudyCrewError(Exception):
    """Raised with a friendly message when the crew cannot run."""


def run_study_crew(student: dict) -> dict:
    """Run the three agents and return their outputs plus a combined plan.

    `student` needs: name, subject, topics, difficult_topics,
    knowledge_level, hours_per_day, exam_date (a datetime.date).
    """
    today = date.today()
    days_left = (student["exam_date"] - today).days
    if days_left < 1:
        raise StudyCrewError("The exam date must be in the future.")

    inputs = {
        "student_name": student["name"],
        "subject": student["subject"],
        "topics": student["topics"],
        "difficult_topics": student["difficult_topics"] or "None specified",
        "knowledge_level": student["knowledge_level"],
        "hours_per_day": student["hours_per_day"],
        "exam_date": student["exam_date"].isoformat(),
        "days_left": days_left,
        "today": today.isoformat(),
    }

    try:
        llm = build_llm()
        agents = create_agents(llm)
        tasks = create_tasks(agents)

        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=False,
        )
        result = crew.kickoff(inputs=inputs)
    except ValueError as err:  # e.g. missing API key
        raise StudyCrewError(str(err)) from err
    except Exception as err:  # network, quota, invalid key, model errors
        raise StudyCrewError(f"The AI crew failed: {err}") from err

    outputs = [t.raw for t in result.tasks_output]
    if len(outputs) != 3:
        raise StudyCrewError("The crew returned an unexpected result. Try again.")

    combined = (
        f"# Personalized Study Plan for {student['name']}\n\n"
        f"**Subject:** {student['subject']}  \n"
        f"**Exam date:** {inputs['exam_date']} ({days_left} days left)  \n"
        f"**Study hours per day:** {student['hours_per_day']}\n\n"
        f"---\n\n## 1. Learning Analysis\n\n{outputs[0]}\n\n"
        f"---\n\n## 2. Study Schedule\n\n{outputs[1]}\n\n"
        f"---\n\n## 3. Learning Resources & Quizzes\n\n{outputs[2]}\n"
    )

    return {
        "analysis": outputs[0],
        "schedule": outputs[1],
        "resources": outputs[2],
        "combined": combined,
    }