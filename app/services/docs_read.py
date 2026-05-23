from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader


class DocsRead:
    def __init__(self, folder_base_dados):
        self.folder_base_dados = folder_base_dados
        
        self.read_docs = DirectoryLoader(
            self.folder_base_dados,
            glob="*.txt",
            loader_cls=lambda path: TextLoader(
                path,
                encoding="utf-8"
            )
        )

    def load_txt_documents(self):
        docs = self.read_docs.load()
        return docs