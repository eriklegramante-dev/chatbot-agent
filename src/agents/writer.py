"""
Writer agent module for formatting responses to users.
"""

import os
from dotenv import load_dotenv
from crewai import LLM, Agent, Crew, Task

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

llm_config = LLM(
    model="openai/llama-3.1-8b-instant",
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1",
    temperature=0.3,
    max_tokens=150,  
)


def run_writer(user_prompt: str, calc_result: str) -> str:
    """
    Formats raw numerical outputs or keywords into natural, short sentences.

    :param user_prompt: Original prompt from the user.
    :param calc_result: The raw numerical or status string to incorporate.
    :return: Formatted response string.
    """
    writer = Agent(
        role="Response Formatter",
        goal="Format raw numerical answers into concise, friendly responses in Portuguese.",
        backstory="You are a helpful assistant that communicates math results clearly and briefly.",
        allow_delegation=False,
        llm=llm_config,
        verbose=False,
    )

    task = Task(
        description=(
            f"User Prompt: '{user_prompt}'\n"
            f"Calculation Result: '{calc_result}'\n\n"
            "INSTRUCTIONS:\n"
            "1. Format the calculation result into a friendly, short sentence in Portuguese.\n"
            "2. Keep the response under 100 characters.\n"
            "3. Example: 'O resultado da sua conta é 9.'"
        ),
        expected_output="A concise formatted sentence in Portuguese presenting the result.",
        agent=writer,
    )

    crew = Crew(agents=[writer], tasks=[task], cache=False, verbose=False)
    result = crew.kickoff()
    return str(result.raw if hasattr(result, "raw") else result).strip()