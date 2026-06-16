import streamlit as st
import re
import logging
import os

from src.logger_config import logger
from src.agents_config import executar_fluxo_agentes

st.set_page_config(
    page_title="MathAgent AI",
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

col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("<h1 style='font-size: 55px; margin-top: -10px;'>🤖</h1>", unsafe_allow_html=True)
with col2:
    st.title("MathAgent AI")
    st.caption("Orquestração Multi-Agente Avançada com CrewAI & Llama 3.3")

st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    st.markdown(
        """
        ### Bem-vindo ao assistente matemático inteligente!
        Este sistema utiliza uma equipe de agentes digitais especializados que colaboram de forma sequencial 
        para resolver problemas lógicos, traduzir contextos e executar cálculos sem alucinações.
        """
    )
    st.write("") 
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info(
            "🧠 **Memória de Contexto**\n\n"
            "O bot retém o histórico. Você pode pedir `5 + 5` e, em seguida, dizer apenas `subtrai por 2`."
        )
    with c2:
        st.success(
            "🛡️ **Guardrails Ativos**\n\n"
            "Filtros robustos contra injeção de prompt, linguagem imprópria e escopos não-matemáticos."
        )
    with c3:
        st.warning(
            "🌐 **Multilíngue**\n\n"
            "O assistente identifica o idioma do prompt automaticamente e responde de forma ultra-concisa."
        )
        
    st.write("")
    st.markdown("💡 *Dica: Experimente iniciar com perguntas diretas ou comandos contínuos no chat abaixo.*")
    st.markdown("---")
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def validar_input_seguro(texto: str) -> tuple[bool, str]:
    """
    Valida se o input é seguro contra Prompt Injections, termos ofensivos 
    e misturas inválidas em cálculos.
    """
    texto_lower = texto.lower()
    
    padroes_injection = [
        r"ignore", r"esqueça", r"bypass", r"override", 
        r"instruç", r"orientaç", r"system prompt", r"as regras",
        r"acting as", r"aja como", r"command"
    ]
    for padrao in padroes_injection:
        if re.search(padrao, texto_lower):
            logger.warning(f"Tentativa de Prompt Injection detectada: '{texto}'")
            return False, "⚠️ **Acesso Negado:** Tentativa de alteração das diretrizes do sistema detectada. Por favor, limite-se a comandos matemáticos."

    palavras_improprias = [
        "palavrao1", "palavrao2", "insulto1", "ofensa2" # Substitua pelos termos reais
    ]
    for termo in palavras_improprias:
        if termo in texto_lower:
            logger.warning(f"Linguagem imprópria detectada: '{texto}'")
            return False, "🚫 **Mensagem Bloqueada:** Por favor, mantenha uma linguagem respeitosa no chat."

    padrao_mistura = r'([\+\-\*/]|\b(mais|menos|vezes|dividido)\b)\s*[a-zA-Záéíóúçãõâêô]+'
    if re.search(padrao_mistura, texto_lower):
        palavras_suspeitas = re.findall(r'[\+\-\*/\b(mais|menos|vezes|dividido)\b]\s*([a-zA-Záéíóúçãõâêô]+)', texto_lower)
        termo = palavras_suspeitas[0] if palavras_suspeitas else "texto"
        return False, f"Detectei um termo inválido misturado ao cálculo: **'{termo}'**."
        
    return True, ""

if user_input := st.chat_input("Digite sua mensagem aqui..."):
    
    valido, mensagem_erro = validar_input_seguro(user_input)
    
    if not valido:
        st.error(mensagem_erro)
    else:
        if len(st.session_state.messages) == 0:
            st.rerun()
            
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("assistant"):
            with st.spinner("Os agentes estão colaborando na resposta..."):
                
                # Montagem da memória contextual
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