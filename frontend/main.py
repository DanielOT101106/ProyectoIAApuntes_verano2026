import streamlit as st
import requests

# Dirección donde está corriendo tu servidor de FastAPI
BACKEND_URL = "http://127.0.0.1:8000"

# Configuración básica de la página web
st.set_page_config(
    page_title="UniNotes AI",
    page_icon="🎓",
    layout="wide"
)

# Título principal y subtítulo
st.title("🎓 UniNotes AI")
st.caption("Tu asistente personal de estudio. Sube tus apuntes en PDF y pregúntale lo que quieras.")

# ---------------------------------------------------------
# BARRA LATERAL: Subida de archivos
# ---------------------------------------------------------
with st.sidebar:
    st.header("📄 Cargar Apuntes")
    uploaded_file = st.file_uploader("Selecciona un archivo PDF", type=["pdf"])

    if uploaded_file is not None:
        if st.button("🚀 Indexar PDF", type="primary", use_container_width=True):
            with st.spinner("Extrayendo texto y guardando en ChromaDB..."):
                # Preparamos el archivo para enviarlo a la API de FastAPI (/upload)
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    response = requests.post(f"{BACKEND_URL}/upload", files=files)
                    if response.status_code == 200:
                        res_data = response.json()
                        st.success(f"¡Éxito! Documento procesado en {res_data.get('chunks_created')} fragmentos.")
                    else:
                        st.error(f"Error {response.status_code}: {response.json().get('detail')}")
                except Exception as e:
                    st.error(f"No se pudo conectar con el backend. Asegúrate de que FastAPI está corriendo.\n\nDetalle: {e}")

    st.markdown("---")
    st.markdown("### 💡 Consejos:")
    st.markdown("- Sube apuntes claros en PDF.")
    st.markdown("- Puedes hacer preguntas sobre resúmenes, conceptos clave o fechas.")

# ---------------------------------------------------------
# CHAT INTERACTIVO: Mensajes e Historial
# ---------------------------------------------------------
# Inicializamos el historial de conversación en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Dibujamos en pantalla los mensajes anteriores de la conversación
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto del usuario (Caja de chat al final)
if prompt := st.chat_input("Escribe tu pregunta sobre los apuntes..."):
    # 1. Mostrar el mensaje del usuario en el chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Consultar al Backend y mostrar la respuesta de la IA
    with st.chat_message("assistant"):
        with st.spinner("Analizando apuntes con NVIDIA..."):
            try:
                # Enviamos la pregunta a la API (/ask)
                res = requests.post(f"{BACKEND_URL}/ask", json={"question": prompt})
                if res.status_code == 200:
                    answer = res.json().get("answer")
                    st.markdown(answer)
                    # Guardamos la respuesta en el historial
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    error_msg = f"Error del servidor ({res.status_code}): {res.json().get('detail')}"
                    st.error(error_msg)
            except Exception as e:
                st.error(f"Error al conectar con la API: {e}")