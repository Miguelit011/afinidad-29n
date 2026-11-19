"""Normalización de texto compartida por la extracción y el verificador de citas.

Hay dos niveles:

* ``limpiar``: limpieza conservadora para guardar el texto de cada página.
  Mantiene mayúsculas, puntuación y saltos de línea, de modo que las citas
  copiadas de ``data/textos`` se lean igual que en el PDF.
* ``normalizar``: forma canónica para comparar (búsquedas y verificación).
  Es agresiva: minúsculas, comillas y guiones unificados, sin viñetas y con
  los espacios colapsados.
"""

from __future__ import annotations

import re
import unicodedata

# Guion blando (U+00AD): InDesign lo usa en los cortes de palabra («elec­ ciones»).
_GUION_BLANDO = re.compile(r"­\s*")
# Guion de corte al final de línea seguido de minúscula: «deci-\nsiones» → «decisiones».
_GUION_CORTE = re.compile(r"(?<=[^\W\d_])-[ \t]*\n[ \t]*(?=[a-záéíóúüñ])")
# En titulares en mayúsculas: «SOCIEDA-\nDES» → «SOCIEDADES» (dos mayúsculas a cada lado).
_GUION_CORTE_MAYUS = re.compile(r"(?<=[A-ZÁÉÍÓÚÜÑ]{2})-[ \t]*\n[ \t]*(?=[A-ZÁÉÍÓÚÜÑ]{2})")
_ESPACIOS_LINEA = re.compile(r"[ \t  -   　]+")
_LINEAS_VACIAS = re.compile(r"\n{3,}")
_ANCHO_CERO = re.compile(r"[​-‍⁠﻿]")

_COMILLAS = str.maketrans(
    {
        "“": '"', "”": '"', "„": '"', "«": '"', "»": '"',
        "‘": "'", "’": "'", "‚": "'", "′": "'", "´": "'",
        "‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-",
        "―": "-", "−": "-",
        "…": "...",
    }
)
# Viñetas y símbolos decorativos que no forman parte del contenido.
_VINETAS = re.compile(r"[•●○▪■►▶‣⁃➢✓✔]")
_ESPACIOS = re.compile(r"\s+")


def limpiar(texto: str) -> str:
    """Limpieza conservadora del texto extraído de una página."""
    texto = unicodedata.normalize("NFC", texto)
    texto = _ANCHO_CERO.sub("", texto)
    # Ligaduras tipográficas (ﬁ, ﬂ, ﬀ…): NFKC solo sobre ellas para no tocar el resto.
    texto = re.sub(r"[ﬀ-ﬆ]", lambda m: unicodedata.normalize("NFKC", m.group()), texto)
    texto = _GUION_BLANDO.sub("", texto)
    texto = _GUION_CORTE.sub("", texto)
    texto = _GUION_CORTE_MAYUS.sub("", texto)
    texto = _ESPACIOS_LINEA.sub(" ", texto)
    texto = "\n".join(linea.strip() for linea in texto.split("\n"))
    texto = _LINEAS_VACIAS.sub("\n\n", texto)
    return texto.strip()


def normalizar(texto: str) -> str:
    """Forma canónica para comparar textos (búsqueda y verificación de citas)."""
    texto = limpiar(texto)
    texto = unicodedata.normalize("NFKC", texto)
    texto = texto.translate(_COMILLAS)
    texto = _VINETAS.sub(" ", texto)
    texto = _ESPACIOS.sub(" ", texto)
    return texto.strip().casefold()
