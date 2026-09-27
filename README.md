# Enfocodeco · Estudio de agentes

Agentes que resuelven tareas de diseño y contenido de Enfocodeco a partir de un pedido en el chat de Claude Code.

## Cómo se usa

Abrí una sesión de Claude Code sobre este repositorio y pedí, por ejemplo:

- *"Armá el lifestyle de este producto en un baño minimalista, y al costado del espejo poné los apliques que te adjunto."*
- *"Quitale el fondo a estas 10 fotos y prepará las versiones para la tienda."*
- *"Escribí el caption para esta foto y 3 ideas de reels para la semana."*

El agente correspondiente hace todo el proceso y te avisa cuando está listo.

| Agente | Qué hace | Usa |
|---|---|---|
| **lifestyle** | Ambientaciones con tus productos | rembg + Gemini + revisión de Claude |
| **fondo-logo** | Recortes, logo y formatos | rembg + Pillow |
| **posts** | Captions, calendario, descripciones | Claude |

## Estructura

```
marca/        marca.md (resumen del manual), logos/, referencias/ (fotos de estilo)
productos/    catálogo: una carpeta por producto
scripts/      quitar_fondo.py · escena.py · terminar.py
salidas/      resultados, una carpeta por pedido
.claude/      skills (agentes) y hook que instala dependencias al iniciar la sesión
```

## Puesta en marcha

1. **Clave de Gemini:** crear en Google AI Studio y agregarla como variable de entorno `GEMINI_API_KEY`
   en la configuración del entorno de Claude Code (nunca en el repositorio).
2. **Marca:** completar `marca/marca.md` con el manual y subir `marca/logos/logo.png` (fondo transparente).
3. **Productos:** subir fotos a `productos/<nombre-del-producto>/`.
4. **Opcional:** habilitar `enfocodeco.com.ar` en el acceso de red del entorno para que los agentes lean el catálogo.

Uso local: `pip install -r requirements.txt`.
