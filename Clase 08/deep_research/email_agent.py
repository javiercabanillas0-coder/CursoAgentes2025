"""
Módulo del Agente de Correo Electrónico.

Este módulo define el Agente de Correo, el cual maneja el formato y la entrega
del informe final por correo electrónico utilizando SendGrid.
"""

import os
import config
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """
    Envía un correo electrónico con el asunto y cuerpo HTML proporcionados.

    Esta función utiliza la API de SendGrid para enviar correos electrónicos. 
    Los valores de configuración (clave API, remitente, destinatario) se recuperan 
    del entorno o del módulo de configuración.

    Args:
        subject (str): La línea de asunto del correo electrónico.
        html_body (str): El contenido HTML del correo electrónico.

    Returns:
        Dict[str, str]: Un diccionario de estado (ej. {"status": "success"}).
    """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    
    # Configurar remitente y destinatario desde config
    from_email = Email(config.EMAIL_SENDER) 
    to_email = To(config.EMAIL_RECIPIENT) 
    
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    
    try:
        # Enviar la solicitud de correo electrónico
        response = sg.client.mail.send.post(request_body=mail)
        print("Respuesta de correo electrónico", response.status_code)
        
        # Validar el código de estado (2xx es éxito)
        if 200 <= response.status_code < 300:
            return {"status": "success"}
        else:
            return {"status": "error", "message": f"SendGrid returned {response.status_code}"}
            
    except Exception as e:
        # Capturar errores de red o de la API de SendGrid
        print(f"Error crítico al enviar correo: {e}")
        return {"status": "error", "message": str(e)}


# Instrucciones para el Agente de Correo
INSTRUCTIONS = """Puedes enviar un correo electrónico con un cuerpo HTML bien formateado basado en un informe detallado.
Se te proporcionará un informe detallado. Debes usar tu herramienta para enviar un correo electrónico, proporcionando el 
informe convertido en un cuerpo HTML limpio, bien presentado con un asunto apropiado."""


# Inicializar el Agente de Correo
email_agent = Agent(
    name="Agente de correo electrónico",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
