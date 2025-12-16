import asyncio
import time
import random

# --- 1. Simulamos al LLM (El "Backend" lento) ---
async def llamar_llm_falso(tema):
    print(f"⏳ [LLM] Pensando chiste sobre '{tema}'...")
    
    # Simulamos la latencia de red y procesamiento (2 segundos)
    # En la vida real, aquí iría: await openai.chat.completions.create(...)
    await asyncio.sleep(2) 
    
    print(f"✅ [LLM] Chiste sobre '{tema}' generado.")
    return f"¿Por qué el {tema} cruzó la calle? ¡Para llegar al otro lado!"

# --- 2. Enfoque Lento (Secuencial / "Uno por uno") ---
async def enfoque_secuencial(temas):
    print("\n--- 🐢 INICIANDO MODO SECUENCIAL (Lento) ---")
    inicio = time.perf_counter()
    
    resultados = []
    for tema in temas:
        # EL ERROR COMÚN: Poner 'await' dentro del bucle for
        # Esto detiene el programa hasta que este chiste termine antes de pedir el siguiente.
        chiste = await llamar_llm_falso(tema)
        resultados.append(chiste)
        
    fin = time.perf_counter()
    print(f"--- 🐢 Tiempo Secuencial: {fin - inicio:.2f} segundos ---")
    return resultados

# --- 3. Enfoque Rápido (Concurrente / "En Paralelo") ---
async def enfoque_paralelo(temas):
    print("\n--- 🚀 INICIANDO MODO PARALELO (Asyncio/Gather) ---")
    inicio = time.perf_counter()
    
    # LA FORMA CORRECTA: Crear tareas sin esperarlas inmediatamente
    tareas = [llamar_llm_falso(tema) for tema in temas]
    
    # Lanzamos todas las peticiones a la vez y esperamos que vuelvan todas
    resultados = await asyncio.gather(*tareas)
    
    fin = time.perf_counter()
    print(f"--- 🚀 Tiempo Paralelo: {fin - inicio:.2f} segundos ---")
    return resultados

# --- Ejecución Principal ---
async def main():
    temas = ["Programador", "Gato", "IA"]
    
    # 1. Probamos el modo lento
    await enfoque_secuencial(temas)
    
    # Pequeña pausa dramática
    await asyncio.sleep(2)
    
    # 2. Probamos el modo rápido
    await enfoque_paralelo(temas)

if __name__ == "__main__":
    asyncio.run(main())