import sys
from pathlib import Path
from dotenv import load_dotenv
import os
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

sys.path.append(str(ROOT_DIR))

from app.services.chatbot_service import ChatbotService

chatbot = ChatbotService()

st.title("🤖 Chatbot RAG - Teste")

# pega dados vindos da página anterior
nome = st.session_state.get("nome", "Usuário")
user_id = st.session_state.get("user_id", None)

st.write(f"Olá, **{nome}** 👋")

if user_id is None:
    st.warning("User ID não encontrado. Volte para o cadastro.")
    st.stop()

# histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# render histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Digite sua pergunta...")

if question:
    st.chat_message("user").write(question)
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = chatbot.startResponse(
                user_id=user_id,
                question=question
            )

        st.write(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )