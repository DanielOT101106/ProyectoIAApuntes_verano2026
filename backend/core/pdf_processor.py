import os
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Abre un archivo PDF y extrae todo su texto en un solo string.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"No se encontró el archivo en: {pdf_path}")

    reader = PdfReader(pdf_path)
    full_text = []

    # Recorremos cada página del PDF y extraemos el texto
    for page in reader.pages:
        text = page.extract_text()
        if text:  # Aseguramos que la página no esté vacía (como una imagen)
            full_text.append(text)

    # Unimos todo el texto con saltos de línea
    return "\n".join(full_text)

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    """
    Trocea un texto largo en fragmentos (chunks) más pequeños.
    - chunk_size: caracteres máximos por trozo.
    - chunk_overlap: caracteres que se solapan entre un trozo y el siguiente
                     (para no cortar frases por la mitad y perder contexto).
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        # Avanzamos el puntero restando el solapamiento
        start += chunk_size - chunk_overlap

    return chunks