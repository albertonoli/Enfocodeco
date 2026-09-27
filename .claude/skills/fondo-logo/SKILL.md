---
name: fondo-logo
description: Recorta fondos de fotos de producto de Enfocodeco, pone el logo y exporta en formatos para Instagram y la tienda. Usar para "quitale el fondo", "poné el logo", "pasá estas fotos a formato story/feed", "prepará las fotos para la tienda", "fondo blanco", procesamiento en lote de fotos de catálogo.
---

# Agente Fondo y Logo — Enfocodeco

Tareas rápidas y repetibles sobre fotos. No usa IA generativa: el resultado es siempre consistente.

## Flujo

1. Ubicá las fotos (adjuntos o `productos/`). Carpeta de trabajo: `salidas/AAAA-MM-DD_<tema>/`.
2. **Quitar fondo** (si se pidió o si el destino es ficha de tienda):
   `python scripts/quitar_fondo.py <fotos o carpeta> --salida salidas/<carpeta>/recortes`
   Revisá los recortes con Read; en piezas finas o translúcidas probá `--modelo birefnet-general`.
3. **Formatos + logo**:
   - Ficha de tienda (producto sobre fondo liso, sin logo):
     `python scripts/terminar.py <recorte.png> --modo encajar --fondo "<color de marca/marca.md o #FFFFFF>" --formatos web --sin-logo`
   - Redes con logo:
     `python scripts/terminar.py <imagen> --formatos feed,story [--posicion abajo-izquierda]`
   Para varias fotos, repetí el comando por cada archivo.
   Si falta `marca/logos/logo.png`, avisá y seguí con `--sin-logo`.
4. **Entregar**: SendUserFile con los finales, notificación push si fue un lote grande,
   commit + push de `salidas/<carpeta>/`, y un resumen de una o dos líneas.
