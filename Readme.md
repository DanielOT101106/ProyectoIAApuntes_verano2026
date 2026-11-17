# 🎓 UniNotes AI

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-orange?style=for-the-badge)](https://www.trychroma.com/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-NVIDIA_Nemotron-blue?style=for-the-badge)](https://openrouter.ai/)

**UniNotes AI** es una aplicación full-stack con arquitectura **RAG (Retrieval-Augmented Generation)** para hacer preguntas sobre tus apuntes en PDF. Subes un documento, se indexa en una base de datos vectorial local y un modelo de lenguaje responde usando únicamente el contenido de tus apuntes, citando de qué fragmento sale cada respuesta.

## Capturas

![Subida de un PDF](docs/captura-subida.png)
![Respuesta con fuentes](docs/captura-respuesta.png)

## Características

- **Ingesta de PDF en memoria:** el archivo se procesa sin guardarse en disco.
- **Búsqueda semántica:** los apuntes se dividen en fragmentos y se indexan en ChromaDB para recuperar solo lo relevante.
- **Citas de fuentes:** cada respuesta indica de qué documento y bloque procede la información.
- **Memoria de conversación:** el chat usa los últimos mensajes como contexto.
- **API REST desacoplada:** backend en FastAPI con documentación Swagger automática.
- **Interfaz de chat:** frontend en Streamlit con subida de archivos.

## Arquitectura

```text
┌───────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ Streamlit UI  │ ──> │ FastAPI backend  │ ──> │ ChromaDB (local) │
│ (frontend)    │ <── │ (API REST)       │ <── │ (embeddings)     │
└───────────────┘     └────────┬─────────┘     └──────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ OpenRouter API       │
                    │ (NVIDIA Nemotron)    │
                    └──────────────────────┘
```

## Tecnologías

| Componente | Tecnología |
| :--- | :--- |
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| Base de datos vectorial | ChromaDB |
| Modelo de lenguaje | OpenRouter (`nvidia/nemotron-3-ultra:free`) |
| Lectura de PDF | pypdf |

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/DanielOT101106/ProyectoIAApuntes_verano2026.git
cd ProyectoIAApuntes_verano2026
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la clave de API

Copia la plantilla y añade tu clave de [OpenRouter](https://openrouter.ai/):

```bash
cp .env.example .env        # Windows: copy .env.example .env
```

Edita `.env`:

```env
OPENROUTER_API_KEY=tu_clave_aqui
```

## Ejecución

Hacen falta dos terminales, con el entorno virtual activado en ambas.

**Terminal 1: backend**

```bash
uvicorn backend.main:app --reload
```

- API: http://127.0.0.1:8000
- Documentación Swagger: http://127.0.0.1:8000/docs

**Terminal 2: frontend**

```bash
streamlit run frontend/main.py
```

- Interfaz web: http://localhost:8501

## Endpoints de la API

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/` | Comprobación de estado del servidor |
| `POST` | `/upload` | Recibe un `.pdf`, extrae el texto e indexa los fragmentos |
| `POST` | `/ask` | Recibe una pregunta (y el historial) y devuelve respuesta y fuentes |
| `DELETE` | `/clear` | Borra todos los datos de la base vectorial |

## Autor

Desarrollado por **Daniel Ortiz Terrón**, estudiante de Ingeniería del Software en la Universidad de Málaga.
[GitHub](https://github.com/DanielOT101106) · [LinkedIn](https://www.linkedin.com/in/daniel-ortiz-372518369)