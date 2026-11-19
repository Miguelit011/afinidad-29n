"""Genera web/public/logos/<PARTIDO>.png a partir del propio programa electoral.

Cada logotipo se recorta de la portada o contraportada del PDF oficial (sin
descargar nada de fuera) y se coloca, centrado y con margen, sobre una ficha de
tamaño fijo con el color de fondo que tiene en el programa. Así todas las fichas
miden lo mismo junto a los porcentajes de la web.

Uso:
    python pipeline/logos.py
"""

from __future__ import annotations

from pathlib import Path

import pymupdf

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "web" / "public" / "logos"

# Ficha de 3:2; se rasteriza al triple para que se vea nítida en pantallas de alta densidad.
ANCHO, ALTO, MARGEN = 120.0, 80.0, 12.0
DPI = round(72 * 3 * 60 / ANCHO)  # 60 px CSS de ancho a 3x (108 ppp)

# partido: (página física 1-based, recorte (x0, y0, x1, y1) en puntos PDF)
RECORTES = {
    "FRENTE_AMPLIO": (151, (192, 358, 403, 442)),  # contraportada
    "PODEMOS": (141, (393, 742, 530, 782)),  # contraportada, abajo a la derecha
    "PP": (64, (262, 732, 333, 782)),  # contraportada, abajo al centro
    "PSOE": (114, (318, 728, 522, 778)),  # contraportada, «PSOE/♥»
    "VOX": (66, (112, 150, 308, 252)),  # contraportada, centro
}


def generar() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    for partido, (num, caja) in RECORTES.items():
        origen = pymupdf.open(RAIZ / "Programas_Electorales" / f"{partido}.pdf")
        # El recorte se rasteriza tal cual se ve en el programa (con alta resolución) y el color de
        # fondo de la ficha se toma de esa misma imagen, en el centro de su borde izquierdo, donde
        # no hay logotipo. Así fondo y logotipo coinciden aunque el fondo original sea una imagen.
        logo = origen[num - 1].get_pixmap(clip=pymupdf.Rect(caja), dpi=600)
        r, g, b = logo.pixel(1, logo.height // 2)[:3]
        fondo = (r / 255, g / 255, b / 255)

        ficha = pymupdf.open()
        pag = ficha.new_page(width=ANCHO, height=ALTO)
        pag.draw_rect(pag.rect, color=None, fill=fondo)
        # Encaja el logotipo dentro de la ficha conservando la proporción
        hueco = pymupdf.Rect(MARGEN, MARGEN, ANCHO - MARGEN, ALTO - MARGEN)
        pag.insert_image(hueco, pixmap=logo, keep_proportion=True)

        salida = DESTINO / f"{partido}.png"
        pag.get_pixmap(dpi=DPI).save(salida)
        print(f"{partido:14} p. {num:>3} -> {salida.relative_to(RAIZ)} ({salida.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    generar()
