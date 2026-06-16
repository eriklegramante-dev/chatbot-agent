import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
import src.tools as math_tools

load_dotenv()

llm_config = LLM(
    temperature=0.0,
    model="groq/llama-3.3-70b-versatile"
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
    Executa a equipe com restrições severas de tamanho, escopo e idioma.
    """
    
    tarefa_calculo = Task(
        description=(
            f"Histórico das conversas anteriores:\n{contexto_historico}\n"
            f"Comando atual do usuário: '{pergunta_usuario}'.\n\n"
            "INSTRUÇÕES DE ESCOPO MATEMÁTICO:\n"
            "1. Se o comando atual pedir uma nova operação sobre o número anterior (ex: 'subtraia por 2'), "
            "identifique o último resultado no histórico e execute o cálculo usando a ferramenta.\n"
            "2. Se o comando atual for uma pergunta completamente fora de matemática (ex: história, pessoas, curiosidades), "
            "NÃO use nenhuma ferramenta e salve internamente a mensagem: 'FORA_DE_ESCOPO'.\n"
            "3. Se o comando atual for um cálculo direto novo, apenas calcule usando a ferramenta."
        ),
        expected_output="O número bruto do resultado OU a palavra exata 'FORA_DE_ESCOPO'.",
        agent=matematico_agent
    )
    
    tarefa_escrita = Task(
        description=(
            f"Texto original enviado pelo usuário: '{pergunta_usuario}'.\n\n"
            "REGRAS CRUTIAIS DE FORMATAÇÃO (MÁXIMO 100 CARACTERES):\n"
            "1. IDIOMA: Identifique o idioma do texto original do usuário e responda EXATAMENTE nesse mesmo idioma.\n"
            "2. SE FORA DE ESCOPO: Se a tarefa anterior retornou 'FORA_DE_ESCOPO', responda apenas: "
            "'Erro: Esta aplicação processa apenas comandos matemáticos.' (traduzido para o idioma do usuário).\n"
            "3. SE FOR CÁLCULO: Seja o mais direto possível. Retorne apenas o número ou uma frase curtíssima.\n"
            "Exemplo em português: 'O resultado é 2.' ou apenas '2'.\n"
            "Exemplo em japonês: '2 です。'\n"
            "4. PROIBIÇÃO: É terminantemente proibido saudações longas como 'Olá! Estou aqui para ajudar'."
        ),
        expected_output="Uma resposta final contendo no máximo 100 caracteres, escrita no mesmo idioma do usuário.",
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