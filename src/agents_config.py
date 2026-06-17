import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
import src.tools as math_tools

load_dotenv()

llm_config = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0,

    fallbacks=[
        "groq/llama-3.3-70b-versatile",  
    ]
)


@tool("Ferramenta de Adição")
def somar_tool(a: float, b: float) -> float:
    """Soma dois números reais (a e b). Use sempre que precisar de adição ou soma."""
    return math_tools.somar(a, b)

@tool("Ferramenta de Subtração")
def subtrair_tool(a: float, b: float) -> float:
    """Subtrai b de a. Use sempre que o usuário pedir uma subtração ou diferença."""
    return math_tools.subtrair(a, b)

@tool("Ferramenta de Multiplicação")
def multiplicar_tool(a: float, b: float) -> float:
    """Multiplica dois números reais. Use sempre que pedir multiplicação ou produto."""
    return math_tools.multiplicar(a, b)

@tool("Ferramenta de Divisão")
def dividir_tool(a: float, b: float):
    """Divide a por b. Contém proteção contra divisão por zero e inputs textuais."""
    return math_tools.dividir(a, b)


matematico_agent = Agent(
    role="Calculador Estrito",
    goal="Identificar números e acionar a ferramenta matemática correta.",
    backstory="Você é um interpretador lógico direto. Não invente cálculos com palavras.",
    tools=[somar_tool, subtrair_tool, multiplicar_tool, dividir_tool],
    allow_delegation=False,
    llm=llm_config,
    verbose=False 
)

escritor_agent = Agent(
    role="Redator Ultra-Conciso",
    goal="Responder ao usuário em no máximo 100 caracteres, mantendo o idioma do prompt.",
    backstory="Você é um assistente direto e breve. Sua resposta NUNCA pode passar de 100 caracteres.",
    allow_delegation=False,
    llm=llm_config,
    verbose=False
)


def executar_fluxo_agentes(pergunta_usuario: str, contexto_historico: str = "") -> str:
    """
    Executa a equipe permitindo interpretação de texto matemático, saudações
    e respostas amigáveis de forma ultra-concisa.
    """
    
    tarefa_calculo = Task(
        description=(
            f"Histórico das conversas anteriores:\n{contexto_historico}\n"
            f"Comando atual do usuário: '{pergunta_usuario}'.\n\n"
            "DIRETRIZES DE RACIOCÍNIO:\n"
            "1. Se o usuário estiver apenas saudando (ex: 'Olá', 'Oi'), responda internamente: 'SAUDACAO'.\n"
            "2. Se o usuário trouxer um problema matemático em formato de texto ou enigma (ex: 'If John is twice as old...'), "
            "interprete a lógica, extraia os números e use as ferramentas necessárias para calcular o resultado.\n"
            "3. Se o comando pedir uma nova operação continuada (ex: 'subtraia por 2'), combine o comando com o último número do histórico.\n"
            "4. Se o assunto for 100% fora de matemática ou lógica (ex: pedir poemas, falar sobre futebol, receitas), salve internamente: 'FORA_DE_ESCOPO'."
        ),
        expected_output="O número bruto calculado, a palavra 'SAUDACAO' ou a palavra 'FORA_DE_ESCOPO'.",
        agent=matematico_agent
    )
    
    tarefa_escrita = Task(
        description=(
            f"Texto original enviado pelo usuário: '{pergunta_usuario}'.\n\n"
            "REGRAS DE FORMATAÇÃO E IDIOMA (MÁXIMO 100 CARACTERES):\n"
            "1. IDIOMA: Responda estritamente NO MESMO IDIOMA em que o usuário escreveu a pergunta atual.\n"
            "2. CASO SEJA SAUDAÇÃO: Dê uma resposta curta e muito amigável convidando para um cálculo. "
            "(Ex em PT: 'Olá! Sou seu assistente matemático. O que vamos calcular hoje?')\n"
            "3. CASO SEJA CÁLCULO: Traga o resultado de forma leve, amigável e ultra-direta. "
            "(Ex em PT: 'O resultado é 10!' ou 'Com certeza, isso dá 6.'). Evite parágrafos longos.\n"
            "4. CASO FORA DE ESCOPO: Explique educadamente que o foco do sistema é apenas matemática. "
            "(Ex em ES: 'Erro: Esta aplicación processa solo comandos matemáticos.').\n"
            "5. RESTRIÇÃO: A sua resposta final combinada NUNCA pode passar de 100 caracteres."
        ),
        expected_output="Uma frase amigável, natural e curtíssima no mesmo idioma do usuário (Máx 100 caracteres).",
        agent=escritor_agent
    )
    
    equipe = Crew(
        agents=[matematico_agent, escritor_agent],
        tasks=[tarefa_calculo, tarefa_escrita],
        process=Process.sequential,
        verbose=False,
        memory=False
    )
    
    resultado_final = equipe.kickoff()
    return str(resultado_final)