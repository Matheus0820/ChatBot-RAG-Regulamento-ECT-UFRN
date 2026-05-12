# Importanto bibliotecas
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter as TextSplit
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import re

# Carregando a .env
load_dotenv()

FOLDER_BASE_DADOS = 'base_dados'

def createDatabase(): 
    # Carregar Documentos
    documentos = carregarDocumentos()

    # Dividir o documento nas chunks
    chunks = dividirChunks(documentos)

    # Vetorizar essas chunks
    chunks = vetorizarChunks(chunks)


def carregarDocumentos():
    leitorDocumentos = PyPDFDirectoryLoader(FOLDER_BASE_DADOS, glob="*.pdf")
    docs_brutos = leitorDocumentos.load()

    # Tratamento dos dados do documentos
    ## Removendo cabeçalho das páginas
    if len(docs_brutos) > 0: 
        # Limpando os dados da primeira página do pdf
        content_page1 = docs_brutos[0].page_content
        
        # Os dados começam a partir da palavra "RESOLVE:"
        if "RESOLVE:" in content_page1:
            docs_brutos[0].page_content = content_page1.split("RESOLVE:")[-1]
        
        # Limpeza geral das páginas
        for doc in docs_brutos:
            doc.page_content = doc.page_content.replace('\n', ' ')

            # Remover espaços duplos
            doc.page_content = re.sub(r'\s+', ' ', doc.page_content).strip()


    return docs_brutos # Lista de documentos


def dividirChunks(docs):
    divididorChunks = TextSplit (
        chunk_size = 800, # 800 Caracteres em cada chunk
        chunk_overlap = 100, # Quantos caracteres ele vai começar antes do fim do chunk anterior
        length_function = len, # Função que vai definir o tamanho dele
        add_start_index = True # Diz o index do caractere inicial do chunk
    )

    chunks = divididorChunks.split_documents(docs)
    return chunks

def vetorizarChunks(chunks):
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # db = Chroma.from_documents(chunks, OpenAIEmbeddings(), persist_directory="database")
    db = Chroma.from_documents(chunks, embedding, persist_directory="database", collection_metadata={"hnsw:space": "cosine"})
    print("Banco de dados Criado!")

createDatabase()