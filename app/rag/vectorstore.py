from langchain_chroma.vectorstores import Chroma
from dotenv import load_dotenv

class Vectorstores:
    def __init__(self, chunks, embedding, path_database):
        self.chunks = chunks
        self.embedding = embedding
        self.path_database = path_database

        # Vetorizando documentos e criando base de dados
        Chroma.from_documents(
            documents = self.chunks,
            embedding = self.embedding,
            persist_directory = self.path_database,
            collection_metadata = {"hnsw:space": "cosine"}
        )
        print("Banco de dados criado com sucesso!")