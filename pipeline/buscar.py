"""Busca términos en los textos extraídos y muestra página y contexto.

Uso:
    python pipeline/buscar.py "alquiler" "zonas tensionadas" [-p PP,VOX] [-c 250] [-n 8]

Todos los términos deben aparecer en la misma página (búsqueda normalizada:
sin distinguir mayúsculas, comillas ni saltos de línea). Se muestra el
contexto alrededor del primer término.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from normalizar import normalizar  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DIR_TEXTOS = RAIZ / "data" / "textos"


def partidos() -> list[str]:
    return sorted(p.stem for p in DIR_TEXTOS.glob("*.json") if p.stem != "fuentes")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("terminos", nargs="+")
    ap.add_argument("-p", "--partidos", default="")
    ap.add_argument("-c", "--contexto", type=int, default=250)
    ap.add_argument("-n", "--max", type=int, default=6, help="máximo de coincidencias por partido")
    args = ap.parse_args()

    elegidos = args.partidos.split(",") if args.partidos else partidos()
    terminos = [normalizar(t) for t in args.terminos]
    for partido in elegidos:
        paginas = json.loads((DIR_TEXTOS / f"{partido}.json").read_text(encoding="utf-8"))
        hits = 0
        print(f"===== {partido}")
        for pag in paginas:
            texto = re.sub(r"\s+", " ", pag["texto"])
            norm = normalizar(texto)
            if not all(t in norm for t in terminos):
                continue
            # normalizar conserva longitudes salvo en casos raros; buscamos sobre el texto
            # con espacios colapsados sin distinguir mayúsculas para mostrar el original.
            m = re.search(re.escape(args.terminos[0]), texto, re.I)
            i = m.start() if m else norm.find(terminos[0])
            ini, fin = max(0, i - args.contexto), i + args.contexto
            print(f"  p{pag['pagina']}: …{texto[ini:fin]}…")
            hits += 1
            if hits >= args.max:
                print("  (más resultados omitidos)")
                break
    return 0


if __name__ == "__main__":
    sys.exit(main())
