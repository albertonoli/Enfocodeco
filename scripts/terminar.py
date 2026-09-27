#!/usr/bin/env python3
"""Pone el logo de Enfocodeco y exporta la imagen en los formatos de cada canal.

Uso:
    python scripts/terminar.py salidas/2026-09-27_bano/escena.png
    python scripts/terminar.py foto.png --formatos feed,story --posicion abajo-izquierda
    python scripts/terminar.py foto.png --sin-logo --modo encajar --fondo "#F4F1EC"
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
LOGO_POR_DEFECTO = RAIZ / "marca" / "logos" / "logo.png"

FORMATOS = {
    "feed": (1080, 1350),      # Instagram feed 4:5
    "story": (1080, 1920),     # Stories / Reels 9:16
    "cuadrado": (1080, 1080),  # 1:1
    "web": (1600, 1600),       # Ficha de producto en la tienda
    "banner": (1920, 800),     # Banner de portada web
}
POSICIONES = {"abajo-derecha", "abajo-izquierda", "arriba-derecha", "arriba-izquierda", "abajo-centro"}


def ajustar(imagen, tamano, modo, fondo, aire):
    if modo == "recortar":
        return ImageOps.fit(imagen, tamano, Image.LANCZOS, centering=(0.5, 0.5))
    lienzo = Image.new("RGBA", tamano, fondo)
    libre = int(min(tamano) * aire)
    copia = ImageOps.contain(imagen, (tamano[0] - 2 * libre, tamano[1] - 2 * libre), Image.LANCZOS)
    lienzo.paste(copia, ((tamano[0] - copia.width) // 2, (tamano[1] - copia.height) // 2), copia)
    return lienzo


def poner_logo(imagen, logo, posicion, tamano_rel, margen_rel, opacidad):
    ancho_logo = int(min(imagen.size) * tamano_rel)
    logo = logo.resize((ancho_logo, int(logo.height * ancho_logo / logo.width)), Image.LANCZOS)
    if opacidad < 1:
        alfa = logo.getchannel("A").point(lambda a: int(a * opacidad))
        logo.putalpha(alfa)
    m = int(min(imagen.size) * margen_rel)
    x = {"izquierda": m, "derecha": imagen.width - logo.width - m,
         "centro": (imagen.width - logo.width) // 2}[posicion.split("-")[1]]
    y = m if posicion.startswith("arriba") else imagen.height - logo.height - m
    imagen.alpha_composite(logo, (x, y))
    return imagen


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("imagen")
    parser.add_argument("--formatos", default="feed,story", help=f"Separados por coma: {', '.join(FORMATOS)}, original")
    parser.add_argument("--salida", help="Carpeta de salida (por defecto, la de la imagen)")
    parser.add_argument("--modo", choices=["recortar", "encajar"], default="recortar",
                        help="recortar: llena el formato; encajar: muestra todo con fondo liso")
    parser.add_argument("--fondo", default="#FFFFFF", help="Color de fondo para --modo encajar")
    parser.add_argument("--aire", type=float, default=0.10, help="Espacio libre alrededor en --modo encajar")
    parser.add_argument("--logo", default=str(LOGO_POR_DEFECTO))
    parser.add_argument("--sin-logo", action="store_true")
    parser.add_argument("--posicion", choices=sorted(POSICIONES), default="abajo-derecha")
    parser.add_argument("--tamano-logo", type=float, default=0.18, help="Ancho del logo relativo al lado menor")
    parser.add_argument("--margen", type=float, default=0.045, help="Margen relativo al lado menor")
    parser.add_argument("--opacidad", type=float, default=1.0)
    args = parser.parse_args()

    imagen = Image.open(args.imagen).convert("RGBA")
    logo = None
    if not args.sin_logo:
        if not Path(args.logo).exists():
            sys.exit(f"No encuentro el logo en {args.logo}. Subilo a marca/logos/logo.png o usá --sin-logo.")
        logo = Image.open(args.logo).convert("RGBA")

    origen = Path(args.imagen)
    salida = Path(args.salida) if args.salida else origen.parent
    salida.mkdir(parents=True, exist_ok=True)

    for nombre in args.formatos.split(","):
        nombre = nombre.strip()
        if nombre == "original":
            final = imagen.copy()
        elif nombre in FORMATOS:
            final = ajustar(imagen, FORMATOS[nombre], args.modo, args.fondo, args.aire)
        else:
            sys.exit(f"Formato desconocido: {nombre}")
        if logo:
            final = poner_logo(final, logo, args.posicion, args.tamano_logo, args.margen, args.opacidad)
        destino = salida / f"{origen.stem}_{nombre}.jpg"
        final.convert("RGB").save(destino, quality=92)
        print(destino)


if __name__ == "__main__":
    main()
