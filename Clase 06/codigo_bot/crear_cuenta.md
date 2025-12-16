## Y ahora, la implementación

Este código está en `app.py`

La implementación se realizará en HuggingFace Spaces. 

Antes de empezar: recuerda actualizar los archivos del directorio "doc" (tu perfil de LinkedIn y resumen.txt) para que se muestren tus credenciales.

Comprueba también que no haya ningún archivo README en el directorio. Si lo hay, elimínalo. El proceso de implementación crea un nuevo archivo README en este directorio.

1. Visita https://huggingface.co y crea una cuenta.
2. En el menú Avatar, en la esquina superior derecha, selecciona "Tokens de acceso". Selecciona "Crear nuevo token". Asígnale permisos de escritura.
3. Tome este token y agréguelo a su archivo .env: `HF_TOKEN=hf_xxx`. Si no se detecta durante la implementación, consulte la nota a continuación.
4. Desde la carpeta, introduzca `dotenv gradio deploy`. Si por alguna razón aún le solicita que introduzca su token HF, interrúmpalo con Ctrl+C y ejecute y revisa que tengas cargada en el .env el token correctamnte
5. Siga sus instrucciones: asígnele el nombre "BotPersonal", especifique app.py, elija cpu-basic como hardware, confirme que es necesario proporcionar secretos, proporcione su clave de API de OpenAI, su usuario y token de Pushover, y confirme que no se permiten las acciones de GitHub. 
Si no subes los secrets en este momento luego los puedes cargar a mano en la web   
6. Cuando termine el proceso te dira que Space available at https://huggingface.co/spaces/...
7. 
#### Más información sobre estos secretos:

Si no entiendes qué sucede con estos secretos, solo te pide que introduzcas el nombre y el valor de la clave para cada uno de ellos. Por ejemplo, escribirías:
`OPENAI_API_KEY`
Seguido de:
`sk-proj-...`

Si no quieres configurar los secretos de esta manera o si algo sale mal, no hay problema: puedes cambiarlos más tarde:

1. Inicia sesión en el sitio web de HuggingFace.
2. Ve a tu perfil a través del menú "Avatar" en la esquina superior derecha.
3. Selecciona el espacio que has implementado.
4. Haz clic en la rueda de Ajustes en la esquina superior derecha.
5. Puedes desplazarte hacia abajo para cambiar tus secretos, eliminar el espacio, etc.

#### ¡Y ya deberías estar implementado!

Aquí está el mío: https://huggingface.co/spaces/ofazzito/Botpersonal

Para más información sobre la implementación:

https://www.gradio.app/guides/sharing-your-app#hosting-on-hf-spaces

Para eliminar tu espacio en el futuro:

1. Inicia sesión en HuggingFace.
2. En el menú Avatar, selecciona tu perfil.
3. Haz clic en el espacio y selecciona la rueda de configuración en la esquina superior derecha.
4. Desplázate hasta la sección Eliminar en la parte inferior.
5. ADEMÁS: borra el archivo README que Gradio haya creado dentro de la carpeta 1_foundations (de lo contrario, no te hará las preguntas la próxima vez que implementes Gradio).