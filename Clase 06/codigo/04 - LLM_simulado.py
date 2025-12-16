import asyncio
import random

# Ejemplo de concurrencia con asyncio para simular consultas a diferentes LLMs.
# Muestra dos formas de recolectar resultados:
# - `asyncio.gather`: devuelve respuestas en el mismo orden de las tareas enviadas.
# - `asyncio.as_completed`: permite procesar respuestas conforme llegan (orden de llegada).
#
# Nota:
# - Para dejar claro el concepto, imprimimos los mensajes "Consultando..." en el
#   mismo orden de envío antes de lanzar las tareas. De ese modo, lo que cambia
#   entre métodos es únicamente el orden de las respuestas, no el orden de envío.
#   Pero la realidad es que las consultas se envían "a la vez" y las respuestas llegan en orden
#   aleatorio según la latencia simulada.


async def consultar_llm(modelo):
    """Simula la consulta a un LLM con latencia aleatoria.

    No imprime "Consultando...": ese mensaje se muestra antes de lanzar las tareas
    para que el orden de envío sea siempre evidente.
    """
    tiempo_espera = random.uniform(1, 8)  # Simula latencia de red
    await asyncio.sleep(tiempo_espera)
    return f"Respuesta de {modelo} en {tiempo_espera:.2f}s"


async def main():
    modelos = ["GPT-4", "Claude 3.5", "Llama 3"]

    # Imprime los mensajes de consulta en el orden de envío (siempre el mismo)
    for modelo in modelos:
        print(f"🤖 Consultando {modelo}...")

    # --- Método 1: Usando asyncio.gather ---
    # Ejecuta todas las tareas y espera a que todas terminen.
    # Las respuestas se imprimen en el mismo orden que los modelos originales.
    print("\nMétodo 1: Respuestas en orden de modelos (asyncio.gather)")
    tareas_gather = [consultar_llm(m) for m in modelos]
    respuestas_gather = await asyncio.gather(*tareas_gather)
    for r in respuestas_gather:
        print(r)

    # --- Método 2: Usando asyncio.as_completed ---
    # Procesa cada tarea conforme termina, mostrando el orden real de llegada.
    print("\nMétodo 2: Respuestas en orden de llegada (asyncio.as_completed)")
    tareas_completed = [consultar_llm(m) for m in modelos]
    for tarea in asyncio.as_completed(tareas_completed):
        respuesta = await tarea
        print(respuesta)


if __name__ == "__main__":
    asyncio.run(main())