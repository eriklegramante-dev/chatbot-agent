"""
Mathematician agent module using CrewAI with Groq API fixes.
"""

import os
from dotenv import load_dotenv
from crewai import LLM, Agent, Crew, Task
from src.tools.tools import add, divide, multiply, subtract

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

llm_config = LLM(
    model="openai/llama-3.1-8b-instant",
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1",
    temperature=0.1,
)


def run_mathematician(user_prompt: str, chat_history: str = "") -> str:
    """
    Executes the mathematical agent with robust fallback handling.

    :param user_prompt: Current message sent by user.
    :param chat_history: Formatted context string.
    :return: Calculation result string.
    """
    mathematician = Agent(
        role="Mathematical Calculator",
        goal="Perform accurate mathematical calculations using available tools.",
        backstory="You are a precise calculation execution engine. Always use provided tools.",
        tools=[add, subtract, multiply, divide],
        allow_delegation=False,
        llm=llm_config,
        max_iter=5,
        verbose=False,
    )

    task = Task(
        description=(
            f"Context History:\n{chat_history}\n\n"
            f"User Request: '{user_prompt}'\n\n"
            "Instructions:\n"
            "1. Identify the numbers and operation required.\n"
            "2. Execute the corresponding tool (add, subtract, multiply, divide).\n"
            "3. State the numeric result clearly."
        ),
        expected_output="The numerical result of the mathematical operation.",
        agent=mathematician,
    )

    crew = Crew(agents=[mathematician], tasks=[task], cache=False, verbose=False)

    result = crew.kickoff()

    output_text = str(result.raw if hasattr(result, "raw") else result).strip()

    if not output_text or output_text.lower() == "none":
        return "Calculation could not be completed."

    return output_text