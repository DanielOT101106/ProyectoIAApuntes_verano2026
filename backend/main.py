from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from backend.core.ai_engine import generate_answer, ingest_pdf_bytes, clear_database

app = FastAPI(
    title="UniNotes AI API",
    description="API profesional para consultar apuntes universitarios usando RAG con Memoria y Citas",
    version="1.2.0"
)

class ChatMessage(BaseModel):
    role: str
    content: str

class QuestionRequest(BaseModel):
    question: str
    history: Optional[List[ChatMessage]] = []

@app.get("/")
def home():
    return {"status": "ok", "message": "UniNotes AI v1.2 backend funcionando 🚀"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Formato no permitido. Solo se admiten archivos .pdf")

    try:
        file_bytes = await file.read()
        num_chunks = ingest_pdf_bytes(file_bytes, file.filename)
        return {
            "status": "success",
            "filename": file.filename,
            "chunks_created": num_chunks,
            "message": f"¡Éxito! Documento '{file.filename}' procesado e indexado."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
def ask_question(body: QuestionRequest):
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")

    try:
        # Convertimos el modelo Pydantic a lista de dicts para el engine
        history_dicts = [msg.model_dump() for msg in body.history] if body.history else []
        result = generate_answer(body.question, history=history_dicts)

        return {
            "question": body.question,
            "answer": result["answer"],
            "sources": result["sources"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el motor de IA: {str(e)}")

@app.delete("/clear")
def clear_db():
    """Borra todos los datos vectoriales almacenados."""
    try:
        clear_database()
        return {"status": "success", "message": "Base de datos vectorial limpiada correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al limpiar la base de datos: {str(e)}")