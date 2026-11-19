"""Fase 1: extrae el texto de los programas electorales página a página.

Uso:
    python pipeline/extract.py

Para cada ``Programas_Electorales/<PARTIDO>.pdf`` genera
``data/textos/<PARTIDO>.json`` con el formato ``[{"pagina": n, "texto": "..."}]``.
``pagina`` es la página física del PDF (índice + 1), no la numeración impresa,
para que los enlaces ``.pdf#page=N`` apunten al sitio correcto.

También escribe ``data/textos/fuentes.json`` con la huella SHA-256 de cada PDF,
de modo que cualquiera pueda comprobar que los datos salen de esos archivos.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from normalizar import limpiar  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DIR_PDF = RAIZ / "Programas_Electorales"
DIR_SALIDA = RAIZ / "data" / "textos"


def sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with ruta.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def fecha_pdf(meta: dict) -> str | None:
    """Convierte 'D:20261117190625+01'00'' en '2026-11-17'."""
    valor = meta.get("creationDate") or ""
    if valor.startswith("D:") and len(valor) >= 10:
        return f"{valor[2:6]}-{valor[6:8]}-{valor[8:10]}"
    return None


def extraer(ruta: Path) -> list[dict]:
    with pymupdf.open(ruta) as doc:
        return [
            {"pagina": i + 1, "texto": limpiar(pagina.get_text("text"))}
            for i, pagina in enumerate(doc)
        ]


def main() -> int:
    pdfs = sorted(DIR_PDF.glob("*.pdf"))
    if not pdfs:
        print(f"No hay PDF en {DIR_PDF}", file=sys.stderr)
        return 1
    DIR_SALIDA.mkdir(parents=True, exist_ok=True)

    fuentes = []
    for ruta in pdfs:
        partido = ruta.stem
        paginas = extraer(ruta)
        destino = DIR_SALIDA / f"{partido}.json"
        destino.write_text(
            json.dumps(paginas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        with pymupdf.open(ruta) as doc:
            meta = doc.metadata or {}
        sin_texto = [p["pagina"] for p in paginas if len(p["texto"]) < 30]
        fuentes.append(
            {
                "partido": partido,
                "archivo": f"Programas_Electorales/{ruta.name}",
                "sha256": sha256(ruta),
                "paginas": len(paginas),
                "fecha_pdf": fecha_pdf(meta),
                "paginas_sin_texto": sin_texto,
            }
        )
        total = sum(len(p["texto"]) for p in paginas)
        print(f"{partido:15} {len(paginas):4} págs. {total:8} caracteres -> {destino.relative_to(RAIZ)}")

    (DIR_SALIDA / "fuentes.json").write_text(
        json.dumps(fuentes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
