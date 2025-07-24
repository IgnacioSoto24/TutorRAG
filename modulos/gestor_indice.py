import faiss
import numpy as np
import os

RUTA_INDICE = "indice/indice_faiss.bin"
RUTA_META = "indice/metadatos.npy"

def guardar_indice(vectores, metadatos):
    vectores_np = np.array(vectores).astype("float32")
    indice = faiss.IndexFlatL2(vectores_np.shape[1])
    indice.add(vectores_np)
    faiss.write_index(indice, RUTA_INDICE)
    np.save(RUTA_META, metadatos)

def cargar_indice_existente():
    if os.path.exists(RUTA_INDICE):
        return faiss.read_index(RUTA_INDICE)
    return None
