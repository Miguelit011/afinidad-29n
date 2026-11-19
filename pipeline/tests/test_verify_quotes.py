import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import verify_quotes as vq  # noqa: E402
from normalizar import normalizar  # noqa: E402

PAGINA = normalizar(
    "1. Bajar los alquileres un 40% por ley. Aprobaremos una reducción extraordinaria\n"
    "del 40 % de los precios del alqui-\nler, aplicable a los contratos vigentes."
)
TEXTOS = {"A": {1: PAGINA, 2: normalizar("Otra página sin relación con la vivienda.")}, "B": {1: PAGINA}}


def test_cita_exacta():
    assert vq.verificar_cita("Bajar los alquileres un 40% por ley.", PAGINA) == (True, 100.0)


def test_cita_con_salto_de_linea_y_guion_de_corte():
    ok, _ = vq.verificar_cita("del 40 % de los precios del alquiler, aplicable a los contratos vigentes.", PAGINA)
    assert ok


def test_cita_con_comillas_y_mayusculas_distintas():
    ok, _ = vq.verificar_cita("«BAJAR LOS ALQUILERES UN 40% POR LEY.»", PAGINA)
    assert ok


def test_cifra_cambiada_falla_aunque_el_parecido_sea_alto():
    ok, score = vq.verificar_cita("Aprobaremos una reducción extraordinaria del 50 % de los precios del alquiler", PAGINA)
    assert not ok
    assert score >= 90  # el fuzzy solo no lo habría detectado


def test_texto_inventado_falla():
    ok, _ = vq.verificar_cita("Prohibiremos los alquileres turísticos en toda España.", PAGINA)
    assert not ok


def _datos(**cambios):
    base = {
        "partidos": [{"id": "A"}, {"id": "B"}],
        "temas": [{"id": "vivienda"}],
        "preguntas": [
            {
                "id": "q1",
                "tema": "vivienda",
                "texto": "¿Limitar el alquiler?",
                "contexto": "Contexto.",
                "posturas": {
                    "A": {"valor": 2, "cita": "Bajar los alquileres un 40% por ley.", "pagina": 1},
                    "B": {"valor": None, "cita": None, "pagina": None},
                },
            }
        ],
    }
    base["preguntas"][0]["posturas"]["B"] = cambios.get("B", base["preguntas"][0]["posturas"]["B"])
    base["preguntas"][0]["posturas"]["A"] = cambios.get("A", base["preguntas"][0]["posturas"]["A"])
    return base


def _validar(datos):
    errores, avisos = [], []
    vq.validar_preguntas(datos, TEXTOS, errores, avisos)
    return errores


def test_no_separa_si_solo_hay_una_postura():
    assert any("no separa" in e for e in _validar(_datos()))


def test_esquema_valido_con_null():
    datos = _datos(B={"valor": -2, "cita": "Bajar los alquileres un 40% por ley.", "pagina": 1})
    assert _validar(datos) == []


@pytest.mark.parametrize("valor", [3, -3, 1.5, "2", True])
def test_valor_fuera_de_rango(valor):
    datos = _datos(B={"valor": valor, "cita": "x", "pagina": 1})
    assert any("fuera de" in e for e in _validar(datos))


def test_valor_sin_cita_falla():
    datos = _datos(B={"valor": -1, "cita": None, "pagina": 1})
    assert any("falta la cita" in e for e in _validar(datos))


def test_valor_sin_pagina_falla():
    datos = _datos(B={"valor": -1, "cita": "Bajar los alquileres un 40% por ley.", "pagina": None})
    assert any("página" in e for e in _validar(datos))


def test_pagina_equivocada_indica_la_correcta():
    datos = _datos(A={"valor": 2, "cita": "Bajar los alquileres un 40% por ley.", "pagina": 2},
                   B={"valor": -2, "cita": "Bajar los alquileres un 40% por ley.", "pagina": 1})
    errores = _validar(datos)
    assert any("no está en p. 2" in e and "aparece en p. 1" in e for e in errores)


def test_faltan_partidos():
    datos = _datos(B={"valor": -2, "cita": "Bajar los alquileres un 40% por ley.", "pagina": 1})
    del datos["preguntas"][0]["posturas"]["B"]
    assert any("exactamente" in e for e in _validar(datos))


def test_datos_reales_del_repositorio_pasan():
    """Integración: todas las citas de data/ deben verificarse."""
    assert vq.main() == 0
