"""
Mathematician Agent Module.

This module defines the Mathematician Agent using CrewAI, responsible for
executing precise mathematical computations by dynamically leveraging arithmetic tools.
"""

import os 
import logging
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()
logger = logging.getLogger(__name__)

free_llm = LLM(
    model="gemini/gemini-3.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)


def run_mathematician(user_prompt: str, chat_history: str = "") -> str:
    mathematician_agent = Agent(
        role="Senior Mathematician",
        goal="Solve mathematical expressions accurately, using conversation history for context when required.",
        backstory="You are a precise mathematical engine capable of tracking sequential calculations across multi-turn conversations.",
        llm=free_llm,
        verbose=True,
        allow_delegation=False
    )

    math_task = Task(
        description=f"""
        Analyze the current user prompt in conjunction with the conversation history.

        Current User Prompt: "{user_prompt}"
        Chat History Log: "{chat_history}"

        Instructions:
        1. If the input is a GREETING (e.g., 'hello', 'hi', 'olá'):
           - Return ONLY the tag: GREETING.
        2. If the user prompt refers to a previous operation or value (e.g., "now subtract 2", "add 5 to that", "subtraia por 2"):
           - Extract the previous result from the Chat History Log.
           - Apply the new mathematical operation to that value.
           - Show the breakdown (e.g., 64 - 2 = 62) and provide the final numeric answer.
        3. If it is a standalone mathematical expression:
           - Solve it directly step-by-step.
        """,
        expected_output="Either 'GREETING' or the step-by-step mathematical resolution and final answer.",
        agent=mathematician_agent
    )

    crew = Crew(
        agents=[mathematician_agent],
        tasks=[math_task]
    )

    result = crew.kickoff()
    return str(result)