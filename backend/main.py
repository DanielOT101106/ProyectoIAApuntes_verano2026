from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from backend.core.ai_engine import generate_answer, ingest_pdf_bytes

app = FastAPI(
    title="UniNotes AI API",
    description="API profesional para consultar apuntes universitarios usando RAG",
    version="1.1.0"
)

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"status": "ok", "message": "El servidor de UniNotes AI está listo y dinámico 🚀"}

# --- NUEVO ENDPOINT DINÁMICO ---
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint para subir cualquier archivo PDF. Extrae su texto,
    lo procesa en fragmentos y lo indexa en la base de datos vectorial.
    """
    # Validación de seguridad elemental: solo PDFs
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Formato no permitido. Solo se admiten archivos .pdf")

    try:
        # Leemos los bytes del archivo que el usuario nos envía en streaming
        file_bytes = await file.read()

        # Procesamos el archivo usando la nueva función del motor
        num_chunks = ingest_pdf_bytes(file_bytes, file.filename)

        return {
            "status": "success",
            "filename": file.filename,
            "chunks_created": num_chunks,
            "message": f"¡Éxito! El documento '{file.filename}' ha sido procesado e indexado en ChromaDB en {num_chunks} trozos. 🧠"
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error crítico al procesar el archivo: {str(e)}")

@app.post("/ask")
def ask_question(body: QuestionRequest):
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")

    try:
        answer = generate_answer(body.question)
        return {
            "question": body.question,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor de IA: {str(e)}")