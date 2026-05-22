import langchain_chroma.vectorstores import Chroma
from dotenv import load_dotenv

class Vectorstores:
    def __init__(self, chunks, embedding, PATH_DATABASE):
        self.chunks = chunks
        self.embedding = embedding
        self.PATH_DATABASE = PATH_DATABASE

        # Vetorizando documentos e criando base de dados
        Chroma.from_documents(
            documents = self.chunks,
            embedding = self.embedding,
            persist_directory = self.PATH_DATABASE
            collection_metadata = {"hnsw:space": "cosine"}
        )
        print("Banco de dados criado com sucesso!")