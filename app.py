import streamlit as st
from tutor import generar_tutoria

st.set_page_config(page_title="EvaluAR - Tutor Pedagógico", layout="centered")

st.title("📚 EvaluAR - Tutor Pedagógico IA")

st.markdown("### Completa la información para recibir orientación sobre un escenario educativo.")

with st.form("formulario_tutoria"):
    nombre = st.text_input("Nombre del estudiante")
    asignatura = st.selectbox("Asignatura", ["Lenguaje", "Matemáticas", "Ciencias", "Historia"])
    curso = st.selectbox("Curso", ["1° Básico", "2° Básico", "3° Básico", "4° Básico", "5° Básico", "6° Básico", "7° Básico", "8° Básico", "1° Medio", "2° Medio", "3° Medio", "4° Medio"])
    objetivo = st.text_area("Objetivo de aprendizaje (OA)")
    contenido = st.text_area("Contenido a trabajar")

    submit = st.form_submit_button("Generar Escenario")

if submit:
    st.markdown("### ✨ Escenario de aprendizaje:")
    escenario, orientaciones = generar_tutoria(asignatura, curso, objetivo, contenido)
    
    st.markdown(f"**Escenario**: {escenario}")
    st.markdown("### 🧠 Tutor IA - Orientación:")
    for orientacion in orientaciones:
        st.info(orientacion)

    st.markdown("---")
    st.success("Puedes pensar tu respuesta antes de continuar. ¡Buena suerte!")
