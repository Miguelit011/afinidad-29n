"""Fase 4: verifica las citas y el esquema de data/preguntas.json y data/catalogo/.

Para cada postura con valor (y cada entrada del catálogo) comprueba que la cita
existe en el texto del partido y precisamente en la página indicada:

1. Se normalizan cita y página (espacios, guiones de corte, comillas, viñetas,
   mayúsculas) y se busca la cita como subcadena exacta.
2. Si no aparece, se acepta con tolerancia fuzzy (rapidfuzz, >= 95) siempre que
   todas las cifras de la cita aparezcan en el fragmento alineado de la página.
   Así se toleran diferencias de maquetación sin aceptar un número cambiado.

Si algo falla, lista los errores y sale con código 1.

Uso:
    python pipeline/verify_quotes.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from rapidfuzz import fuzz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from normalizar import normalizar  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
UMBRAL_FUZZY = 95.0
VALORES = {-2, -1, 0, 1, 2, None}
_CIFRAS = re.compile(r"\d+(?:[.,]\d+)*")


def cargar_textos(dir_textos: Path) -> dict[str, dict[int, str]]:
    textos = {}
    for f in sorted(dir_textos.glob("*.json")):
        if f.stem == "fuentes":
            continue
        paginas = json.loads(f.read_text(encoding="utf-8"))
        textos[f.stem] = {p["pagina"]: normalizar(p["texto"]) for p in paginas}
    return textos


def verificar_cita(cita: str, texto_pagina_norm: str) -> tuple[bool, float]:
    """Devuelve (ok, puntuación) de la cita contra el texto ya normalizado de una página."""
    # Las comillas que envuelven la cita no forman parte del texto citado.
    c = normalizar(cita).strip("\"' ")
    if not c:
        return False, 0.0
    if c in texto_pagina_norm:
        return True, 100.0
    alin = fuzz.partial_ratio_alignment(c, texto_pagina_norm)
    if alin is None or alin.score < UMBRAL_FUZZY:
        return False, alin.score if alin else 0.0
    fragmento = texto_pagina_norm[alin.dest_start : alin.dest_end]
    if any(n not in fragmento for n in _CIFRAS.findall(c)):
        return False, alin.score
    return True, alin.score


def localizar(cita: str, paginas: dict[int, str]) -> list[int]:
    """Páginas donde la cita sí aparece (para orientar el mensaje de error)."""
    return [n for n, t in paginas.items() if verificar_cita(cita, t)[0]]


def comprobar_cita(origen: str, partido: str, cita, pagina, textos, errores: list[str], avisos: list[str]) -> None:
    if not isinstance(cita, str) or not cita.strip():
        errores.append(f"{origen}: falta la cita")
        return
    if not isinstance(pagina, int) or isinstance(pagina, bool):
        errores.append(f"{origen}: falta la página o no es un entero")
        return
    paginas = textos.get(partido)
    if paginas is None:
        errores.append(f"{origen}: no hay texto extraído para {partido}")
        return
    if pagina not in paginas:
        errores.append(f"{origen}: la página {pagina} no existe (el PDF tiene {len(paginas)})")
        return
    ok, score = verificar_cita(cita, paginas[pagina])
    if ok:
        if score < 100:
            avisos.append(f"{origen}: coincidencia aproximada ({score:.1f}) en p. {pagina}")
        return
    otras = localizar(cita, paginas)
    donde = f"; aparece en p. {', '.join(map(str, otras))}" if otras else "; no aparece en ninguna página"
    errores.append(f"{origen}: la cita no está en p. {pagina} (similitud {score:.1f}){donde}: «{cita[:70]}…»")


def validar_preguntas(datos: dict, textos: dict, errores: list[str], avisos: list[str]) -> None:
    for clave in ("partidos", "temas", "preguntas"):
        if not isinstance(datos.get(clave), list):
            errores.append(f"preguntas.json: falta la lista «{clave}»")
            return
    partidos = [p.get("id") for p in datos["partidos"]]
    temas = {t.get("id") for t in datos["temas"]}
    ids = set()
    for i, q in enumerate(datos["preguntas"]):
        qid = q.get("id", f"#{i}")
        if qid in ids:
            errores.append(f"{qid}: id duplicado")
        ids.add(qid)
        for campo in ("texto", "contexto", "de_acuerdo", "en_desacuerdo"):
            if not isinstance(q.get(campo), str) or not q[campo].strip():
                errores.append(f"{qid}: falta «{campo}»")
        if q.get("tema") not in temas:
            errores.append(f"{qid}: tema desconocido «{q.get('tema')}»")
        posturas = q.get("posturas")
        if not isinstance(posturas, dict):
            errores.append(f"{qid}: falta «posturas»")
            continue
        if set(posturas) != set(partidos):
            errores.append(f"{qid}: las posturas deben cubrir exactamente {partidos}")
        valores = []
        for partido, p in posturas.items():
            origen = f"{qid}/{partido}"
            if not isinstance(p, dict) or "valor" not in p:
                errores.append(f"{origen}: postura mal formada")
                continue
            v = p["valor"]
            if isinstance(v, bool) or v not in VALORES:
                errores.append(f"{origen}: valor {v!r} fuera de {{-2..2, null}}")
                continue
            if v is None:
                continue
            valores.append(v)
            comprobar_cita(origen, partido, p.get("cita"), p.get("pagina"), textos, errores, avisos)
        if len(set(valores)) < 2:
            errores.append(f"{qid}: no separa a los partidos (posturas {valores})")


def validar_catalogo(dir_catalogo: Path, textos: dict, temas: set, errores: list[str], avisos: list[str]) -> int:
    n = 0
    for f in sorted(dir_catalogo.glob("*.json")):
        for i, e in enumerate(json.loads(f.read_text(encoding="utf-8"))):
            origen = f"catalogo/{f.stem}#{i}"
            if e.get("tema") not in temas:
                errores.append(f"{origen}: tema desconocido «{e.get('tema')}»")
            if not isinstance(e.get("resumen"), str) or not e["resumen"].strip():
                errores.append(f"{origen}: falta el resumen")
            comprobar_cita(origen, f.stem, e.get("cita_literal"), e.get("pagina"), textos, errores, avisos)
            n += 1
    return n


def main(raiz: Path = RAIZ) -> int:
    textos = cargar_textos(raiz / "data" / "textos")
    datos = json.loads((raiz / "data" / "preguntas.json").read_text(encoding="utf-8"))
    errores: list[str] = []
    avisos: list[str] = []
    validar_preguntas(datos, textos, errores, avisos)
    temas = {t.get("id") for t in datos.get("temas", [])}
    n_cat = validar_catalogo(raiz / "data" / "catalogo", textos, temas, errores, avisos)

    for a in avisos:
        print(f"AVISO  {a}")
    if errores:
        for e in errores:
            print(f"ERROR  {e}", file=sys.stderr)
        print(f"\n{len(errores)} error(es).", file=sys.stderr)
        return 1
    n_citas = sum(1 for q in datos["preguntas"] for p in q["posturas"].values() if p["valor"] is not None)
    print(f"OK: {len(datos['preguntas'])} preguntas, {n_citas} citas de posturas y {n_cat} del catálogo verificadas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
