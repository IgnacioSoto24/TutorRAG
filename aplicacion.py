import streamlit as st
from modulos.cargador import cargar_documentos_pdf
from modulos.incrustador import crear_incrustaciones
from modulos.gestor_indice import guardar_indice, cargar_indice_existente
from modulos.recuperador import recuperar_contexto
from modulos.generador import generar_orientacion
from utilidades.plantillas_prompts import prompt_tutor

# ===========================
# 🎨 ESTILOS PERSONALIZADOS
# ===========================
st.set_page_config(page_title="TutorRAG", page_icon="📚", layout="wide")

CUSTOM_CSS = """
<style>
    .stApp {
        background: linear-gradient(135deg, #e0f7fa, #f1f8e9);
        font-family: 'Segoe UI', sans-serif;
    }
    .main-title {
        text-align: center;
        color: #2e7d32;
        font-size: 36px;
        font-weight: bold;
    }
    .sub-title {
        text-align: center;
        color: #388e3c;
        font-size: 20px;
        margin-bottom: 30px;
    }
    hr {
        border: none;
        height: 2px;
        background: #81c784;
        margin: 20px 0;
    }
    .context-box {
        background: #ffffffcc;
        border-left: 5px solid #66bb6a;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .answer-box {
        background: #e8f5e9;
        border-left: 5px solid #43a047;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .history-box {
        background: #f1f8e9;
        padding: 10px;
        border-radius: 10px;
        font-size: 14px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ===========================
# 🌟 ENCABEZADO PRINCIPAL
# ===========================
st.markdown("<div class='main-title'>📚 TutorRAG</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Asistente pedagógico inteligente para apoyar la evaluación auténtica</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ===========================
# INFO SOBRE MULTIPÁGINA
# ===========================
st.sidebar.info(
    "📄 Usa el menú lateral para navegar entre páginas.\n\n"
    "✅ **Página principal:** Consultas al tutor.\n"
    "✅ **Crear Tarea:** Genera tareas en PDF automáticamente."
)

# ===========================
# 📂 SECCIÓN LAYOUT
# ===========================
col1, col2 = st.columns([1, 2])

# === COL1: GESTIÓN DEL CORPUS ===
with col1:
    st.subheader("📂 Gestión del Corpus")
    st.write("Sube documentos curriculares en PDF para que el tutor los utilice.")

    pdfs = st.file_uploader("Selecciona documentos curriculares (PDF)", type=["pdf"], accept_multiple_files=True)

    if st.button("🔄 Procesar y crear índice"):
        if pdfs:
            with st.spinner("⏳ Procesando documentos y generando índice..."):
                textos = cargar_documentos_pdf(pdfs)
                vectores, metadatos = crear_incrustaciones(textos)
                guardar_indice(vectores, metadatos)
                st.success("✅ Índice creado correctamente.")
        else:
            st.warning("⚠️ Primero sube al menos un documento PDF.")

    if st.button("📥 Cargar índice existente"):
        cargar_indice_existente()
        st.success("✅ Índice cargado desde disco.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("📜 Historial de consultas")
    if "historial" not in st.session_state:
        st.session_state.historial = []

    # Mostrar historial si existe
    if st.session_state.historial:
        for h in reversed(st.session_state.historial[-5:]):  # últimas 5 preguntas
            st.markdown(
                f"<div class='history-box'><b>❓ {h['pregunta']}</b><br>💡 {h['respuesta']}</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("Todavía no hay historial de preguntas.")

# === COL2: INTERACCIÓN CON EL TUTOR ===
with col2:
    st.subheader("🤔 Haz una consulta")
    pregunta = st.text_input("✏️ Escribe tu pregunta sobre el contenido curricular:")

    if st.button("💡 Obtener orientación"):
        if pregunta.strip():
            with st.spinner("🔍 Buscando en el currículo y generando orientación..."):
                contexto = recuperar_contexto(pregunta)
                # ✅ Generar el prompt dinámico del tutor
                prompt = prompt_tutor(contexto, pregunta)
                respuesta = generar_orientacion(prompt)

                st.markdown("### ✅ Orientación generada:")
                st.markdown(
                    f"<div class='answer-box'>{respuesta}</div>", unsafe_allow_html=True
                )

                # Guardar en historial
                st.session_state.historial.append(
                    {"pregunta": pregunta, "respuesta": respuesta}
                )
        else:
            st.warning("⚠️ Escribe una pregunta antes de continuar.")

# ===========================
# 🔗 BOTÓN EXTRA PARA RECORDAR CREAR TAREA
# ===========================
st.markdown("<hr>", unsafe_allow_html=True)
st.write(
    "¿Eres docente? 👉 Ve a la página **Crear Tarea** desde el menú lateral para generar actividades y descargarlas en PDF."
)
