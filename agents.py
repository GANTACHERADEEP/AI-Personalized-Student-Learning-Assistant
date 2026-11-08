"""agents.py - defines the LLM and the three CrewAI agents."""
import os

from crewai import Agent, LLM


def build_llm() -> LLM:
    """Create the LLM that all agents will use. The key comes from .env."""
    api_key = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "No API key found. Copy .env.example to .env and set GEMINI_API_KEY."
        )
    model = os.getenv("LLM_MODEL", "gemini/gemini-3.8-flash")
    return LLM(model=model, api_key=api_key, temperature=0.4)


def create_agents(llm: LLM) -> dict:
    """Create and return the three agents."""
    learning_analyzer = Agent(
        role="Learning Analyzer",
        goal=(
            "Analyze the student's topics, difficulty areas and knowledge level "
            "to decide priorities, prerequisites and the best learning order."
        ),
        backstory=(
            "You are an experienced academic mentor who quickly spots where "
            "students struggle and which concepts must be learned first."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    study_planner = Agent(
        role="Study Planner",
        goal=(
            "Build a realistic day-by-day study schedule that fits the student's "
            "daily hours and exam date, with enough time for hard topics and revision."
        ),
        backstory=(
            "You are a time-management expert who designs achievable study plans "
            "that avoid burnout and finish before the exam."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    resource_advisor = Agent(
        role="Learning Resource Advisor",
        goal=(
            "Recommend effective learning methods, practice activities, "
            "topic-wise quizzes and revision techniques."
        ),
        backstory=(
            "You are a learning-science coach who knows which study techniques "
            "work best for different subjects and levels."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    return {
        "analyzer": learning_analyzer,
        "planner": study_planner,
        "advisor": resource_advisor,
    }


