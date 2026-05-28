import sys
from pathlib import Path
from dotenv import load_dotenv
import os
import streamlit as st

# define raiz do projeto
ROOT_DIR = Path(__file__).resolve().parent.parent

# CARREGA .env PRIMEIRO (antes de qualquer import do app)
load_dotenv(ROOT_DIR / ".env")

# debug (importante agora)
print("GROQ KEY:", os.getenv("GROQ_API_KEY"))

sys.path.append(str(ROOT_DIR))

from app.services.chatbot_service import ChatbotService


# Inicializa o chatbot
chatbot = ChatbotService()

st.title("🤖 Chatbot RAG - Teste")

# Inicializa histórico da UI
if "messages" not in st.session_state:
    st.session_state.messages = []


# Renderiza mensagens antigas
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# Input do usuário
question = st.chat_input("Digite sua pergunta...")

if question:

    user_id = 1  # teste fixo

    # Mostra mensagem do usuário
    st.chat_message("user").write(question)
    st.session_state.messages.append({"role": "user", "content": question})

    # Gera resposta do chatbot
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):

            response = chatbot.startResponse(
                user_id=user_id,
                question=question
            )

        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})