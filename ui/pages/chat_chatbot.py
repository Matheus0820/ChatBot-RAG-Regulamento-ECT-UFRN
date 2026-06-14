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
    layout="wide"
)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

sys.path.append(str(ROOT_DIR))

from app.services.chatbot_service import ChatbotService

# --------------------------------------------------
# SERVICE
# --------------------------------------------------

@st.cache_resource
def get_chatbot():
    return ChatbotService()

chatbot = get_chatbot()

# --------------------------------------------------
# SESSION
# --------------------------------------------------

nome = st.session_state.get("nome")
user_id = st.session_state.get("user_id")

if not nome or not user_id:
    st.error("Sessão não encontrada. Volte para a tela inicial.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Layout */

.block-container {
    max-width: 1100px;
    padding-top: 1rem;
}

/* Header */

.hero {
    background-color: var(--secondary-background-color);
    border: 1px solid rgba(128,128,128,0.15);
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 20px;
}

.hero-title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 6px;
}

.hero-subtitle {
    color: var(--text-color);
    opacity: 0.75;
}

/* Sidebar */

[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,0.15);
}

/* Cards da sidebar */

.sidebar-card {
    background-color: var(--secondary-background-color);
    padding: 16px;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.15);
}

/* Chat */

[data-testid="stChatMessage"] {
    padding-top: 8px;
    padding-bottom: 8px;
}

/* Input */

[data-testid="stChatInput"] {
    margin-top: 10px;
}

/* Botões */

.stButton button {
    border-radius: 10px;
    width: 100%;
}

/* Scroll suave */

html {
    scroll-behavior: smooth;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🎓 ChatBot do Calouro")

    st.caption("Assistente Acadêmico")

    st.divider()

    st.markdown(f"""
    <div class="sidebar-card">
        <strong>👤 {nome}</strong><br>
        <small>Matrícula: {user_id}</small>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.metric(
        "Mensagens",
        len(st.session_state.messages)
    )

    st.divider()

    if st.button(
        "🗑️ Limpar conversa",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-title">
        🤖 Chatbot do Calouro
    </div>
    <div class="hero-subtitle">
        Tire dúvidas sobre disciplinas, matrícula,
        calendário acadêmico e serviços da universidade.
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CHAT
# --------------------------------------------------

for msg in st.session_state.messages:

    avatar = "👨‍🎓" if msg["role"] == "user" else "🤖"

    with st.chat_message(
        msg["role"],
        avatar=avatar
    ):
        st.markdown(msg["content"])

# --------------------------------------------------
# INPUT
# --------------------------------------------------

question = st.chat_input(
    "Digite sua dúvida..."
)

if question:

    # usuário
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message(
        "user",
        avatar="👨‍🎓"
    ):
        st.markdown(question)

    # assistente
    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        with st.spinner("Consultando informações..."):

            response = chatbot.startResponse(
                user_id=user_id,
                question=question
            )

        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })