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
                for msg in st.session_state.messages[:-1]:
                    autor = "Usuário" if msg["role"] == "user" else "Assistente"
                    historico_formatado += f"{autor}: {msg['content']}\n"
                
                try:
                    resposta_agentes = executar_fluxo_agentes(
                        pergunta_usuario=user_input, 
                        contexto_historico=historico_formatado
                    )
                    
                except Exception as e:
                    erro_str = str(e).lower()
                    
                    if "rate_limit" in erro_str or "limit_exceeded" in erro_str or "quota" in erro_str:
                        resposta_agentes = (
                            "⚠️ **Ufa, quanta energia!** Nosso motor de IA atingiu o limite temporário de mensagens da conta gratuita. "
                            "Por favor, **aguarde cerca de 1 minuto** para o sistema respirar e envie sua mensagem novamente. "
                            "Seu histórico de conversa não foi perdido!"
                        )
                        logger.warning(f"Rate Limit atingido na API: {str(e)}")
                        
                    elif "api_key" in erro_str or "authentication" in erro_str:
                        resposta_agentes = (
                            "🔧 **Erro de Configuração:** Houve um problema de autenticação com o provedor de IA. "
                            "Por favor, verifique se a chave de API nas configurações do servidor está correta."
                        )
                        logger.error(f"Erro de autenticação de API: {str(e)}")
                        
                    elif "timeout" in erro_str or "deadline" in erro_str:
                        resposta_agentes = (
                            "⏳ **Tempo limite esgotado:** O servidor de IA demorou um pouco mais do que o esperado para responder. "
                            "Pode tentar enviar o comando novamente?"
                        )
                        logger.warning(f"Timeout na requisição de IA: {str(e)}")
                        
                    else:
                        resposta_agentes = (
                            "🤖 **Ih, deu um pequeno curto-circuito!** Eu não consegui processar essa resposta agora. "
                            "Isso pode ser uma instabilidade temporária no servidor do modelo. Pode tentar de novo?"
                        )
                        logger.error(f"Erro inesperado no fluxo de agentes: {str(e)}", exc_info=True)
                
                st.write(resposta_agentes)
                
        st.session_state.messages.append({"role": "assistant", "content": resposta_agentes})