from langchain_text_splitters import RecursiveCharacterTextSplitter as TextSplit

class Chunking:
    """
    Essa classe tem como proposito receber os documento e reparticiona-los em chunks
    """
    
    def __init__(self, chunk_size, chunk_overlap, docs):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.docs = docs

        # Criando o divisor de Chunks
        self.chunk_divider = TextSplit(
            chunk_size = self.chunk_size,
            chunk_overlap = self.chunk_overlap,
            length_function = len,
            add_start_index = True
        )

        # Gerando as Chunks
        self.chunks = self.chunk_divider.split_documents(self.docs)


    def getChunks(self):
        return self.chunks

