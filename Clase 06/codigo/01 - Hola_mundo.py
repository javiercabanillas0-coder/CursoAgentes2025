import asyncio

# Definimos una corrutina
async def saludar():
    print("Hola...")
    # Simulamos una espera de 2 segundo (ej. esperando a una base de datos)
    await asyncio.sleep(2) 
    print("...Mundo!")

# Punto de entrada principal
if __name__ == "__main__":
    asyncio.run(saludar())
    
# NOTA IMPORTANTE:Nunca uses time.sleep() dentro de una función async. 
# time.sleep() bloquea todo el programa. asyncio.sleep() solo pausa esa tarea específica.     
    