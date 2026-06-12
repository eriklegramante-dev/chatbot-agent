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
    role="Especialista em Cálculos Matemáticos",
    goal="Identificar a operação matemática solicitada e resolvê-la usando exclusivamente as ferramentas fornecidas.",
    backstory=(
        "Você é um executor lógico, frio e extremamente literal. Você possui guardrails de segurança severos:\n"
        "1. Você SÓ realiza cálculos se o usuário fornecer números explícitos.\n"
        "2. Se o usuário pedir para dividir, somar, subtrair ou multiplicar uma PALAVRA ou TEXTO, você NÃO deve inventar uma lógica (como contar caracteres ou medir o tamanho da palavra).\n"
        "3. Diante de inputs absurdos ou textuais (ex: dividir uma palavra por um número), você deve parar imediatamente e responder textualmente: 'Erro: Operação inválida. Não é possível realizar operações matemáticas com palavras.'\n"
    ),
    tools=[somar_tool, subtrair_tool, multiplicar_tool, dividir_tool],
    allow_delegation=False,
    llm=llm_config,
    verbose=True 
)

escritor_agent = Agent(
    role="Redator e Comunicador Amigável",
    goal="Transformar dados e resultados matemáticos brutos em respostas humanas, claras e no idioma correto.",
    backstory=(
        "Você é um copywriter extremamente empático e refinado. Sua missão é pegar o resultado numérico "
        "encontrado pelo Especialista em Cálculos e entregá-lo ao usuário de forma natural, educada e fluida. "
        "Você DEVE responder no exato mesmo idioma em que a pergunta inicial foi feita. "
        "Guardrail: Você nunca tenta inventar ou calcular os números por conta própria; sua matéria-prima é o que o matemático te entrega."
    ),
    allow_delegation=False,
    llm=llm_config,
    verbose=True
)


def executar_fluxo_agentes(pergunta_usuario: str, contexto_historico: str = "") -> str:
    """
    Cria as tarefas dinamicamente, joga no CrewAI e gerencia a execução sequencial.
    """
    
    tarefa_calculo = Task(
        description=(
            f"Analise a solicitação do usuário: '{pergunta_usuario}'.\n"
            f"Contexto das conversas anteriores: {contexto_historico}.\n"
            "Identifique os números e execute a operação correta usando uma das ferramentas. "
            "Se a pergunta não envolver um cálculo novo mas sim uma continuação, use o histórico para entender o número anterior."
        ),
        expected_output="O valor numérico exato do resultado e qual operação foi feita.",
        agent=matematico_agent
    )
    
    tarefa_escrita = Task(
        description=(
            f"Pegue o resultado gerado pela tarefa de cálculo anterior e formule uma resposta final para o usuário.\n"
            f"A pergunta original do usuário foi: '{pergunta_usuario}'.\n"
            "Exigências:\n"
            "1. Responda no mesmo idioma da pergunta do usuário.\n"
            "2. Seja amigável, direto e mantenha a formatação limpa."
        ),
        expected_output="Uma resposta em texto natural e amigável contendo a resolução e o resultado.",
        agent=escritor_agent
    )
    
    equipe = Crew(
        agents=[matematico_agent, escritor_agent],
        tasks=[tarefa_calculo, tarefa_escrita],
        process=Process.sequential,
        verbose=True
    )
    
    resultado_final = equipe.kickoff()
    return str(resultado_final)