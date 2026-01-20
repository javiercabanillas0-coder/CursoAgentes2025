"""
Módulo de Configuración.

Este módulo maneja la configuración para la aplicación de Investigación Profunda,
enfocándose principalmente en la configuración de correo electrónico y claves API.
Permite la configuración a través de variables de entorno o modificación directa de este archivo.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env si está presente
load_dotenv()

# --- Configuración de Correo Electrónico ---
# Las direcciones se pueden configurar mediante variables de entorno o codificarse aquí como respaldo.
# Se recomienda utilizar variables de entorno por seguridad y flexibilidad.

# La dirección de correo electrónico utilizada para enviar los informes (debe estar verificada en SendGrid)
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "juangabriel@frogames.es")

# La dirección de correo electrónico que recibirá los informes
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "juangabriel@frogames.es")


# --- Configuración de Claves API ---
# Las claves API suelen ser cargadas automáticamente por las librerías respectivas (OpenAI, SendGrid)
# desde las variables de entorno, pero recuperamos explícitamente la clave de SendGrid aquí para verificación o uso.

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

# --- Configuración de Búsqueda ---
# Definimos los límites y valores por defecto para la cantidad de fuentes a investigar.
DEFAULT_SEARCH_COUNT = 6
MIN_SEARCH_COUNT = 3
MAX_SEARCH_COUNT = 20
