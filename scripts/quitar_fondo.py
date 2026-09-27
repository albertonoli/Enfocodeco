#!/usr/bin/env python3
"""Quita el fondo de fotos de producto y guarda PNG con transparencia.

Uso:
    python scripts/quitar_fondo.py foto1.jpg foto2.jpg
    python scripts/quitar_fondo.py productos/apliques/ --salida salidas/recortes
"""
import argparse
import sys
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
EXTENSIONES = {".jpg", ".jpeg", ".png", ".webp"}


def listar_imagenes(entradas):
    for entrada in entradas:
        ruta = Path(entrada)
        if ruta.is_dir():
            yield from sorted(p for p in ruta.rglob("*") if p.suffix.lower() in EXTENSIONES)
        elif ruta.is_file():
            yield ruta
        else:
            print(f"⚠️  No existe: {ruta}", file=sys.stderr)


def recortar_al_producto(imagen, margen):
    """Recorta el lienzo al contorno del producto, dejando un margen relativo."""
    # Umbral: rembg deja píxeles casi transparentes en el fondo que agrandarían la caja.
    caja = imagen.getchannel("A").point(lambda a: 255 if a > 16 else 0).getbbox()
    if not caja:
        return imagen
    izq, arr, der, aba = caja
    m = int(max(der - izq, aba - arr) * margen)
    return imagen.crop((max(izq - m, 0), max(arr - m, 0),
                        min(der + m, imagen.width), min(aba + m, imagen.height)))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("entradas", nargs="+", help="Archivos o carpetas con fotos")
    parser.add_argument("--salida", default=str(RAIZ / "salidas" / "recortes"), help="Carpeta de salida")
    parser.add_argument("--modelo", default="isnet-general-use",
                        help="Modelo de rembg (isnet-general-use, u2net, birefnet-general...)")
    parser.add_argument("--sin-recortar", action="store_true", help="Mantener el tamaño original del lienzo")
    parser.add_argument("--margen", type=float, default=0.03, help="Margen alrededor del producto (0.03 = 3%%)")
    args = parser.parse_args()

    # Import diferido: rembg tarda en cargar y descarga el modelo la primera vez.
    from rembg import new_session, remove

    sesion = new_session(args.modelo)
    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)

    generadas = []
    for ruta in listar_imagenes(args.entradas):
        imagen = remove(Image.open(ruta).convert("RGB"), session=sesion)
        if not args.sin_recortar:
            imagen = recortar_al_producto(imagen, args.margen)
        destino = salida / f"{ruta.stem}_recorte.png"
        imagen.save(destino)
        generadas.append(destino)
        print(destino)

    if not generadas:
        sys.exit("No se encontró ninguna imagen para procesar.")


if __name__ == "__main__":
    main()
