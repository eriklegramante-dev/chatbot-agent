"""
Writer Agent Module.

This module defines the Writer Agent using CrewAI, responsible for transforming
raw calculation outputs into natural, friendly Portuguese user responses.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

load_dotenv()


def run_writer(raw_input: str, user_message: Optional[str] = "", *args, **kwargs) -> str:
    """
    Executes the Writer Agent to format raw calculation output into natural language.

    Args:
        raw_input (str): The raw mathematical result or computation output.
        user_message (Optional[str], optional): The original context or query from the user. Defaults to "".
        *args: Additional positional arguments for flexibility across caller implementations.
        **kwargs: Additional keyword arguments for flexibility across caller implementations.

    Returns:
        str: The formatted natural language response in Portuguese, or the raw input on failure.
    """
    try:
        llm: LLM = LLM(
            model="groq/llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.7,
        )

        writer_agent: Agent = Agent(
            role="Writer",
            goal="Format mathematical responses into natural Portuguese text.",
            backstory="You are a friendly assistant skilled at presenting numbers clearly and concisely.",
            llm=llm,
            verbose=False,
        )

        task_description: str = (
            f"Format the following raw mathematical result into a clear, natural response in Portuguese: '{raw_input}'."
        )
        if user_message:
            task_description += f" Original user message context: '{user_message}'."

        formatting_task: Task = Task(
            description=task_description,
            expected_output="A polite, natural sentence containing the final numerical answer.",
            agent=writer_agent,
        )

        crew: Crew = Crew(
            agents=[writer_agent],
            tasks=[formatting_task],
            verbose=False,
        )

        result = crew.kickoff()
        return result.raw if hasattr(result, "raw") else str(result)

    except Exception:
        return raw_input