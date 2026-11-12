import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="UniNotes AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 UniNotes AI")
st.caption("Tu asistente de estudio con Memoria y Citas Exactas.")

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# BARRA LATERAL
with st.sidebar:
    st.header("📄 Cargar Apuntes")
    uploaded_file = st.file_uploader("Selecciona un archivo PDF", type=["pdf"])

    if uploaded_file is not None:
        if st.button("🚀 Indexar PDF", type="primary", use_container_width=True):
            with st.spinner("Procesando e indexando..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    res = requests.post(f"{BACKEND_URL}/upload", files=files)
                    if res.status_code == 200:
                        st.success(f"¡Documento indexado!")
                    else:
                        st.error(f"Error: {res.json().get('detail')}")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")

    st.markdown("---")

    # BOTÓN PARA VACIAR BASE DE DATOS Y CHAT
    if st.button("🗑️ Vaciar Memoria / Borrar Datos", use_container_width=True):
        try:
            res = requests.delete(f"{BACKEND_URL}/clear")
            if res.status_code == 200:
                st.session_state.messages = []
                st.success("Base de datos y chat reiniciados.")
                st.rerun()
            else:
                st.error("No se pudo limpiar la base de datos.")
        except Exception as e:
            st.error(f"Error de conexión: {e}")

# MOSTRAR MENSAJES ANTERIORES
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📌 Fuentes consultadas"):
                for src in message["sources"]:
                    st.write(src)

# ENTRADA DEL USUARIO
if prompt := st.chat_input("Haz una pregunta sobre tus apuntes..."):
    # Renderizar pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta de la IA
    with st.chat_message("assistant"):
        with st.spinner("Pensando con contexto e historial..."):
            try:
                # Preparamos el payload con la pregunta y el historial actual
                payload = {
                    "question": prompt,
                    "history": [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages[:-1]
                    ]
                }

                res = requests.post(f"{BACKEND_URL}/ask", json=payload)

                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("answer")
                    sources = data.get("sources", [])

                    st.markdown(answer)

                    if sources:
                        with st.expander("📌 Fuentes consultadas"):
                            for src in sources:
                                st.write(src)

                    # Guardar respuesta y fuentes en el historial de sesión
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                else:
                    st.error(f"Error ({res.status_code}): {res.json().get('detail')}")
            except Exception as e:
                st.error(f"Error al conectar con el servidor: {e}")