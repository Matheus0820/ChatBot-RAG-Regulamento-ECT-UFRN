import sys
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ChatBot do Calouro",
    page_icon="🎓",
    layout="centered"
)

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

sys.path.append(str(ROOT_DIR))

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Container principal */

.block-container {
    max-width: 650px;
    padding-top: 4rem;
}

/* Card principal */

.hero-card {
    background-color: var(--secondary-background-color);
    padding: 40px;
    border-radius: 24px;
    border: 1px solid rgba(128,128,128,0.15);
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

/* Título */

.hero-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 10px;
}

/* Subtítulo */

.hero-subtitle {
    text-align: center;
    color: var(--text-color);
    opacity: 0.75;
    margin-bottom: 10px;
}

/* Labels */

.stTextInput label {
    font-weight: 600;
}

/* Inputs */

.stTextInput input {
    border-radius: 10px;
}

/* Botão */

.stButton button {
    width: 100%;
    height: 52px;
    border-radius: 12px;
    font-weight: 600;
}

/* Rodapé */

.footer {
    text-align: center;
    color: var(--text-color);
    opacity: 0.6;
    margin-top: 25px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.html("""
<div class="hero-card">

    <div class="hero-title">
        🎓 ChatBot do Calouro
    </div>

    <div class="hero-subtitle">
        Seu assistente virtual para dúvidas acadêmicas,
        matrícula, disciplinas e vida universitária.
    </div>

</div>
""")

# --------------------------------------------------
# FORMULÁRIO
# --------------------------------------------------

with st.form("login_form"):

    nome = st.text_input(
        "👤 Nome completo",
        placeholder="Digite seu nome"
    )

    user_id = st.text_input(
        "🎓 Matrícula UFRN",
        placeholder="Ex: 20251234567"
    )

    entrar = st.form_submit_button(
        "Entrar no Chat",
        use_container_width=True
    )

# --------------------------------------------------
# LOGIN
# --------------------------------------------------

if entrar:

    nome = nome.strip()
    user_id = user_id.strip()

    if not nome:
        st.error("Informe seu nome.")
        st.stop()

    if not user_id:
        st.error("Informe sua matrícula.")
        st.stop()

    st.session_state["nome"] = nome
    st.session_state["user_id"] = user_id

    st.success("Acesso realizado com sucesso!")

    st.switch_page(
        "pages/chat_chatbot.py"
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
Universidade Federal do Rio Grande do Norte • UFRN
</div>
""", unsafe_allow_html=True)