from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# Cargar documentos desde la carpeta /rag/data
def cargar_documentos():
    loader = DirectoryLoader("rag/data", glob="**/*.pdf", loader_cls=PyPDFLoader)
    return loader.load()

# Procesar e indexar
def crear_indice():
    documentos = cargar_documentos()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    docs = splitter.split_documents(documentos)

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    db.save_local("rag/vector_db_sicrea")

    print("✅ Índice creado y guardado en /rag/vector_db_sicrea")

if __name__ == "__main__":
    crear_indice()