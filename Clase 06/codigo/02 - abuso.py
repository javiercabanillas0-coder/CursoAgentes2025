# El problema: Ejecución Secuencial (Lenta)
# Si usamos await uno detrás de otro, el código sigue siendo secuencial (lento), aunque sea asíncrono.

import asyncio
import time

async def cocinar_plato(nombre, tiempo):
    print(f"Empezando {nombre}...")
    await asyncio.sleep(tiempo)
    print(f"Terminado {nombre}!")
    return nombre

async def main():
    inicio = time.time()
    
    # Esto es secuencial: espera a que termine uno para empezar el otro
    await cocinar_plato("Pizza", 2)
    await cocinar_plato("Pasta", 2)
  
    
    fin = time.time()
    print(f"Tiempo total: {fin - inicio:.2f} segundos")

asyncio.run(main())

# Resultado esperado: ~4 segundos (2 + 2)