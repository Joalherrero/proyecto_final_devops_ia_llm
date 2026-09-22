# Proyecto final: diagnóstico local de incidentes Django

Este laboratorio convierte las prácticas de `pta-ai-devops/finetuning/` en una aplicación que puedes estudiar de principio a fin. Django genera o registra incidentes, un servicio FastAPI los clasifica y Ollama puede explicar el resultado con un modelo local. Todo está definido para **Podman Compose**, pero **no he construido imágenes ni arrancado contenedores**.

Lee primero el [diagrama de arquitectura](docs/arquitectura.md).

## Qué hay en este directorio

```text
proyecto_final_devops_ia_llm/
├── README.md                    Esta guía
├── docs/arquitectura.md         Diagrama y recorrido de datos
├── compose.yaml                 Tres servicios, red interna y volúmenes
├── .env.example                 Variables locales de ejemplo
├── django_app/                  Web de incidentes y diagnósticos
│   ├── Containerfile
│   ├── requirements.txt
│   ├── config/                 Configuración Django
│   └── incidents/              Modelos, vistas y plantilla HTML
├── triage_service/              API FastAPI de diagnóstico
│   ├── Containerfile
│   ├── requirements.txt
│   ├── main.py
│   └── triage_core/             Copia del baseline del curso
└── runbooks/                   Consejos locales por categoría
```

La copia de `triage_core/` procede de `../pta-ai-devops/finetuning/triage_core/` para que el contexto de construcción de la imagen no incluya todo el repositorio. Si mejoras las reglas, decide conscientemente si sincronizar ambas versiones. **No se copia `apuntes.md` ni ninguna clave a las imágenes.**

## Requisitos

- Podman y un proveedor Compose (`podman-compose` está instalado en este ordenador).
- En macOS, una `podman machine` creada y arrancada desde tu terminal. Podman usa una VM Linux en este sistema ([documentación](https://docs.podman.io/en/latest/markdown/podman-machine-start.1.html)).
- Conexión a Internet para descargar las imágenes y, si usas Ollama, el modelo. La clasificación por reglas no llama a ningún proveedor de IA.
- Memoria suficiente para el modelo que elijas; empieza con uno pequeño y ajusta la memoria de Podman machine según tu equipo.

## Cómo arrancarlo **cuando decidas hacerlo**

Estas son instrucciones para ti; no se han ejecutado en esta tarea.

```bash
cd proyecto_final_devops_ia_llm
podman machine list
# Si no existe: podman machine init --now
# Si existe y está parada: podman machine start
cp .env.example .env
# Cambia DJANGO_SECRET_KEY en .env por una cadena aleatoria local.
podman-compose -f compose.yaml build
podman-compose -f compose.yaml up -d
podman-compose -f compose.yaml ps
```

Abre `http://127.0.0.1:8000`. Pulsa **Crear fallo de importación de prueba** y después **Diagnosticar con reglas**. El resultado quedará en SQLite, dentro del volumen `django_data`. Para ver la petición y los errores:

```bash
podman-compose -f compose.yaml logs django
podman-compose -f compose.yaml logs triage
```

La API triage no se publica en el host. Desde su propio contenedor puedes consultar salud:

```bash
podman-compose -f compose.yaml exec triage python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8001/health').read().decode())"
```

### Activar la explicación de Ollama

El servicio Ollama estará creado al levantar Compose, pero el volumen empieza sin modelos. Descarga el modelo indicado en `.env` y espera a que termine:

```bash
podman-compose -f compose.yaml exec ollama ollama pull llama3.2:3b
```

Después pulsa **Explicar con Ollama** en Django. Si cambias `OLLAMA_MODEL`, descarga ese modelo y recrea `triage` para que lea la variable nueva. Esta versión usa el modelo para redactar la causa, pero conserva categoría y gravedad del baseline por reglas; aún no implementa selección autónoma de herramientas.

Para parar los servicios sin borrar los datos:

```bash
podman-compose -f compose.yaml down
```

## Qué aprenderás al recorrer el código

1. **Django:** `incidents/models.py` define un incidente y sus diagnósticos; `views.py` crea el fallo de prueba, redacta valores sensibles y hace la llamada HTTP. La plantilla muestra ambos resultados.
2. **Contenedores:** `compose.yaml` conecta servicios por nombre. Solo publica Django en `127.0.0.1`; SQLite y el modelo sobreviven en volúmenes.
3. **Baseline:** `triage_service/triage_core/rules.py` aplica reglas del curso. Cambia una regla y verifica qué ejemplos mejoran o empeoran.
4. **Contexto:** `triage_service/main.py` lee un runbook para la categoría detectada. Añade un runbook para otra categoría y observa cómo cambia la evidencia.
5. **LLM local:** el modo `ollama` envía log, categoría y runbook al modelo. Compara su explicación con el resultado por reglas y anota errores.
6. **Siguiente práctica:** convierte la lectura de runbooks en una herramienta elegida por un agente, añade evaluación de casos reservados y solo entonces considera LoRA.

## Límites conocidos

- La redacción de secretos en `incidents/views.py` es **básica**; usa solo logs ficticios o previamente revisados. No envíes incidentes reales con credenciales.
- El modo Ollama puede tardar o devolver `503` si el modelo no se ha descargado o no está listo. El modo de reglas sigue disponible.
- La vista hace la petición de diagnóstico de forma síncrona. Para una aplicación con tráfico real, moverías este trabajo a una cola y añadirías autenticación, límites y monitorización.
- Esta primera versión **no es todavía un agente** ni incluye fine tuning. Separa intencionadamente baseline, explicación y futuro agente para poder medir qué aporta cada pieza.
- No se han ejecutado pruebas de integración con contenedores; la definición de Compose y los módulos Python se pueden validar sin arrancarlos.

## Fuentes oficiales

- [Podman Compose](https://docs.podman.io/en/latest/markdown/podman-compose.1.html).
- [Logging en Django](https://docs.djangoproject.com/en/5.2/topics/logging/).
