# 🎓 UniNotes AI - Sistema RAG para Consulta de Apuntes

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Local_Vector_DB-orange?style=for-the-badge)](https://www.trychroma.com/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-NVIDIA_Nemotron-blue?style=for-the-badge)](https://openrouter.ai/)

**UniNotes AI** es una aplicación Full-Stack basada en arquitectura **RAG (Retrieval-Augmented Generation)** diseñada para interactuar dinámicamente con documentos PDF universitarios. Permite procesar apuntes en tiempo real, almacenarlos en una base de datos vectorial local y responder preguntas mediante un modelo de lenguaje masivo (LLM) sin sufrir de alucinaciones.

---

##  Arquitectura del Sistema

```text
┌────────────────┐       ┌────────────────────────┐       ┌────────────────────────┐
│                │       │                        │       │                        │
│  Streamlit UI  │ ────> │    FastAPI Backend     │ ────> │   ChromaDB (Vector)    │
│  (Frontend)    │ <──── │    (REST API)          │ <──── │   (Local Embeddings)   │
│                │       │                        │       └────────────────────────┘
└────────────────┘       └───────────┬────────────┘
                                     │
                                     ▼
                         ┌────────────────────────┐
                         │ OpenRouter API         │
                         │ (NVIDIA Nemotron 3)    │
                         └────────────────────────┘

```

## Características Principales

* **Procesamiento de PDF en Memoria:** Ingesta dinámica de archivos PDF sin necesidad de guardarlos temporalmente en disco.
* **Chunking Inteligente:** División del texto en fragmentos (*chunks*) optimizados para preservación contextual.
* **Búsqueda Semántica Local:** Almacenamiento e indexación en **ChromaDB** para recuperar únicamente los datos relevantes según la consulta.
* **Generación Aumentada (RAG):** *Prompt engineering* estructurado para garantizar que el modelo **NVIDIA Nemotron 3** responda exclusivamente basándose en la información de los apuntes.
* **Arquitectura Desacoplada:** Backend independiente expuesto mediante **FastAPI** con documentación automática e interactiva (**Swagger UI**).
* **Interfaz Interactiva:** Frontend conversacional tipo chat construido en **Streamlit** con soporte para *drag-and-drop*.

---

## Tech Stack

| Componente | Tecnología | Descripción |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Interfaz gráfica e interactiva de usuario |
| **Backend** | FastAPI / Uvicorn | Servidor asíncrono y gestión de endpoints HTTP |
| **Vector Database** | ChromaDB | Almacenamiento local de embeddings y búsqueda vectorial |
| **LLM Provider** | OpenRouter (NVIDIA) | Inferencia con el modelo `nvidia/nemotron-3-ultra:free` |
| **PDF Parser** | PyPDF | Extracción e ingesta de contenido textual |

```
```
### 1. Clonar el repositorio

```bash
git clone [https://github.com/DanielOT101106/ProyectoIA.git](https://github.com/DanielOT101106/ProyectoIA.git)
cd ProyectoIA

```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt

```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto y añade tu clave de API de OpenRouter:

```env
OPENROUTER_API_KEY=tu_api_key_aqui

```

---

## 💻 Ejecución del Proyecto

El proyecto requiere ejecutar dos servicios simultáneamente:

#### Paso 1: Arrancar el Backend (FastAPI)

```bash
uvicorn backend.main:app --reload

```

* **API Base:** `http://127.0.0.1:8000`
* **Documentación Swagger UI:** `http://127.0.0.1:8000/docs`

#### Paso 2: Arrancar el Frontend (Streamlit)

En una nueva pestaña de terminal:

```bash
streamlit run frontend/main.py

```

* **Interfaz Web:** `http://localhost:8501`

---

## 🔗 Endpoints de la API

* `GET /` - Health check del servidor backend.
* `POST /upload` - Recibe un archivo `.pdf`, extrae su texto e indexa los fragmentos en ChromaDB.
* `POST /ask` - Recibe una pregunta en lenguaje natural y genera una respuesta contextualizada mediante la IA.

---

## 👤 Autor

Desarrollado por **Daniel** - [GitHub Profile](https://www.google.com/search?q=https://github.com/DanielOT101106)

```
