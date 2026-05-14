import os
from dotenv import load_dotenv
from langchain_chroma.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Carregando credenciais e ambiente
load_dotenv()

# ==========================================
# CONFIGURAÇÕES DO PROJETO
# ==========================================
PATH_DATABASE = 'database'
EMBEDDING_MODEL = "mxbai-embed-large"

# Escolha o modo de execução da LLM mudando para True ou False:
USE_LOCAL_MODEL = False  # True = Ollama (Local) | False = Groq (Nuvem)

# ==========================================
# PROMPT TEMPLATE
# ==========================================
template_prompt = """
Você é um tutor virtual para alunos de Ciência e Tecnologia (C&T). Sua tarefa é responder perguntas de forma clara, simples e didática, facilitando o entendimento do aluno.

Pergunta do aluno:
{question}

Base de conhecimento (use estas informações para formular sua resposta, mas NÃO mencione que você recebeu esses dados ou qualquer fonte externa):
{data_result}

Instruções importantes:
- Responda de forma objetiva e fácil de entender.
- Explique como um professor explicando para um aluno iniciante.
- Não mencione, em hipótese alguma, que você recebeu dados, documentos ou qualquer fonte externa.
- Se a informação fornecida não for suficiente para responder com segurança, diga que não possui informações suficientes no momento e, se possível, dê uma resposta geral ou explicação parcial relacionada ao tema.
- Evite respostas vazias; tente sempre ajudar dentro do possível.

Resposta:
"""

def questionFunction():
    # Pedindo pergunta ao usuário 
    question = input("Faça sua pergunta sobre o regulamento da ECT: ").strip()
    if not question:
        print("A pergunta não pode ser vazia.")
        return

    try:
        # Carregando o banco de dados e função de embedding
        embedding = OllamaEmbeddings(model=EMBEDDING_MODEL)
        database = Chroma(persist_directory=PATH_DATABASE, embedding_function=embedding)

        # Configurando o buscador com MMR para mitigar falsos positivos
        retriever = database.as_retriever(
            search_type="mmr",
            search_kwargs={'k': 3, 'fetch_k': 5, 'lambda_mult': 0.6}
        )
        
        # Recuperando os documentos contextuais
        result_question = retriever.invoke(question)

        # Verificando se algum resultado relevante foi retornado
        if not result_question:
            print("\nPara essa pergunta não conseguimos achar resultados relevantes no regulamento.")
            return

        # Tratando e agrupando o conteúdo dos documentos
        listTextResult = [doc.page_content for doc in result_question]
        data_result = "\n\n ---- \n\n".join(listTextResult)

        # Configurando e invocando o prompt template
        prompt_template = ChatPromptTemplate.from_template(template_prompt)
        prompt = prompt_template.invoke({"question": question, "data_result": data_result})
        
        # Seleção dinâmica do modelo (Groq ou Ollama) com suporte a streaming
        if USE_LOCAL_MODEL:
            print(" -> Processando resposta localmente via Ollama...")
            model = ChatOllama(model="llama3.2:1b", temperature=0.2)
        else:
            print(" -> Processando resposta na nuvem via Groq...")
            model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)
            
        # Exibição do cabeçalho estilizado no terminal ANTES da resposta começar
        print(f"\n{Colors.GREEN}{'=' * 40}")
        print("RESPOSTA DO TUTOR VIRTUAL:")
        print(f"{'=' * 40}{Colors.RESET}")

        # Gerando e imprimindo a resposta em tempo real (Streaming)
        for chunk in model.stream(prompt):
            # Capturamos o texto do conteúdo de forma segura.
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            print(content, end="", flush=True)

        print(f"\n\n{Colors.GREEN}{'=' * 40}{Colors.RESET}\n")

    except ConnectionError:
        print(f"\n{Colors.RED}Erro: Não foi possível conectar ao Ollama. Certifique-se de que o comando 'ollama serve' está rodando no terminal.{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Ocorreu um erro inesperado: {e}{Colors.RESET}\n")

# Classe auxiliar para colorir saídas de terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

if __name__ == "__main__":
    questionFunction()