import streamlit as st
import re

from src.agents_config import executar_fluxo_agentes

# 1. Configuração da página
st.set_page_config(
    page_title="Multi-Agent Chatbot",
    page_icon="🤖",
    layout="centered"
)

def validar_input_matematico(texto: str) -> tuple[bool, str]:
    """
    Valida se o input do usuário contém tentativas inválidas de mistura
    de texto com operações matemáticas (ex: '5 + batata').
    """
    texto_lower = texto.lower()
    operadores = ['+', '-', '*', '/', 'somar', 'subtrair', 'multiplicar', 'dividir', 'mais', 'menos']
    tentando_calcular = any(op in texto_lower for op in operadores) or any(char in texto for char in ['+', '-', '*', '/'])
    
    if tentando_calcular:
        palavras_permitidas = {
            'quanto', 'é', 'o', 'resultado', 'de', 'por', 'e', 'qual', 'conta', 
            'soma', 'subtração', 'multiplicação', 'divisão', 'da', 'do', 'com', 'agora'
        }
        palavras_no_texto = re.findall(r'[a-záéíóúçãõâêô]+', texto_lower)
        for palavra in palavras_no_texto:
            if palavra not in palavras_permitidas:
                if any(char.isdigit() for char in texto):
                    return False, f"Detectei um termo inválido para cálculos: **'{palavra}'**. Por favor, insira apenas números e operadores válidos."
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

# 5. Campo de Entrada do Usuário
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
                for msg in st.session_state.messages[:-1]: # Ignora a última mensagem que acabou de ser enviada
                    autor = "Usuário" if msg["role"] == "user" else "Assistente"
                    historico_formatado += f"{autor}: {msg['content']}\n"
                
                try:
                    resposta_agentes = executar_fluxo_agentes(
                        pergunta_usuario=user_input, 
                        contexto_historico=historico_formatado
                    )
                except Exception as e:
                    resposta_agentes = f"Desculpe, ocorreu um erro ao acionar os agentes: {str(e)}"
                
                st.write(resposta_agentes)
                
        st.session_state.messages.append({"role": "assistant", "content": resposta_agentes})