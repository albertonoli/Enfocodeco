#!/usr/bin/env python3
"""Genera una escena de lifestyle con Gemini a partir de fotos de referencia.

Requiere la variable de entorno GEMINI_API_KEY.

Uso:
    python scripts/escena.py --prompt "..." --ref aplique_recorte.png --ref espejo.jpg \
        --formato 4:5 --salida salidas/2026-09-27_bano/escena.png --variantes 2
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image

MODELO_POR_DEFECTO = "gemini-2.5-flash-image"
FORMATOS = {"1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    texto = parser.add_mutually_exclusive_group(required=True)
    texto.add_argument("--prompt", help="Instrucción de la escena")
    texto.add_argument("--prompt-archivo", help="Archivo de texto con la instrucción")
    parser.add_argument("--ref", action="append", default=[], help="Imagen de referencia (repetible)")
    parser.add_argument("--formato", default="4:5", choices=sorted(FORMATOS), help="Relación de aspecto")
    parser.add_argument("--salida", required=True, help="Ruta del PNG de salida")
    parser.add_argument("--variantes", type=int, default=1, help="Cuántas versiones generar")
    parser.add_argument("--modelo", default=os.environ.get("GEMINI_IMAGE_MODEL", MODELO_POR_DEFECTO))
    args = parser.parse_args()

    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("Falta GEMINI_API_KEY. Agregala como variable de entorno en la configuración del entorno.")

    from google import genai
    from google.genai import types

    prompt = args.prompt or Path(args.prompt_archivo).read_text(encoding="utf-8")
    referencias = [Image.open(r) for r in args.ref]

    cliente = genai.Client()
    config = types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
        image_config=types.ImageConfig(aspect_ratio=args.formato),
    )

    salida = Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    generadas = []
    for i in range(1, args.variantes + 1):
        respuesta = cliente.models.generate_content(
            model=args.modelo, contents=[prompt, *referencias], config=config)
        partes = (respuesta.candidates[0].content.parts
                  if respuesta.candidates and respuesta.candidates[0].content else [])
        imagen = next((p.inline_data.data for p in partes if p.inline_data), None)
        if imagen is None:
            comentario = " ".join(p.text for p in partes if p.text) or "sin detalle"
            print(f"⚠️  Variante {i}: Gemini no devolvió imagen ({comentario})", file=sys.stderr)
            continue
        destino = salida if args.variantes == 1 else salida.with_stem(f"{salida.stem}_v{i}")
        destino.write_bytes(imagen)
        generadas.append(destino)
        print(destino)

    # Registro para poder repetir o ajustar la escena más adelante.
    registro = salida.with_suffix(".json")
    registro.write_text(json.dumps({
        "fecha": datetime.now().isoformat(timespec="seconds"),
        "modelo": args.modelo,
        "formato": args.formato,
        "prompt": prompt,
        "referencias": args.ref,
        "resultados": [str(g) for g in generadas],
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    if not generadas:
        sys.exit("No se generó ninguna imagen.")


if __name__ == "__main__":
    main()
