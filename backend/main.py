from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.core.ai_engine import generate_answer

# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="UniNotes AI API",
    description="API profesional para consultar apuntes universitarios usando RAG",
    version="1.0.0"
)

# Definimos la estructura de los datos que esperamos recibir (el "contrato")
class QuestionRequest(BaseModel):
    question: str

# 1. Ruta de bienvenida (Health Check)
@app.get("/")
def home():
    return {"status": "ok", "message": "El servidor de UniNotes AI está rugiendo perfectamente 🚀"}

# 2. Ruta principal para preguntar a tus apuntes
@app.post("/ask")
def ask_question(body: QuestionRequest):
    """
    Recibe una pregunta, busca en ChromaDB y responde usando la IA de NVIDIA.
    """
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")

    try:
        # Llamamos a la función que perfeccionamos en el paso anterior
        answer = generate_answer(body.question)
        return {
            "question": body.question,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor de IA: {str(e)}")