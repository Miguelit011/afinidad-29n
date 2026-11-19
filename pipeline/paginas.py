"""Imprime el texto (con espacios colapsados) de páginas concretas de un partido.

Uso: python pipeline/paginas.py PSOE 92-94 [100 ...]
"""
import json, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
partido, rangos = sys.argv[1], sys.argv[2:]
paginas = {p["pagina"]: p["texto"] for p in json.loads((RAIZ / "data" / "textos" / f"{partido}.json").read_text(encoding="utf-8"))}
for r in rangos:
    a, _, b = r.partition("-")
    for n in range(int(a), int(b or a) + 1):
        print(f"[[{partido} p{n}]] " + re.sub(r"\s+", " ", paginas.get(n, "")).strip())
