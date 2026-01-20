"""
Módulo del Agente Planificador.

Este módulo define el Agente Planificador, el cual es responsable de descomponer
una consulta de investigación de alto nivel en un conjunto específico de consultas de búsqueda web.
"""

from pydantic import BaseModel, Field
from agents import Agent


# Instrucciones para el Agente Planificador
# Nota: La cantidad de búsquedas se inyectará dinámicamente en el prompt, 
# por lo que estas instrucciones son generales.
INSTRUCTIONS = "Eres un asistente de investigación útil. Dado un término de búsqueda y una cantidad objetivo, \
produce un conjunto de búsquedas web para realizar para responder la consulta. \
Salida: el número solicitado de términos para consultar."


class WebSearchItem(BaseModel):
    """
    Representa una única consulta de búsqueda web.

    Atributos:
        reason (str): La justificación de por qué esta búsqueda es relevante.
        query (str): La cadena de búsqueda real que se enviará.
    """
    reason: str = Field(description="Tu razonamiento de por qué esta búsqueda es importante para la consulta.")
    query: str = Field(description="El término de búsqueda a usar para la búsqueda web.")


class WebSearchPlan(BaseModel):
    """
    Representa el plan de búsqueda general que contiene múltiples elementos de búsqueda.

    Atributos:
        searches (list[WebSearchItem]): Una lista de búsquedas planificadas.
    """
    searches: list[WebSearchItem] = Field(description="Una lista de búsquedas web a realizar para responder la consulta.")


# Inicializar el Agente Planificador
planner_agent = Agent(
    name="Agente de planificación",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)