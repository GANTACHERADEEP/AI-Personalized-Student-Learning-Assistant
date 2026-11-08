"""tasks.py - defines what each agent must do.

Placeholders like {student_name} are filled in by crew.kickoff(inputs=...).
"""
from crewai import Agent, Task

STUDENT_PROFILE = """Student profile:
- Name: {student_name}
- Subject: {subject}
- Topics to learn: {topics}
- Difficult topics: {difficult_topics}
- Current knowledge level: {knowledge_level}
- Study hours per day: {hours_per_day}
- Exam date: {exam_date} ({days_left} days from today, {today})
"""


def create_tasks(agents: dict) -> list[Task]:
    analysis_task = Task(
        description=(
            STUDENT_PROFILE
            + "\nAnalyze this student's learning needs. You must:\n"
            "1. Identify which topics are difficult and why.\n"
            "2. Assign a priority (High/Medium/Low) to every topic.\n"
            "3. List prerequisite concepts for each topic.\n"
            "4. Recommend the best order to learn the topics."
        ),
        expected_output=(
            "A markdown report with: a priority table (Topic | Difficulty | "
            "Priority | Prerequisites) and a numbered recommended learning order "
            "with one-line reasons."
        ),
        agent=agents["analyzer"],
    )

    planning_task = Task(
        description=(
            STUDENT_PROFILE
            + "\nUsing the analysis from the previous task, create a daily study "
            "schedule from today until the exam. You must:\n"
            "1. Respect the available hours per day.\n"
            "2. Give more time to difficult and high-priority topics.\n"
            "3. Include regular revision sessions and a final revision phase.\n"
            "4. Keep the plan realistic for the number of days left. If time is "
            "very short, say so and focus on the most important topics."
        ),
        expected_output=(
            "A markdown study plan: a day-by-day (or week-by-week with daily "
            "details) schedule listing topic, activity and hours per day, "
            "revision sessions marked clearly, and a short summary of time "
            "allocation."
        ),
        agent=agents["planner"],
        context=[analysis_task],
    )

    resources_task = Task(
        description=(
            STUDENT_PROFILE
            + "\nUsing the analysis and the study plan, recommend how the student "
            "should learn. You must:\n"
            "1. Suggest learning methods for each main topic.\n"
            "2. Recommend practice activities.\n"
            "3. Write a short quiz (3-5 questions with answers) for each topic.\n"
            "4. Suggest revision techniques."
        ),
        expected_output=(
            "A markdown document with sections: Learning Methods, Practice "
            "Activities, Topic-wise Quizzes (with answers), and Revision "
            "Techniques."
        ),
        agent=agents["advisor"],
        context=[analysis_task, planning_task],
    )

    return [analysis_task, planning_task, resources_task]