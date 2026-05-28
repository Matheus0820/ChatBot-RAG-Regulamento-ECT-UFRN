from app.rag.embeddings import Embedding
from app.rag.chunking import Chunking
from app.rag.vectorstore import Vectorstores
from app.rag.docs_read import DocsRead

from pathlib import Path

class PipelineRag:
    def __init__(self):

        PATH_DATABASE = "database"
        EMBEDDING_MODEL = "mxbai-embed-large"

        # caminho absoluto correto
        BASE_DIR = Path(__file__).resolve().parents[2]
        FOLDER_BASE_DADOS = BASE_DIR / "base_dados"

        # instâncias
        self.docsRead = DocsRead(str(FOLDER_BASE_DADOS))
        self.embedding = Embedding(EMBEDDING_MODEL)

        self.chunking = Chunking(
            800,
            200,
            self.docsRead.load_txt_documents()
        )

        self.vectorstore = Vectorstores(
            self.chunking.getChunks(),
            self.embedding.getEmbedding(),
            PATH_DATABASE
        )