from langchain_community.document_loaders import DirectoryLoader, TextLoader


class DocsRead:
    def __init__(self, folder_base_dados: str):
        self.folder_base_dados = folder_base_dados

        self.read_docs = DirectoryLoader(
            path=self.folder_base_dados,
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )

    def load_txt_documents(self):
        return self.read_docs.load()