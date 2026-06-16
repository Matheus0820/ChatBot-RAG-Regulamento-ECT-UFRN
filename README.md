# ChatBot RAG - Regulamento ECT/UFRN

Sistema de chatbot utilizando **RAG (Retrieval-Augmented Generation)** para responder perguntas relacionadas ao regulamento da Escola de Ciências e Tecnologia (ECT) da UFRN.

O projeto utiliza modelos de linguagem (LLMs), banco vetorial e recuperação semântica de documentos para fornecer respostas contextualizadas baseadas no regulamento institucional.

---

# Objetivo do Projeto

Este projeto foi desenvolvido para permitir consultas inteligentes ao regulamento da ECT/UFRN através de linguagem natural.

Com a técnica de **RAG (Retrieval-Augmented Generation)**, o sistema:

1. Recupera trechos relevantes do regulamento;
2. Envia o contexto para um modelo de linguagem;
3. Gera respostas contextualizadas e mais precisas.

Esse tipo de arquitetura reduz alucinações do modelo e melhora a qualidade das respostas em domínios específicos.

---

# Tecnologias Utilizadas

- Python
- LangChain
- ChromaDB
- Ollama
- Groq
- Streamlit
- Embeddings
- Modelos LLM locais

---

# Estrutura do Projeto
## Pasta de aplicação (app)
```mermaid
---
config:
  theme: neo
  layout: dagre
---
graph TB

    app["📁 app"]

    subgraph CORE ["📁 core"]
        core_desc["Configurações do projeto"]
    end

    subgraph DATABASE ["📁 database"]
        chat_repository["📄 chat_repository.py"]
    end

    subgraph LLM ["📁 llm"]
        history["📄 history.py"]
        prompt_build["📄 prompt_build.py"]
        prompts["📄 prompts.yaml"]

        subgraph MODELS ["📁 models"]
            groq_model["📄 groq_model.py"]
        end
    end

    subgraph RAG ["📁 rag"]
        chunking["📄 chunking.py"]
        docs_read["📄 docs_read.py"]
        embeddings["📄 embeddings.py"]
        pipeline["📄 pipeline.py"]
        retriever["📄 retriever.py"]
        vectorstore["📄 vectorstore.py"]
    end

    subgraph SERVICES ["📁 services"]
        chatbot_service["📄 chatbot_service.py"]
    end

    app --> CORE
    app --> DATABASE
    app --> LLM
    app --> RAG
    app --> SERVICES

    classDef folder fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#000;
    classDef file fill:#f8fafc,stroke:#64748b,color:#000;

    class CORE,DATABASE,LLM,MODELS,RAG,SERVICES folder;
    class chat_repository,groq_model,history,prompt_build,prompts,chunking,docs_read,embeddings,pipeline,retriever,vectorstore,chatbot_service,core_desc file;
```

## Pasta de integração com a interface WEB (ui)
```mermaid
---
config:
  theme: neo
  layout: dagre
---
flowchart TB
 subgraph STREAMLIT["📁 .streamlit"]
        config["📄 config.toml"]
  end
 subgraph PAGES["📁 pages"]
        chat["📄 chat_chatbot.py"]
  end
    ui["📁 ui"] --> app["📄 streamlit_app.py"] & STREAMLIT & PAGES

     config:::file
     chat:::file
     app:::file
     STREAMLIT:::folder
     PAGES:::folder
    classDef folder fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#000
    classDef file fill:#f8fafc,stroke:#64748b,color:#000
    style ui stroke-width:2px,stroke-dasharray: 0
```

---

# Rodando o projeto

## Dependências 
### Python
```bash

pip install -r requirements.txt

```

### Ollama
#### Instalar o Ollama
```bash

curl -fsSL https://ollama.com/install.sh | sh

```

#### Execultar o Ollama
```bash

ollama serve

```

#### Baixando modelo necessário do Ollama
```bash

ollama pull mxbai-embed-large

```

### Configurando o .env
A estrutura do **.env** ideal está no arquivo **.env.exemple**. Pegue a chave do GROQ no site da API do GROQ: https://console.groq.com/keys

### Execultando o arquivo StreamLit do projeto (main)
Na raiz do projeto rode o seguinte comando:

```bash

streamlit run ui/streamlit_app.py

```
