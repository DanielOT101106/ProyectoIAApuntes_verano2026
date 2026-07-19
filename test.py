from backend.core.pdf_processor import extract_text_from_pdf, chunk_text
from backend.core.ai_engine import save_chunks_to_db, generate_answer

try:
    # 1. PROCESAR Y GUARDAR LOS APUNTES
    # (Esto creará la colección en ChromaDB y guardará los textos en tu ordenador)
    print("⏳ Procesando el PDF 'data/apuntes.pdf'...")
    texto = extract_text_from_pdf("data/apuntes.pdf")

    print("⏳ Troceando el texto...")
    trozos = chunk_text(texto)

    print("⏳ Guardando los trozos en ChromaDB (Creando la base de datos)...")
    save_chunks_to_db(trozos)

    # 2. PREGUNTAR A LA IA
    # 💡 RECUERDA: Cambia esta pregunta por algo real que venga dentro de tu PDF
    pregunta = "Resumeme de q va el trabajo"

    print(f"\n🤔 Preguntando a la IA sobre tus apuntes: '{pregunta}'...\n")

    respuesta = generate_answer(pregunta)

    print("🤖 RESPUESTA DE TU ASISTENTE DE IA:")
    print(respuesta)

except Exception as e:
    print(f"❌ Error: {e}")