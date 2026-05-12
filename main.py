# Importando bibliotecas 
from langchain_chroma.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Carregando credenciais
load_dotenv()

# Caminho do base de dados
PATH_DATABASE = 'database'

# Criando um prompt template 
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


# Função de processamento de pergunta

def questionFunction():
    # Pedindo pergunta ao usuário 
    question = input("Faça sua pergunta sobre o regulamento da ECT: ")

    # Carregando o banco de dados
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    database = Chroma(persist_directory=PATH_DATABASE, embedding_function=embedding)

    # Pegando o resultado do processamento
    result_question = database.similarity_search_with_relevance_scores(question, k=3)

    # Verificando os resultados
    print(result_question[0][1])
    if len(result_question) == 0 or result_question[0][1] < 0.2:
        print("Para essa pergunta não conseguimos achar resultados relevantes")
        return


    # Tratanto resultado
    listTextResult = []
    for result in result_question:
        text = result[0].page_content
        listTextResult.append(text)
    
    data_result = "\n\n ---- \n\n".join(listTextResult)

    # Configurando o prompt template
    prompt = ChatPromptTemplate.from_template(template_prompt)
    prompt = prompt.invoke({"question": question, "data_result": data_result})
    print(prompt) 
    
    # Mandando o prompt para a LLM
    model = ChatGroq(model="llama-3.3-70b-versatile")
    response_model = model.invoke(prompt)

    print(f"""
{'=' * 30}
Resposta do modelo:
{'=' * 30}
{response_model.content}
{'=' * 30}
    """)


questionFunction()
