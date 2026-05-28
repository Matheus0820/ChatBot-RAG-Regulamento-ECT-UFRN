import yaml
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate

class PromptBuild:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent
        file_path = base_dir / "prompts.yaml"

        with open(file_path, "r", encoding="utf-8") as file:
            self.prompts = yaml.safe_load(file)

        
        self.template_prompt = ChatPromptTemplate.from_template(self.prompts["template_prompt"])
    
    def getPrompt(self, question, context, history):
        self.prompt = self.template_prompt.invoke({
            "question": question,
            "context": context,
            "history": history
        })

        return self.prompt