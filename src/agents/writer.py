"""
Writer Agent Module.

This module defines the Writer Agent using CrewAI, responsible for transforming
raw calculation outputs into natural, friendly Portuguese user responses.
"""


from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from src.config.llm import get_llm

load_dotenv()


def run_writer(user_prompt: str, calc_result: str) -> str:
    writer_agent = Agent(
        role="Multilingual Retro-Futuristic Copywriter",
        goal="Format greetings or mathematical results concisely in the same language as the user.",
        backstory="You are SYNTH_AI, a synthwave assistant. You deliver brief, direct calculation results in the exact same language the user used.",
        llm=get_llm(),
        cache=False,
        verbose=True,
        allow_delegation=False
    )

    writer_task = Task(
        description=f"""
        Format the output for the user.

        User Query: "{user_prompt}"
        Calculation Result: "{calc_result}"

        Instructions:
        1. CRITICAL: Detect the language of the User Query (Portuguese, English, Japanese, etc.) and respond in that EXACT same language.
        2. If Calculation Result is 'GREETING':
           - Provide a short, cool retro-futuristic greeting in the detected user language.
        3. If Calculation Result is a MATH RESULT:
           - Display the mathematical operation and final result clearly in the detected user language. Keep explanations short.
        4. Do NOT wrap output in markdown code blocks (no ```text or ```).
        5. Output plain raw text directly.
        """,
        expected_output="A concise synthwave-styled response written in the same language as the user query.",
        agent=writer_agent
    )

    crew = Crew(
        agents=[writer_agent],
        tasks=[writer_task]
    )

    result = crew.kickoff()
    return str(result)