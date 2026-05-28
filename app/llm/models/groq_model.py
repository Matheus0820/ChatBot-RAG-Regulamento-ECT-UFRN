from dotenv import load_dotenv
from langchain_groq import ChatGroq


class GroqModel:
    def __init__(self, model, temperature):
        self.__model = ChatGroq(model=model, temperature=temperature)
    
    def getResponse(self, prompt):
        response = self.__model.invoke(prompt)

        if hasattr(response, 'content'):
            return(response.content)
        
        return(str(response))
