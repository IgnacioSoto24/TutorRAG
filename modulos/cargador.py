import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader

def cargar_documentos_pdf(lista_pdfs):
    textos = []

    for archivo in lista_pdfs:
        # Crear archivo temporal para que PyPDFLoader lo pueda leer
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(archivo.read())  # Guardar el contenido del PDF subido
            tmp.flush()
            ruta_temp = tmp.name

        # Ahora sí, PyPDFLoader puede procesarlo
        loader = PyPDFLoader(ruta_temp)
        documentos = loader.load()

        for doc in documentos:
            textos.append(doc.page_content)

        # Opcional: eliminar el archivo temporal
        os.remove(ruta_temp)

    return textos
