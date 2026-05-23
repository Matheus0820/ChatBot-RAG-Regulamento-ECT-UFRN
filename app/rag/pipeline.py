from embeddings import Embedding
from chunking import Chunking
from vectorstore import Vectorstores
from services.docs_read import DocsRead

class PipelineRag:
    def __init__(self):
        # Variaveis essenciais
        PATH_DATABASE = 'database'
        EMBEDDING_MODEL = "mxbai-embed-large"
        FOLDER_BASE_DADOS = "../../base_dados"

        # Criando objetos e instanciando-os
        self.docsRead = DocsRead(FOLDER_BASE_DADOS)
        self.embedding = Embedding(EMBEDDING_MODEL)
        self.chunking = Chunking(800, 200, self.docsRead.load_txt_documents())
        self.vectorstore = Vectorstores(self.chunking.getChunks, self.embedding.getEmbedding, PATH_DATABASE)
    
