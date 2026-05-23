from langchain_ollama import OllamaEmbedding
from dotenv import load_dotenv

class Embedding:
    def __init__(self, modelEmbedding):
        load_dotenv()

        self.model = modelEmbedding
        self.embedding = OllamaEmbedding(model = self.model)
    
    def getEmbedding(self):
        return self.embedding

    def getModel(self, model):
        return self.model
