from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document

# Inicializar la base vectorial una sola vez
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.load_local("rag/vector_db_sicrea", embeddings, allow_dangerous_deserialization=True)

# Recuperar contexto relevante dado un mensaje de usuario
def recuperar_contexto(pregunta_usuario, k=3):
    documentos_similares = vectorstore.similarity_search(pregunta_usuario, k=k)
    
    # Combinar el contenido en un solo string
    contexto = "\n".join([doc.page_content for doc in documentos_similares])
    return contexto

# Solo para pruebas
if __name__ == "__main__":
    pregunta = "¿Cuáles son los requisitos para obtener un financiamiento con SICREA?"
    contexto = recuperar_contexto(pregunta)
    print("🧠 Contexto recuperado:")
    print(contexto)