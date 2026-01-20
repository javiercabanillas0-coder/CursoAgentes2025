"""
Módulo del Agente Escritor.

Este módulo define el Agente Escritor, el cual sintetiza la información recopilada
de múltiples búsquedas en un informe markdown completo.
"""

from pydantic import BaseModel, Field
from agents import Agent


# Instrucciones para el Agente Escritor
# Especifica el rol, el formato de entrada y la estructura de salida esperada (markdown largo y detallado).
INSTRUCTIONS = (
    "Eres un investigador senior encargado de escribir un informe coherente para una consulta de investigación. "
    "Se te proporcionará la consulta original, y algunas investigaciones iniciales realizadas por un asistente de investigación.\n"
    "Primero, debes elaborar un esquema para el informe que describa la estructura y "
    "flujo del informe. Luego, genera el informe y devuelve ese como tu salida final.\n"
    "La salida final debe estar en formato markdown, y debe ser larga y detallada. Asegúrate de "
    "tener 5-10 páginas de contenido, al menos 1000 palabras."
)


class ReportData(BaseModel):
    """
    Representa la estructura del informe de salida final.

    Atributos:
        short_summary (str): Un resumen conciso de 2-3 oraciones de los hallazgos.
        markdown_report (str): El informe detallado completo en formato Markdown.
        follow_up_questions (list[str]): Preguntas sugeridas para investigar más.
    """
    short_summary: str = Field(description="Un resumen de 2-3 oraciones de los hallazgos.")

    markdown_report: str = Field(description="El informe final")

    follow_up_questions: list[str] = Field(description="Temas sugeridos para investigar más")


# Inicializar el Agente Escritor
writer_agent = Agent(
    name="Agente de escritura",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)
