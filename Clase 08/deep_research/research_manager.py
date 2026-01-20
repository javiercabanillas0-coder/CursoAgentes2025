"""
Módulo del Gestor de Investigación (Research Manager).

Este módulo define la clase `ResearchManager`, que orquesta todo el proceso
de investigación. Coordina entre los diferentes agentes (Planificador, Búsqueda,
Escritor, Correo) para satisfacer la consulta de investigación del usuario.
"""

from agents import Runner, trace, gen_trace_id
import asyncio
import config

# Importaciones de agentes
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent


class ResearchManager:
    """
    Gestiona el ciclo de vida de una tarea de investigación profunda.

    Esta clase coordina la planificación, ejecución, síntesis y entrega
    de un informe de investigación basado en la consulta de un usuario.

    Métodos:
        run(query): Punto de entrada principal para iniciar la investigación.
        plan_searches(query): Utiliza el Agente Planificador para generar una estrategia de búsqueda.
        perform_searches(search_plan): Ejecuta las búsquedas planificadas en paralelo.
        search(item): Ejecuta una única consulta de búsqueda utilizando el Agente de Búsqueda.
        write_report(query, search_results): Utiliza el Agente Escritor para compilar el informe.
        send_email(report): Utiliza el Agente de Correo para entregar el informe.
    """

    async def run(self, query: str, num_searches: int = config.DEFAULT_SEARCH_COUNT):
        """
        Ejecuta el proceso de investigación profunda, emitiendo actualizaciones de estado.

        Este método ejecuta el flujo de trabajo de investigación de forma secuencial:
        1. Inicialización de trazado (trace).
        2. Planificación de búsquedas.
        3. Realización de búsquedas.
        4. Redacción del informe.
        5. Envío del correo electrónico.

        Args:
            query (str): El tema de investigación proporcionado por el usuario.
            num_searches (int): Cantidad de búsquedas a realizar.

        Yields:
            str: Mensajes de estado y finalmente el contenido del informe en markdown.
        """
        trace_id = gen_trace_id()
        
        # Iniciar una traza para observabilidad (ej. en el panel de OpenAI)
        with trace("Ingestigación", trace_id=trace_id):
            print(f"Ver traza: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"Ver traza: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            
            print(f"Iniciando investigación con {num_searches} fuentes...")
            
            # Paso 1: Planificar
            search_plan = await self.plan_searches(query, num_searches)
            yield "Búsquedas planificadas, iniciando búsqueda..."     
            
            # Paso 2: Buscar
            search_results = await self.perform_searches(search_plan)
            yield "Búsquedas completas, escribiendo informe..."
            
            # Paso 3: Escribir
            report = await self.write_report(query, search_results)
            yield "Informe escrito, enviando correo electrónico..."
            
            # Paso 4: Entregar
            await self.send_email(report)
            yield "Correo electrónico enviado, investigación completa"
            
            # Salida Final
            yield report.markdown_report
        

    async def plan_searches(self, query: str, num_searches: int) -> WebSearchPlan:
        """
        Genera un plan de búsquedas web para la consulta dada.

        Args:
            query (str): El tema de investigación.
            num_searches (int): Cantidad de búsquedas a generar.

        Returns:
            WebSearchPlan: Un plan estructurado que contiene consultas de búsqueda y razones.
        """
        print(f"Planificando {num_searches} búsquedas...")
        try:
            result = await Runner.run(
                planner_agent,
                f"Consulta: {query}\nGenera {num_searches} búsquedas.",
            )
        except Exception as e:
            # Manejo de errores en caso de fallo del agente planificador
            print(f"Error al planificar búsquedas: {e}")
            # Retornar un plan vacío o predeterminado para no romper el flujo
            return WebSearchPlan(searches=[])

        print(f"Se realizarán {len(result.final_output.searches)} búsquedas")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """
        Ejecuta todas las búsquedas definidas en el plan de forma concurrente.

        Args:
            search_plan (WebSearchPlan): El plan que contiene los elementos de búsqueda.

        Returns:
            list[str]: Una lista de resúmenes de búsqueda devueltos por el Agente de Búsqueda.
        """
        print("Buscando...")
        num_completed = 0
        
        # Crear tareas asíncronas para todos los elementos de búsqueda
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        
        # Procesar tareas a medida que se completan
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Buscando... {num_completed}/{len(tasks)} completadas")
            
        print("Búsqueda completada")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """
        Realiza una única búsqueda web utilizando el Agente de Búsqueda.

        Args:
            item (WebSearchItem): El elemento de búsqueda específico que contiene la consulta y la razón.

        Returns:
            str | None: El resumen del resultado de la búsqueda, o None si falló.
        """
        input_text = f"Término de búsqueda: {item.query}\nRazón para buscar: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input_text,
            )
            return str(result.final_output)
        except Exception:
            # Manejar silenciosamente los fallos para búsquedas individuales para evitar bloquear todo el proceso
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """
        Compila los resultados de búsqueda en un informe final utilizando el Agente Escritor.

        Args:
            query (str): La consulta de investigación original.
            search_results (list[str]): Los resúmenes recopilados de las búsquedas web.

        Returns:
            ReportData: El informe estructurado que contiene el contenido en markdown.
        """
        print("Pensando en el informe...")
        input_text = f"Consulta original: {query}\nResultados de búsqueda resumidos: {search_results}"
        
        try:
            result = await Runner.run(
                writer_agent,
                input_text,
            )
            print("Informe escrito")
            return result.final_output_as(ReportData)
        except Exception as e:
            # Manejo de errores al escribir el informe
            print(f"Error al escribir el informe: {e}")
            # Retornar un informe de error básico
            return ReportData(
                short_summary="Hubo un error al generar el informe.",
                markdown_report=f"# Error de Generación\n\nNo se pudo generar el informe debido a un error: {str(e)}",
                follow_up_questions=[]
            )
    
    async def send_email(self, report: ReportData) -> None:
        """
        Envía el informe generado por correo electrónico utilizando el Agente de Correo.

        Args:
            report (ReportData): Los datos del informe que contienen el informe en markdown.
        """
        print("Escribiendo correo electrónico...")
        try:
            result = await Runner.run(
                email_agent,
                report.markdown_report,
            )
            print("Correo electrónico enviado")
        except Exception as e:
            # Manejo de errores al enviar el correo
            print(f"Error al enviar el correo electrónico: {e}")
        
        return report