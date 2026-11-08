\# AI-Based Personalized Student Learning Assistant (CrewAI)



Three CrewAI agents (Learning Analyzer, Study Planner, Resource Advisor)

run sequentially to create a personalized study plan in a Streamlit app.



\## Setup

1\. Use Python 3.10 to 3.13.

2\. Create and activate a virtual environment: python -m venv venv

&#x20;  (Windows: venv\\Scripts\\activate / macOS-Linux: source venv/bin/activate)

3\. Install: pip install -r requirements.txt

4\. Copy .env.example to .env and set GEMINI\_API\_KEY

&#x20;  (free key: https://aistudio.google.com/apikey)



\## Run

streamlit run app.py



\## Files

\- agents.py: LLM and the 3 agents

\- tasks.py: the 3 tasks and their dependencies

\- crew.py: sequential Crew + error handling

\- app.py: Streamlit interface

