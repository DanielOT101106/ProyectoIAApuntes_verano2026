import os
import io
from pypdf import PdfReader
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Inicializamos el cliente local de ChromaDB (guardará los datos en la carpeta ./chroma_db)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="universidad_apuntes")

# Inicializamos el cliente de OpenRouter para conectar con NVIDIA
ai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def ingest_pdf_bytes(file_bytes: bytes, filename: str) -> int:
    """
    Recibe un PDF en formato de bytes, extrae su texto,
    lo trocea y lo almacena indexado en ChromaDB.
    """
    # 1. Leer el PDF desde la memoria RAM (sin guardarlo en disco)
    pdf_file = io.BytesIO(file_bytes)
    reader = PdfReader(pdf_file)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    if not full_text.strip():
        raise ValueError("El archivo PDF está vacío o su texto no es legible.")

    # 2. Trocear el texto de forma inteligente (Chunking)
    # Creamos bloques de 1000 caracteres para que la IA los procese mejor
    chunk_size = 1000
    chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]

    # 3. Preparar los datos para ChromaDB
    documents = []
    metadatas = []
    ids = []

    for idx, chunk in enumerate(chunks):
        documents.append(chunk)
        metadatas.append({"source": filename, "chunk_index": idx})
        ids.append(f"{filename}_chunk_{idx}") # ID único para que no se pisen

    # 4. Guardar los trozos en la base de datos vectorial
    collection.add(
        documents=documents,
        metadatas=metadatas if 'metandatas' in locals() else metadatas, # Pequeño seguro por compatibilidad
        ids=ids
    )

    return len(chunks)

def generate_answer(question: str) -> str:
    """
    Busca los fragmentos más relevantes en ChromaDB y genera la respuesta con la IA.
    """
    # Recuperamos los 2 fragmentos que semánticamente se parecen más a la pregunta
    results = collection.query(
        query_texts=[question],
        n_results=2
    )

    context = ""
    if results and 'documents' in results and results['documents']:
        context = "\n\n".join(results['documents'][0])

    # Construimos el prompt con la técnica RAG
    prompt = f"""
    Eres un asistente de IA experto en resumir y explicar apuntes universitarios.
    Utiliza ÚNICAMENTE la siguiente información para responder a la pregunta del usuario. 
    Si la información no es suficiente, dilo amablemente, no inventes nada.

    CONTEXTO EXTRAÍDO DE LOS APUNTES:
    {context}

    PREGUNTA DEL USUARIO:
    {question}

    RESPUESTA (en un español claro, profesional y estructurado):
    """

    completion = ai_client.chat.completions.create(
        model="nvidia/nemotron-3-ultra:free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return completion.choices[0].message.content