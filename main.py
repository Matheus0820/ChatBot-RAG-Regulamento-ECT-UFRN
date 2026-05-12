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
Responda a seguinte pergunta do aluno de C&T de forma fácil de ser entendida. Pergunta:
{question}

Responda ela com base nesses dados:
{data_result}

Caso não saiba responder a pergunta, ou seja, não achar uma resposta para a pergunta do aluno, responda que não sabe responder no momento.
"""


# Função de processamento de pergunta

def questionFunction():
    # Pedindo pergunta ao usuário 
    question = input("Faça sua pergunta sobre o regulamento da ECT: ")

    # Carregando o banco de dados
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
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
    
    # Mandando o prompt para a LLM
    model = ChatGroq(model="llama-3.3-70b-versatile")
    response_model = model.invoke(prompt)
    print(response_model.content)


questionFunction()
