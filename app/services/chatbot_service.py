from pathlib import Path

# RAG
from app.rag.pipeline import PipelineRag
from app.rag.retriever import Retriever
from app.rag.embeddings import Embedding

# LLM cores
from app.llm.history import History
from app.llm.prompt_build import PromptBuild
from app.llm.models.groq_model import GroqModel


class ChatbotService:

    def __init__(self):

        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        DB_DIR = BASE_DIR / "database"

        PATH_DATABASE = str(DB_DIR)
        EMBEDDING_MODEL = "mxbai-embed-large"
        GROQ_MODEL = "llama-3.3-70b-versatile"
        SEARCH_TYPE = "mmr"

        # self.__pipeline_rag = PipelineRag()

        self.__embedding = Embedding(EMBEDDING_MODEL)

        self.__retriever = Retriever(
            PATH_DATABASE,
            self.__embedding.getEmbedding(),
            SEARCH_TYPE,
            3,
            5,
            0.6
        )

        self.__history = History()

        self.__prompt_build = PromptBuild()

        self.__model_groq = GroqModel(
            model=GROQ_MODEL,
            temperature=0.2
        )

    def startResponse(self, user_id, question):

        # Busca histórico do usuário
        history_user = self.__history.getUserHistoryById(user_id)

        # Salva pergunta no histórico
        self.__history.createHistory(user_id, question)

        # Busca contexto no RAG
        result_retriever = self.__retriever.getContext(question)

        # Monta contexto
        if result_retriever:

            context_question = "\n\n----\n\n".join(
                doc.page_content
                for doc in result_retriever
            )

        else:
            context_question = "Nenhum contexto encontrado."

        # Cria prompt
        prompt = self.__prompt_build.getPrompt(question, context_question, history_user)

        # Gera resposta
        result_response_llm = self.__model_groq.getResponse(prompt)

        return result_response_llm