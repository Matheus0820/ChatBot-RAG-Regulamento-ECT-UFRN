import yaml
from langchain_core.prompts import ChatPromptTemplate

class PromptBuild:
    def __init__(self, path_prompts):
        with open(path_prompts, "r", encoding="utf-8") as file:
            self.prompts = yaml.safe_load(file)

        
        self.template_prompt = ChatPromptTemplate.from_template(self.prompts["template_prompt"])
    
    def getPrompt(self, question, context, history):
        self.prompt = self.template_prompt.invoke({
            "question": question,
            "context": context,
            "history": history
        })

        return self.prompt