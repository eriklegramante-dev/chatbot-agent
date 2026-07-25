"""
Writer Agent Module.

This module defines the Writer Agent using CrewAI, responsible for transforming
raw calculation outputs into natural, friendly Portuguese user responses.
"""
import os 
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()


free_llm = LLM(
    model="gemini/gemini-3.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

def run_writer(user_prompt: str, calc_result: str) -> str:
    writer_agent = Agent(
        role="Retro-Futuristic Synthwave Copywriter",
        goal="Format greetings or mathematical results concisely into retro-futuristic AI responses.",
        backstory="You are SYNTH_AI, a synthwave assistant. You deliver brief, direct calculation results or friendly greetings.",
        llm=free_llm,
        verbose=True,
        allow_delegation=False
    )

    writer_task = Task(
        description=f"""
        Process the input data:
        Calculation/Intent Result: {calc_result}
        User Prompt: {user_prompt}

        Instructions:
        - If the calculation result indicates GREETING:
          Provide a short, cool retro-futuristic welcome message (e.g., "SYSTEM ONLINE :: Welcome user. Ready for mathematical processing.").
        - If the calculation result is a MATH RESULT:
          Limit the response strictly to the calculation resolution and final answer. Keep explanations minimal and direct to the numbers.
        - Do NOT wrap output in markdown code blocks like ```text or ```.
        - Output plain raw text directly.
        """,
        expected_output="A brief synthwave-styled greeting or a direct mathematical result in plain text.",
        agent=writer_agent
    )

    crew = Crew(
        agents=[writer_agent],
        tasks=[writer_task]
    )

    result = crew.kickoff()
    return str(result)