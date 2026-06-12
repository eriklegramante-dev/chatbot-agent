import streamlit as st
import re
import logging
import os

from src.logger_config import logger
from src.agents_config import executar_fluxo_agentes

st.set_page_config(
    page_title="Multi-Agent Chatbot",
    page_icon="🤖",
    layout="centered"
)

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def validar_input_matematico(texto: str) -> tuple[bool, str]:
    """
    Valida se o input tenta misturar texto inválido como argumento de uma operação.
    Bloqueia apenas padrões bizarros como '5 + batata' ou '10 / texto'.
    Frases naturais como 'Poderia somar 5 + 5' passam livremente.
    """
    texto_lower = texto.lower()
    
    padrao_mistura = r'([\+\-\*/]|\b(mais|menos|vezes|dividido)\b)\s*[a-zA-Záéíóúçãõâêô]+'
    
    if re.search(padrao_mistura, texto_lower):
        palavras_suspeitas = re.findall(r'[\+\-\*/\b(mais|menos|vezes|dividido)\b]\s*([a-zA-Záéíóúçãõâêô]+)', texto_lower)
        termo = palavras_suspeitas[0] if palavras_suspeitas else "texto"
        return False, f"Detectei um termo inválido misturado ao cálculo: **'{termo}'**. Por favor, use apenas números com os operadores (ex: 'Poderia somar 10000 + 10000')."
        
    return True, ""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Eu sou o seu assistente de IA. Como posso te ajudar com cálculos ou textos hoje?"}
    ]

st.title("🤖 Chatbot Multi-Agente (CrewAI)")
st.caption("Orquestração sequencial: Agente Matemático ──> Agente Escritor")
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input("Digite sua mensagem aqui..."):
    logger.info(f"Input do Usuário: '{user_input}'")
    valido, mensagem_erro = validar_input_matematico(user_input)
    
    if not valido:
        st.error(mensagem_erro)
    else:
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("assistant"):
            with st.spinner("Os agentes estão colaborando na resposta..."):
                

                historico_formatado = ""
                for msg in st.session_state.messages[:-1]: # Ignora a última mensagem que acabou de ser enviada
                    autor = "Usuário" if msg["role"] == "user" else "Assistente"
                    historico_formatado += f"{autor}: {msg['content']}\n"
                
                try:
                    resposta_agentes = executar_fluxo_agentes(
                        pergunta_usuario=user_input, 
                        contexto_historico=historico_formatado
                    )
                    logger.info(f"Resposta dos Agentes enviada com sucesso.")
                except Exception as e:
                    logger.error(f"Erro ao processar a requisição: {str(e)}", exc_info=True)
                    resposta_agentes = f"Desculpe, ocorreu um erro ao acionar os agentes: {str(e)}"
                
                st.write(resposta_agentes)
                
        st.session_state.messages.append({"role": "assistant", "content": resposta_agentes})