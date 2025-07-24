from langchain.llms import Ollama

# Usa el modelo descargado en Ollama (ejemplo: llama3)
modelo_llama = Ollama(model="llama3")

def generar_orientacion(prompt):
    """
    Recibe un prompt completo y lo envía a LLaMA.
    Retorna el texto generado.
    """
    return modelo_llama(prompt)
