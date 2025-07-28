from langchain.embeddings import HuggingFaceEmbeddings

modelo_emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def crear_incrustaciones(textos):
    vectores = modelo_emb.embed_documents(textos)
    metadatos = [{"contenido": texto} for texto in textos]
    return vectores, metadatos
