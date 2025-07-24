import streamlit as st
from fpdf import FPDF
from utilidades.plantillas_prompts import prompt_tarea
from modulos.generador import generar_orientacion

st.set_page_config(page_title="Crear tarea", page_icon="📝")

st.title("📝 Crear Tarea Automáticamente")
st.write("Genera automáticamente preguntas a partir del **objetivo** y el **título de la tarea**.")

# Entradas del docente
titulo = st.text_input("📌 Título de la tarea")
objetivo = st.text_area("🎯 Objetivo de aprendizaje")

# === Paso 1: Generar preguntas automáticamente ===
if st.button("🤖 Generar preguntas automáticamente"):
    if not titulo.strip() or not objetivo.strip():
        st.warning("⚠️ Escribe al menos un objetivo y un título para generar preguntas.")
    else:
        with st.spinner("Generando preguntas según el objetivo..."):
            # ✅ Crear el prompt para tareas
            prompt = prompt_tarea(objetivo, titulo)
            preguntas_generadas = generar_orientacion(prompt)

        st.success("✅ Preguntas generadas automáticamente")
        # ✅ Mostramos las preguntas para que el docente pueda editarlas si quiere
        st.session_state["preguntas_tarea"] = st.text_area(
            "✏️ Edita las preguntas si es necesario:",
            preguntas_generadas,
            height=200,
        )

# === Paso 2: Si ya hay preguntas, habilitar PDF ===
if "preguntas_tarea" in st.session_state and st.session_state["preguntas_tarea"]:
    if st.button("📥 Descargar tarea en PDF"):
        preguntas_texto = st.session_state["preguntas_tarea"]

        # Crear el PDF con título, objetivo y preguntas
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, titulo, ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, f"Objetivo de aprendizaje:\n{objetivo}")
        pdf.ln(5)

        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Preguntas generadas:", ln=True)

        pdf.set_font("Arial", "", 12)
        for linea in preguntas_texto.split("\n"):
            pdf.multi_cell(0, 10, linea)
            pdf.ln(2)

        nombre_pdf = "tarea_generada.pdf"
        pdf.output(nombre_pdf)

        with open(nombre_pdf, "rb") as file:
            st.download_button(
                label="✅ Descargar tarea en PDF",
                data=file,
                file_name=nombre_pdf,
                mime="application/pdf"
            )
