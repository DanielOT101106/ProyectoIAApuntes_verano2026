import os
import io
from pypdf import PdfReader
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
CHROMA_PATH = Path(__file__).resolve().parents[2] / "chroma_db"
chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))
COLLECTION_NAME = "universidad_apuntes"
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

ai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def clear_database():
    """Borra todos los documentos guardados en ChromaDB y recrea la colección vacía."""
    global collection
    chroma_client.delete_collection(name=COLLECTION_NAME)
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

def ingest_pdf_bytes(file_bytes: bytes, filename: str) -> int:
    pdf_file = io.BytesIO(file_bytes)
    reader = PdfReader(pdf_file)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    if not full_text.strip():
        raise ValueError("El archivo PDF está vacío o su texto no es legible.")

    chunk_size = 1000
    chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]

    documents = []
    metadatas = []
    ids = []

    for idx, chunk in enumerate(chunks):
        documents.append(chunk)
        metadatas.append({"source": filename, "chunk_index": idx + 1})
        ids.append(f"{filename}_chunk_{idx}")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    return len(chunks)

def generate_answer(question: str, history: list = None) -> dict:
    """
    Busca fragmentos relevantes, añade el historial de conversación
    y devuelve la respuesta junto con las fuentes utilizadas.
    """
    if history is None:
        history = []

    # 1. Recuperar contexto de ChromaDB
    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    context = ""
    sources = []

    if results and 'documents' in results and results['documents'] and results['documents'][0]:
        context = "\n\n".join(results['documents'][0])
        # Extraer metadatos de las fuentes utilizadas
        for meta in results['metadatas'][0]:
            source_str = f"📄 {meta.get('source', 'Documento')} (Bloque #{meta.get('chunk_index')})"
            if source_str not in sources:
                sources.append(source_str)

    # 2. Construir el historial para el prompt
    messages = [
        {
            "role": "system",
            "content": (
                "Eres UniNotes AI, un tutor académico experto. Responde a la pregunta del usuario utilizando "
                "el contexto proporcionado. Si la información no está en el contexto, indícalo amablemente. "
                f"\n\nCONTEXTO DE LOS APUNTES:\n{context}"
            )
        }
    ]

    # Añadimos los últimos 4 mensajes del historial para dar memoria a la IA
    for msg in history[-4:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Añadimos la pregunta actual
    messages.append({"role": "user", "content": question})

    # 3. Llamada al modelo con OpenRouter
    completion = ai_client.chat.completions.create(
        model="nvidia/nemotron-3-ultra:free",
        messages=messages,
        temperature=0.3
    )

    answer_text = completion.choices[0].message.content

    return {
        "answer": answer_text,
        "sources": sources
    }