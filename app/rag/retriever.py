from langchain_chroma.vectorstores import Chroma
from dotenv import load_dotenv

class Retriever:
    def __init__(self, path_database, embedding, search_type, k, fetch_k, lambda_mult):
        self.database = Chroma(
            persist_directory = path_database,
            embedding_function = embedding
        )

        self.retriever = self.database.as_retriever(
            search_type = search_type,
            search_kwargs={'k': k, 'fetch_k': fetch_k, 'lambda_mult': lambda_mult}
        )
    

    def getContext(self, question):
        self.context = self.retriever.invoke(question)

        return self.context