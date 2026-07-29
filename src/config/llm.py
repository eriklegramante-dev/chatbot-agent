import os
from crewai import LLM

def get_llm():
    groq_key = os.getenv("GROQ_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if groq_key:
        return LLM(
            model="openai/llama-3.3-70b-versatile",
            base_url="https://api.groq.com/openai/v1",
            api_key=groq_key
        )
    elif gemini_key:
        return LLM(
            model="gemini/gemini-1.5-flash-lite",
            api_key=gemini_key
        )
    else:
        raise ValueError("No API keys were found in the environment.")