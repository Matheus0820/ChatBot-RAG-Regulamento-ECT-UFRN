# Importanto bibliotecas
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter as TextSplit
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

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
    documentos = leitorDocumentos.load()

    return documentos # Lista de documentos


def dividirChunks(docs):
    divididorChunks = TextSplit (
        chunk_size = 3000, # 3000 Caracteres em cada chunk
        chunk_overlap = 500, # Quantos caracteres ele vai começar antes do fim do chunk anterior
        length_function = len, # Função que vai definir o tamanho dele
        add_start_index = True # Diz o index do caractere inicial do chunk
    )

    chunks = divididorChunks.split_documents(docs)
    return chunks

def vetorizarChunks(chunks):
    db = Chroma.from_documents(chunks, OpenAIEmbeddings(), persist_directory="database")
    print("Banco de dados Criado!")

createDatabase()