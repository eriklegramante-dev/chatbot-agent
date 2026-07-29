"""
Mathematician Agent Module.

This module defines the Mathematician Agent using CrewAI, responsible for
executing precise mathematical computations by dynamically leveraging arithmetic tools.
"""


import logging
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from src.config.llm import get_llm

load_dotenv()
logger = logging.getLogger(__name__)

def run_mathematician(user_prompt: str, chat_history: str = "") -> str:
    mathematician_agent = Agent(
        role="Senior Mathematician",
        goal="Solve mathematical expressions accurately, maintaining context from previous calculation results in the chat history.",
        backstory="You are a precise mathematical engine. You look at the chat history log to find previous answers when the user gives follow-up commands.",
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )

    math_task = Task(
        description="""
        CHAT HISTORY LOG:
        {chat_history}

        CURRENT USER INPUT:
        {user_prompt}

        Instructions:
        1. CHECK THE CHAT HISTORY LOG FIRST.
        2. If CURRENT USER INPUT refers to a previous calculation (e.g., "agora subtraia por 2", "add 10 to that", "subtraia 2"):
           - Look at the CHAT HISTORY LOG for the LAST NUMERIC RESULT or equation (e.g., if history has "5 + 5 = 10", the previous result is 10).
           - Perform the new math operation on that previous result (e.g., 10 - 2 = 8).
           - Output the operation and the new final answer clearly (e.g., 10 - 2 = 8).
        3. If CURRENT USER INPUT is a new standalone math problem (e.g., "5 + 5"), solve it directly.
        4. If it is a simple greeting, output ONLY: GREETING.
        """,
        expected_output="The mathematical calculation breakdown using historical context if applicable, and final answer.",
        agent=mathematician_agent
    )

    crew = Crew(
        agents=[mathematician_agent],
        tasks=[math_task]
    )

    result = crew.kickoff(inputs={
        "user_prompt": user_prompt,
        "chat_history": chat_history if chat_history.strip() else "No previous history."
    })

    return str(result)