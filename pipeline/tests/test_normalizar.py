import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from normalizar import limpiar, normalizar  # noqa: E402


def test_guion_blando_se_une():
    assert limpiar("elec­ ciones generales") == "elecciones generales"
    assert limpiar("inme­\ndiato") == "inmediato"


def test_guion_de_corte_de_linea_se_une():
    assert limpiar("deci-\nsiones a su altura") == "decisiones a su altura"


def test_guion_real_se_conserva():
    # Seguido de mayúscula o número no es un corte de palabra.
    assert limpiar("Castilla-\nLa Mancha") == "Castilla-\nLa Mancha"
    assert limpiar("2027-2030") == "2027-2030"


def test_ligaduras():
    assert limpiar("eﬁciencia y ﬂujo") == "eficiencia y flujo"


def test_espacios_y_lineas():
    assert limpiar("  hola  \t mundo  \n\n\n\nfin ") == "hola mundo\n\nfin"


def test_normalizar_comillas_vinetas_y_mayusculas():
    a = normalizar("● Bajaremos el «IRPF» — a las “familias”")
    b = normalizar('bajaremos el "irpf" - a las "familias"')
    assert a == b


def test_normalizar_saltos_de_linea_equivalen_a_espacios():
    assert normalizar("parque público\nde vivienda") == normalizar("parque público de vivienda")
