# Enfocodeco — asistentes de diseño y contenido

Enfocodeco vende artículos de iluminación decorativa (enfocodeco.com.ar, Instagram @enfocodeco).
Este repositorio es el "estudio" de agentes: el dueño dispara pedidos desde el chat y los agentes
los resuelven de punta a punta.

## Agentes (skills en `.claude/skills/`)
- `lifestyle` — fotos de ambientación con productos (recorte → Gemini → control de calidad → logo → entrega).
- `fondo-logo` — quitar fondos, poner logo, exportar formatos (sin IA generativa).
- `posts` — captions, calendario y descripciones de tienda con la voz de la marca.

## Reglas generales
- Respondé en español rioplatense, breve y concreto.
- Leé siempre `marca/marca.md` antes de producir algo visual o de texto. No inventes datos marcados `[COMPLETAR]`.
- Los productos deben verse **idénticos** a las fotos reales: es lo que se vende.
- Todo lo generado va a `salidas/AAAA-MM-DD_<tema>/`; al terminar: SendUserFile con los finales,
  notificación push, commit y push a la rama de trabajo.
- No pidas claves por chat. `GEMINI_API_KEY` se configura como variable de entorno del entorno.

## Scripts (`scripts/`, Python; dependencias en `requirements.txt`)
- `quitar_fondo.py <fotos|carpeta> --salida DIR [--modelo birefnet-general]`
- `escena.py --prompt-archivo P --ref IMG [--ref IMG] --formato 4:5 --variantes N --salida OUT.png`
  (modelo por defecto `gemini-2.5-flash-image`; se cambia con `GEMINI_IMAGE_MODEL`)
- `terminar.py IMG --formatos feed,story,web,cuadrado,banner,original [--modo encajar --fondo HEX] [--sin-logo]`
