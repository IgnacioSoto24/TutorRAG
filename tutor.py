import os
import ollama
from pathlib import Path

def cargar_prompt():
    ruta = Path("prompts/generar_tarea_tutor.txt")
    with open(ruta, "r", encoding="utf-8") as archivo:
        return archivo.read()

def generar_tutoria(asignatura, curso, objetivo, contenido):
    prompt_base = cargar_prompt()

    prompt = prompt_base.format(
        asignatura=asignatura,
        curso=curso,
        objetivo=objetivo,
        contenido=contenido
    )

    respuesta = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    texto = respuesta["message"]["content"]
    
    if "Orientaciones:" in texto:
        partes = texto.split("Orientaciones:")
        escenario = partes[0].strip()
        orientaciones = partes[1].strip().split("\n")
        orientaciones = [o for o in orientaciones if o.strip()]
    else:
        escenario = texto
        orientaciones = []

    return escenario, orientaciones
