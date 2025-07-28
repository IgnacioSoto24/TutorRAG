import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader

def cargar_documentos_pdf(lista_pdfs):
    textos = []

    for archivo in lista_pdfs:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(archivo.read())
            tmp.flush()
            ruta_temp = tmp.name

        loader = PyPDFLoader(ruta_temp)
        documentos = loader.load()

        for doc in documentos:
            textos.append(doc.page_content)

        os.remove(ruta_temp)

    return textos
