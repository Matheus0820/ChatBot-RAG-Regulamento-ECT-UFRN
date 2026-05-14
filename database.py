import re
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter as TextSplit
from langchain_chroma.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

load_dotenv()

FOLDER_BASE_DADOS = 'base_dados'
PATH_DATABASE = 'database'

def createDatabase(): 
    documentos = carregarDocumentos()
    chunks = dividirChunks(documentos)
    vetorizarChunks(chunks)

def carregarDocumentos():
    leitorDocumentos = PyPDFDirectoryLoader(FOLDER_BASE_DADOS, glob="*.pdf")
    docs_brutos = leitorDocumentos.load()

    if docs_brutos: 
        # Remove a burocracia inicial da UFRN antes do "RESOLVE:"
        content_page1 = docs_brutos[0].page_content
        if "RESOLVE:" in content_page1:
            docs_brutos[0].page_content = content_page1.split("RESOLVE:")[-1]
        
        # Limpeza e normalização do texto para melhorar a precisão vetorial
        for doc in docs_brutos:
            doc.page_content = doc.page_content.replace('\n', ' ')
            doc.page_content = re.sub(r'\s+', ' ', doc.page_content).strip()

    return docs_brutos

def dividirChunks(docs):
    divididorChunks = TextSplit(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True
    )
    return divididorChunks.split_documents(docs)

def vetorizarChunks(chunks):
    embedding = OllamaEmbeddings(model="mxbai-embed-large")
    
    Chroma.from_documents(
        documents=chunks, 
        embedding=embedding, 
        persist_directory=PATH_DATABASE, 
        collection_metadata={"hnsw:space": "cosine"}
    )
    print("Banco de dados criado com sucesso!")

if __name__ == "__main__":
    createDatabase()