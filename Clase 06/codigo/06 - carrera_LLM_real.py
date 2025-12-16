"""Comparativa de llamadas reales a OpenAI: secuencial vs. asíncrona.

Requisitos previos:
- Añade tu API key en un archivo `.env` con la clave `OPENAI_API_KEY`.
- Instala dependencias: `pip install python-dotenv httpx`

Ejecuta:
    python "06 - carrera_LLM_real.py"
"""

import asyncio
import os
import sys
import time
from typing import List, Tuple

try:
    from dotenv import load_dotenv
    import httpx
except ImportError:
    print("Faltan dependencias necesarias: python-dotenv y httpx.")
    print("Instálalas con:")
    print("    pip install python-dotenv httpx")
    sys.exit(1)

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    print("No se encontró la variable OPENAI_API_KEY en el entorno. Añádela a tu .env.")
    sys.exit(1)

OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
MODELO_DEFECTO = "gpt-4o-mini"


async def consultar_openai(tema: str, model: str = MODELO_DEFECTO) -> Tuple[str, float]:
    """Solicita a OpenAI un chiste corto sobre el tema indicado."""
    prompt = f"Dame un chiste corto sobre {tema}."
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    json_payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Responde siempre en español."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 200,
        "temperature": 0.9,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        inicio = time.perf_counter()
        respuesta = await client.post(OPENAI_CHAT_URL, headers=headers, json=json_payload)
        fin = time.perf_counter()

    duracion = fin - inicio

    if respuesta.status_code != 200:
        return (f"ERROR {respuesta.status_code}: {respuesta.text}", duracion)

    try:
        contenido = respuesta.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        contenido = respuesta.text

    return (contenido, duracion)


async def enfoque_secuencial(temas: List[str]):
    print("\n--- 🐢 INICIANDO MODO SECUENCIAL (Lento) ---")
    inicio = time.perf_counter()
    resultados = []

    for tema in temas:
        print(f"⏳ [LLM] Pensando chiste sobre '{tema}'...")
        contenido, duracion = await consultar_openai(tema)
        print(f"✅ [LLM] Chiste sobre '{tema}' generado en {duracion:.2f}s.")
        resultados.append((tema, contenido, duracion))

    fin = time.perf_counter()
    print(f"--- 🐢 Tiempo Secuencial total: {fin - inicio:.2f} segundos ---\n")

    for tema, contenido, duracion in resultados:
        print(f"🐢 {tema} ({duracion:.2f}s): {contenido}\n")


async def enfoque_paralelo(temas: List[str]):
    print("\n--- 🚀 INICIANDO MODO PARALELO (Asyncio/Gather) ---")
    inicio = time.perf_counter()

    async def worker(tema: str):
        print(f"⏳ [LLM] Pensando chiste sobre '{tema}'...")
        contenido, duracion = await consultar_openai(tema)
        print(f"✅ [LLM] Chiste sobre '{tema}' generado en {duracion:.2f}s.")
        return (tema, contenido, duracion)

    tareas = [asyncio.create_task(worker(tema)) for tema in temas]
    resultados = await asyncio.gather(*tareas)

    fin = time.perf_counter()
    print(f"--- 🚀 Tiempo Paralelo total: {fin - inicio:.2f} segundos ---\n")

    for tema, contenido, duracion in resultados:
        print(f"🚀 {tema} ({duracion:.2f}s): {contenido}\n")


async def main():
    temas = ["Programador", "Gato", "IA"]

    await enfoque_secuencial(temas)

    # Pausa breve para hacer evidente el cambio de modalidad
    await asyncio.sleep(2)

    await enfoque_paralelo(temas)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
