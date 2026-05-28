import sys
from pathlib import Path
from dotenv import load_dotenv
import os
import streamlit as st

# raiz do projeto
ROOT_DIR = Path(__file__).resolve().parent.parent

# carregar .env
load_dotenv(ROOT_DIR / ".env")

sys.path.append(str(ROOT_DIR))

st.title("Cadastro de novo usuário")
st.write("Seja bem-vindo ao ChatBot do Calouro!")
st.write("Preencha os dados abaixo para prosseguir!")

nome = st.text_input("Digite seu nome:")
user_id = st.text_input("Digite sua matrícula da UFRN:")

# botão de entrada
if st.button("Acessar o chat!") and nome and user_id:

    # salva dados na sessão (IMPORTANTE)
    st.session_state["nome"] = nome
    st.session_state["user_id"] = user_id

    # navega para página do chat
    st.switch_page("pages/chat_chatbot.py")