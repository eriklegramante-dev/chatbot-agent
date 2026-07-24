"""
Mathematician Agent Module.

This module defines the Mathematician Agent using CrewAI, responsible for
executing precise mathematical computations by dynamically leveraging arithmetic tools.
"""

import logging
import os
from typing import Optional
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from src.tools.tools import add, subtract, multiply, divide

load_dotenv()
logger = logging.getLogger(__name__)


def run_mathematician(
    user_message: str,
    chat_history: Optional[str] = "",
    context: Optional[str] = "",
    *args,
    **kwargs,
) -> str:
    """
    Executes the Mathematician Agent to evaluate mathematical requests.

    Args:
        user_message (str): The primary prompt or calculation request from the user.
        chat_history (Optional[str], optional): Prior conversation turn history. Defaults to "".
        context (Optional[str], optional): Additional context or follow-up history. Defaults to "".
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments (e.g., history, session_history).

    Returns:
        str: The calculated numerical result or an error message if processing fails.
    """
    try:
        extracted_history = (
            chat_history
            or context
            or kwargs.get("history", "")
            or kwargs.get("session_history", "")
            or "No prior context."
        )

        llm: LLM = LLM(
            model="groq/llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.0,
        )

        mathematician_agent: Agent = Agent(
            role="Mathematician",
            goal="Perform precise mathematical calculations using available tools.",
            backstory="You are an expert mathematician focused on accuracy and correctness.",
            tools=[add, subtract, multiply, divide],
            llm=llm,
            verbose=False,
        )

        calculation_task: Task = Task(
            description=(
                f"Calculate the following request: '{user_message}'. "
                f"Previous Conversation Context: '{extracted_history}'"
            ),
            expected_output="Only the numerical result or mathematical final output.",
            agent=mathematician_agent,
        )

        crew: Crew = Crew(
            agents=[mathematician_agent],
            tasks=[calculation_task],
            verbose=False,
        )

        result = crew.kickoff()
        output_str = result.raw if hasattr(result, "raw") else str(result)
        return output_str

    except Exception as error:
        print(f"\n[ERROR in run_mathematician]: {type(error).__name__} - {error}")
        logger.error(f"Error in run_mathematician: {str(error)}", exc_info=True)
        return "Desculpe, ocorreu um erro ao processar sua solicitação matemática."