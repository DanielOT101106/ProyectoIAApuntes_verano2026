import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

# Cargamos las claves del archivo .env
load_dotenv()

# Inicializamos el cliente de ChromaDB
chroma_client = chromadb.PersistentClient(path="./data/vector_db")

# Inicializamos el cliente usando la infraestructura de OpenRouter
ai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def save_chunks_to_db(chunks: list, collection_name: str = "university_notes"):
    """Guarda los trozos en ChromaDB (Función oficial ya probada)"""
    collection = chroma_client.get_or_create_collection(name=collection_name)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, ids=ids)
    print(f"✅ Guardados {len(chunks)} trozos en ChromaDB.")

def search_relevant_chunks(query: str, collection_name: str = "university_notes", n_results: int = 3) -> list:
    """Busca los trozos más relevantes en ChromaDB"""
    collection = chroma_client.get_or_create_collection(name=collection_name)
    results = collection.query(query_texts=[query], n_results=n_results)
    return results['documents'][0]

def generate_answer(question: str) -> str:
    """
    Busca en ChromaDB y le pasa el contexto a Llama 3 a través de OpenRouter.
    """
    # 1. Buscar los fragmentos de apuntes relevantes
    context_chunks = search_relevant_chunks(question, n_results=3)
    context = "\n---\n".join(context_chunks)

    # 2. Crear las instrucciones
    prompt = f"""
    Eres un asistente de estudio universitario brillante y empático. Tu trabajo es responder a la pregunta del estudiante basándote ÚNICAMENTE en el contexto de los apuntes proporcionados a continuación.
    
    Si el contexto no contiene la información para responder, di amablemente: "Lo siento, no encuentro esa información en los apuntes que has subido". No inventes nada.
    
    CONTEXTO DE LOS APUNTES:
    {context}
    
    PREGUNTA DEL ESTUDIANTE:
    {question}
    """

    # 3. Llamar a OpenRouter usando un modelo Llama 3 gratuito
    completion = ai_client.chat.completions.create(
        model="tencent/hy3:free",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return completion.choices[0].message.content