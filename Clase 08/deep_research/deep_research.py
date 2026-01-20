"""
Punto de Entrada de la Aplicación de Investigación Profunda.

Este módulo inicializa la interfaz Gradio para la aplicación de Investigación Profunda (Deep Research).
Sirve como punto de entrada principal para que los usuarios interactúen con los agentes de investigación.

Uso:
    Ejecute el script para lanzar la interfaz web:
    $ python deep_research.py
"""

import gradio as gr
from dotenv import load_dotenv
import config

# Importaciones internas
from research_manager import ResearchManager

# Cargar variables de entorno desde el archivo .env
load_dotenv(override=True)


async def run(query: str, num_searches: float):
    """
    Ejecuta el proceso de investigación para una consulta dada.

    Esta función generadora asíncrona actúa como puente entre la interfaz de usuario de Gradio
    y el ResearchManager. Emite (yield) actualizaciones de estado y el informe final
    fragmento por fragmento.

    Args:
        query (str): El tema o pregunta de investigación proporcionada por el usuario.
        num_searches (float): El número de fuentes a buscar (Gradio pasa float para sliders numéricos).

    Yields:
        str: Actualizaciones de estado y el informe final en markdown.
    """
    # Inicializar y ejecutar el Gestor de Investigación (Research Manager)
    try:
        # Convertir a int porque ResearchManager espera un entero
        async for chunk in ResearchManager().run(query, int(num_searches)):
            yield chunk
    except Exception as e:
        # Capturar cualquier error no controlado que suba hasta la UI
        error_message = f"❌ **Ocurrió un error inesperado:**\n\n```\n{str(e)}\n```\nPor favor intenta de nuevo o revisa tu conexión."
        yield error_message


# Inicializar la Interfaz de Gradio
# Usamos un contexto Blocks para definir el diseño de la aplicación web.
with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Búsqueda Profunda")
    
    # Sección de entrada
    query_textbox = gr.Textbox(label="¿Sobre qué tema te gustaría investigar?")
    
    # Control deslizante para la cantidad de fuentes
    # Permite al usuario seleccionar entre MIN y MAX fuentes, con el valor por defecto configurado.
    search_count_slider = gr.Slider(
        minimum=config.MIN_SEARCH_COUNT,
        maximum=config.MAX_SEARCH_COUNT,
        value=config.DEFAULT_SEARCH_COUNT,
        step=1,
        label="Cantidad de fuentes (Búsquedas Web)",
        info="Selecciona cuántas búsquedas independientes realizar para recopilar información."
    )
    
    # Sección de control
    run_button = gr.Button("Ejecutar", variant="primary")
    
    # Sección de salida
    report = gr.Markdown(label="Informe")
    
    # Oyentes de eventos (Event listeners)
    # Activar la función run al hacer clic en el botón o enviar texto
    # Ahora pasamos ambos inputs: el texto y el valor del slider
    run_button.click(fn=run, inputs=[query_textbox, search_count_slider], outputs=report)
    query_textbox.submit(fn=run, inputs=[query_textbox, search_count_slider], outputs=report)

# Lanzar la aplicación
if __name__ == "__main__":
    ui.launch(inbrowser=True)
