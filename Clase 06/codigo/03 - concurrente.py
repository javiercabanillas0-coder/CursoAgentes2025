# La solución: Ejecución Concurrente (asyncio.gather)
# Aquí es donde ocurre la magia. Usamos asyncio.gather para lanzar múltiples tareas 
# al Event Loop al mismo tiempo.

import asyncio
import time

async def cocinar_plato(nombre, tiempo):
    print(f"🍳 Empezando {nombre}...")
    await asyncio.sleep(tiempo)
    print(f"✅ Terminado {nombre}!")
    return f"{nombre} listo"

async def main():
    inicio = time.time()
    
    print("----- Iniciando Cocina -----")
    
    # Programamos las tres tareas para correr "a la vez"
    # El loop saltará entre ellas cuando encuentre un 'await'
    resultados = await asyncio.gather(
        cocinar_plato("Pizza", 2),
        cocinar_plato("Pasta", 2),
        cocinar_plato("Ensalada", 1)
    )
    
    fin = time.time()
    print("----- Cocina Cerrada -----")
    print(f"Resultados: {resultados}")
    print(f"Tiempo total: {fin - inicio:.2f} segundos")

if __name__ == "__main__":
    asyncio.run(main())

# Resultado esperado: ~2 segundos (El tiempo de la tarea más larga)