import os
import litellm
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
import src.tools as math_tools

load_dotenv()

# 1. Força o LiteLLM a NÃO injetar o parâmetro de cache de prompt em nenhuma chamada
litellm.drop_params = True

# 2. Configuração do LLM apontando explicitamente via prefixo openai/ para a Groq
llm_config = LLM(
    model="openai/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    temperature=0.0,
)


@tool("Addition Tool")
def add_tool(a: float, b: float) -> float:
    """Adds two real numbers (a and b). Use whenever addition or sum is needed."""
    return math_tools.add(a, b)

@tool("Subtraction Tool")
def subtract_tool(a: float, b: float) -> float:
    """Subtracts b from a. Use whenever a subtraction or difference is requested."""
    return math_tools.subtract(a, b)

@tool("Multiplication Tool")
def multiply_tool(a: float, b: float) -> float:
    """Multiplies two real numbers. Use whenever multiplication or product is requested."""
    return math_tools.multiply(a, b)

@tool("Division Tool")
def divide_tool(a: float, b: float):
    """Divides a by b. Includes protection against division by zero and textual inputs."""
    return math_tools.divide(a, b)


mathematician_agent = Agent(
    role="Strict Calculator",
    goal="Identify numbers and trigger the correct mathematical tool.",
    backstory="You are a direct logical interpreter. Do not invent calculations with words.",
    tools=[add_tool, subtract_tool, multiply_tool, divide_tool],
    allow_delegation=False,
    llm=llm_config,
    verbose=False
)

writer_agent = Agent(
    role="Ultra-Concise Copywriter",
    goal="Respond to the user in a maximum of 100 characters, maintaining the language of the prompt.",
    backstory="You are a direct and concise assistant. Your response must NEVER exceed 100 characters.",
    allow_delegation=False,
    llm=llm_config,
    verbose=False
)


async def execute_agent_flow(user_prompt: str, chat_history: str = "") -> str:
    """
    Executes the crew allowing interpretation of mathematical text, greetings,
    and friendly responses in an ultra-concise format.
    """
    
    calculation_task = Task(
            description=(
                f"Previous conversation history:\n{chat_history}\n"
                f"Current user command: '{user_prompt}'.\n\n"
                "REASONING GUIDELINES:\n"
                "1. GREETINGS: If the user message is a simple greeting, hi, hello, or casual check-in (e.g., 'Olá', 'Oi', 'Hello', 'Hi', 'Tudo bem?'), "
                "OUTPUT EXACTLY AND ONLY THE WORD: 'GREETING'. Do not call any tools.\n"
                "2. MATH PROBLEMS: If the user brings numbers, calculations, or word problems (e.g., 'Quanto é 2+2', 'If John has 5 apples...'), "
                "extract the numbers, use the mathematical tools, and return the raw calculated number.\n"
                "3. CONTINUED OPERATIONS: If the command requests a continued operation (e.g., 'subtract 2'), combine it with the last result from history.\n"
                "4. OUT OF SCOPE: If the topic is entirely unrelated to math (e.g., recipes, football, poems, general trivia), OUTPUT EXACTLY AND ONLY: 'OUT_OF_SCOPE'."
            ),
            expected_output="The raw calculated number, or the exact keyword 'GREETING', or 'OUT_OF_SCOPE'.",
            agent=mathematician_agent
        )
        
    writing_task = Task(
        description=(
            f"Original text sent by the user: '{user_prompt}'.\n"
            f"Result from previous step: '{{calculation_task.output}}'.\n\n"
            "FORMATTING RULES (STRICT MAXIMUM OF 100 CHARACTERS):\n"
            "1. LANGUAGE: Respond strictly in the SAME LANGUAGE as the user's prompt.\n"
            "2. IF GREETING: Give a warm, ultra-short welcome inviting them to do a math calculation. "
            "(e.g., in PT: 'Olá! Sou seu assistente matemático. O que vamos calcular hoje?')\n"
            "3. IF CALCULATION: Present the final result in a clear, direct, and friendly way. "
            "(e.g., in PT: 'O resultado é 15!').\n"
            "4. IF OUT OF SCOPE: Politely explain that you only handle math operations. "
            "(e.g., in PT: 'Desculpe, só posso ajudar com cálculos e matemática.').\n"
            "5. RESTRICTION: Your response MUST NEVER exceed 100 characters."
        ),
        expected_output="A friendly, concise sentence in the user's language (Max 100 characters).",
        agent=writer_agent
    )
    
    crew = Crew(
        agents=[mathematician_agent, writer_agent],
        tasks=[calculation_task, writing_task],
        process=Process.sequential,
        verbose=False,
        memory=False
    )
    
    final_result = await crew.kickoff_async()
    return str(final_result)