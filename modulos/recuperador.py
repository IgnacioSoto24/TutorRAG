import numpy as np
from modulos.gestor_indice import cargar_indice_existente
from modulos.incrustador import modelo_emb
import numpy as np

def recuperar_contexto(pregunta, k=3):
    indice = cargar_indice_existente()
    if indice is None:
        return "No hay índice disponible. Sube documentos primero."
    
    vector_pregunta = np.array(modelo_emb.embed_query(pregunta)).astype("float32").reshape(1, -1)
    distancias, indices = indice.search(vector_pregunta, k)

    from numpy import load
    metadatos = load("indice/metadatos.npy", allow_pickle=True)
    contexto = [metadatos[i]["contenido"] for i in indices[0] if i < len(metadatos)]
    return "\n".join(contexto)
