"""Fases 2 y 3: construye data/preguntas.json y data/catalogo/<PARTIDO>.json.

Este archivo es la fuente editorial: aquí están las afirmaciones, la codificación
de cada partido (-2..2 o sin postura) y, para cada cita, su página y una frase de
inicio y otra de fin. La cita se recorta del texto extraído (data/textos), de modo
que es una copia literal del programa y no una transcripción.

Para corregir una codificación: edita la entrada correspondiente y ejecuta
    python pipeline/construir_datos.py
y después  python pipeline/verify_quotes.py
"""
import json, re, sys
from pathlib import Path

RAIZ = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
TEXTOS = {}
for f in (RAIZ / "data" / "textos").glob("*.json"):
    if f.stem != "fuentes":
        TEXTOS[f.stem] = {p["pagina"]: re.sub(r"\s+", " ", p["texto"]).strip() for p in json.loads(f.read_text(encoding="utf-8"))}

ERRORES = []


def cita(partido, pagina, inicio, fin):
    t = TEXTOS[partido][pagina]
    i = t.find(inicio)
    if i < 0:
        ERRORES.append(f"{partido} p{pagina}: no encuentro el inicio «{inicio}»")
        return None
    j = t.find(fin, i)
    if j < 0:
        ERRORES.append(f"{partido} p{pagina}: no encuentro el fin «{fin}»")
        return None
    c = t[i : j + len(fin)]
    n = len(c.split())
    if n > 45:
        ERRORES.append(f"{partido} p{pagina}: cita de {n} palabras (máx. ~40): «{c[:60]}…»")
    return c


def P(valor, partido, pagina, inicio, fin, inferida=False, nota=None):
    return {"partido": partido, "valor": valor, "cita": cita(partido, pagina, inicio, fin), "pagina": pagina,
            "inferida": inferida, "nota": nota}


FA, POD, PP, PSOE, VOX = "FRENTE_AMPLIO", "PODEMOS", "PP", "PSOE", "VOX"
PARTIDOS = [FA, POD, PP, PSOE, VOX]
LOGRO = "El programa lo presenta como un logro ya aprobado, no como un compromiso nuevo."

PREGUNTAS = [
    # ---------------- VIVIENDA ----------------
    dict(id="viv-1", tema="vivienda", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Debería haber un precio máximo para el alquiler en las zonas donde alquilar es muy caro.",
         contexto="La ley ya permite poner ese tope, pero solo si la comunidad autónoma lo pide para sus zonas más caras. Cada comunidad decide.",
         de_acuerdo="El alquiler tendría un límite en esas zonas.",
         en_desacuerdo="El precio lo seguiría fijando libremente el propietario.",
         posturas=[
             P(2, FA, 13, "Limitaremos por ley el precio del alquiler", "en todas las zonas tensionadas"),
             P(2, POD, 8, "Bajar los alquileres un 40% por ley.", "de los precios del alquiler"),
             P(1, PSOE, 30, "Congelar temporalmente las rentas", "en los mercados tensionados."),
             P(-2, PP, 42, "Eliminaremos las zonas tensionadas", "menos oferta en el mercado del alquiler."),
             P(-1, VOX, 23, "Recuperar la seguridad jurídica y una oferta de alquileres", "Derogación de la Ley de Vivienda.", inferida=True,
               nota="La Ley de Vivienda es la norma que permite limitar el alquiler en zonas tensionadas; el programa propone derogarla."),
         ]),
    dict(id="viv-2", tema="vivienda", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Debería prohibirse desahuciar a familias vulnerables que no tienen otra casa a la que ir.",
         contexto="Hoy hay algunas protecciones: por ejemplo, se avisa a los servicios sociales y el juez puede aplazar el desahucio un tiempo. Pero no hay una prohibición permanente.",
         de_acuerdo="No se podría desahuciar a estas familias hasta que tuvieran otra vivienda.",
         en_desacuerdo="Se las podría desahuciar, aunque con algunas protecciones, como los aplazamientos.",
         posturas=[
             P(2, FA, 15, "Prohibiremos de forma permanente y con rango de ley", "alternativa habitacional digna, adecuada y estable."),
             P(2, POD, 9, "Prohibiremos los desahucios y lanzamientos de personas en situación de vulnerabilidad", "digna y adecuada"),
             P(2, PSOE, 33, "Asegurar que el coste de la prohibición de los desahucios a personas vulnerables", "directamente las administraciones."),
             P(-1, PP, 42, "DEROGAREMOS LA LEY DE VIVIENDA.", "propietarios e inquilinos.", inferida=True,
               nota="Propone derogar la ley de vivienda de 2023, que incluye protecciones frente al desahucio de familias vulnerables."),
             P(-1, VOX, 24, "Mano dura contra la okupación y la inquiocupación.", "por su legítimo titular, el propietario.", inferida=True,
               nota="Propone recuperar de inmediato la vivienda también cuando el inquilino deja de pagar («inquiocupación»), sin mencionar excepciones."),
         ]),
    # ---------------- FISCALIDAD ----------------
    dict(id="fis-1", tema="fiscalidad", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Las personas que más ganan deberían pagar más impuestos por lo que ganan.",
         contexto="En la declaración de la renta, cuanto más se gana, mayor es el porcentaje que se paga. Por la parte más alta de los ingresos se paga hoy entre el 45 % y el 54 %, según la comunidad autónoma.",
         de_acuerdo="Subiría el impuesto de la renta a quienes más ganan.",
         en_desacuerdo="Se quedaría igual o bajaría.",
         posturas=[
             P(2, POD, 21, "Reforma del IRPF para que las rentas más altas contribuyan más.", "contribuyan más."),
             P(2, FA, 46, "Ampliaremos el número de tramos del IRPF", "para rentas a partir de 300.000 euros."),
             P(1, PSOE, 48, "Introducir progresividad a la imposición del capital.", "rentas de capital más elevadas.",
               nota="Solo se refiere a las rentas del capital, no a las del trabajo."),
             P(-1, VOX, 9, "Reforma del sistema de tributación sobre la renta (IRPF).", "Simplificación y bajada del IRPF.", inferida=True,
               nota="Propone bajar el IRPF con carácter general, sin referirse expresamente a las rentas altas."),
         ]),
    dict(id="fis-2", tema="fiscalidad", formulada_desde="PP/VOX",
         texto="Las empresas deberían pagar menos impuestos por lo que ganan.",
         contexto="Hoy pagan, en general, el 25 % de sus beneficios, y algo menos las empresas pequeñas.",
         de_acuerdo="Bajaría ese impuesto.",
         en_desacuerdo="Se quedaría igual o subiría.",
         posturas=[
             P(2, VOX, 9, "Reducir el tipo del Impuesto de Sociedades", "dinamización de nuestra economía"),
             P(1, PP, 47, "LA EMPRESA QUE INVIERTA PARA CRECER PAGARÁ MENOS IMPUESTO SOBRE SOCIEDADES.", "SOBRE SOCIEDADES.",
               nota="La rebaja se limita a las empresas que invierten (libertad de amortización)."),
             P(-2, FA, 8, "Nuestra reforma fiscal hará que el nuevo esfuerzo tributario recaiga", "tipo mínimo real del 20 % en Sociedades"),
             P(-2, POD, 21, "Reforma del impuesto de sociedades para que las grandes empresas", "aumentar su capacidad recaudatoria"),
             P(-1, PSOE, 48, "Aumentar la tributación de las empresas cotizadas", "supere 100 a 1",
               nota="Solo para empresas cotizadas con grandes diferencias salariales internas."),
         ]),
    dict(id="fis-3", tema="fiscalidad", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Las grandes fortunas deberían pagar un impuesto igual en toda España, que ninguna comunidad autónoma pueda quitar.",
         contexto="Hay un impuesto por lo que se tiene (casas, dinero, acciones…). Lo gestionan las comunidades autónomas y algunas, en la práctica, no lo cobran. Desde 2022 hay además uno estatal para las grandes fortunas, aprobado como temporal.",
         de_acuerdo="Las grandes fortunas pagarían ese impuesto vivan donde vivan.",
         en_desacuerdo="Cada comunidad seguiría decidiendo si lo cobra.",
         posturas=[
             P(2, POD, 17, "Ampliaremos el impuesto a las grandes fortunas", "para evitar que las Comunidades Autónomas lo eliminen."),
             P(2, FA, 45, "Reformaremos el Impuesto de Solidaridad de las Grandes Fortunas", "paguen como mínimo el 2 %."),
             P(1, PSOE, 107, "Impulsar la creación de un impuesto mínimo global sobre las grandes fortunas", "sobre las grandes fortunas", inferida=True,
               nota="Propone un impuesto de ámbito internacional, no estatal."),
             P(-1, PP, 47, "Las Comunidades Autónomas seguirán decidiendo con libertad", "y podrán bajarlos cuanto quieran.", inferida=True,
               nota="Defiende que las comunidades puedan bajar libremente los impuestos cedidos, como el de Patrimonio."),
             P(-1, VOX, 9, "Revisión y reducción sistemática de todos los impuestos", "lastran la prosperidad", inferida=True,
               nota="Propone reducir todos los impuestos, sin mencionar expresamente el de grandes fortunas."),
         ]),
    # ---------------- EMPLEO ----------------
    dict(id="emp-1", tema="empleo", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="La jornada de trabajo debería bajar a 35 horas a la semana o menos, cobrando lo mismo.",
         contexto="Hoy el máximo es de 40 horas a la semana. Se propuso bajarlo a 37,5 horas, pero no se aprobó.",
         de_acuerdo="Se trabajaría como máximo 35 horas a la semana, sin bajar el sueldo.",
         en_desacuerdo="El máximo seguiría en 40 horas o bajaría menos.",
         posturas=[
             P(2, POD, 41, "Reduciremos la jornada laboral a 30 horas semanales", "comenzando con una bajada a 35 horas"),
             P(2, FA, 7, "Avanzaremos hacia la jornada laboral máxima de 32 horas semanales", "sin reducción salarial"),
             P(1, PSOE, 41, "Completar la reducción de la jornada a 37,5 horas", "hacia las 35 horas.",
               nota="Por ley hasta 37,5 horas; las 35 horas, mediante la negociación colectiva."),
         ]),
    dict(id="emp-2", tema="empleo", formulada_desde="PP/VOX",
         texto="Las empresas deberían tener más libertad para hacer contratos temporales.",
         contexto="Desde 2021, el contrato normal es el fijo. Los temporales solo se permiten por motivos concretos, como sustituir a alguien o un aumento del trabajo, y hay una excepción de hasta 90 días al año.",
         de_acuerdo="Sería más fácil hacer contratos temporales.",
         en_desacuerdo="Seguirían los límites actuales, o serían más estrictos.",
         posturas=[
             P(1, VOX, 13, "Derogar la legislación laboral de Sánchez", "agravado la precariedad", inferida=True,
               nota="Se entiende que «la legislación laboral de Sánchez» incluye la reforma laboral de 2021, que limitó los contratos temporales."),
             P(-2, POD, 42, "Eliminaremos la posibilidad de recurrir a la contratación temporal sin causa justificada", "durante 90 días al año"),
             P(-1, PSOE, 90, "La reforma laboral ha reforzado la estabilidad en el empleo", "limitando el abuso de la temporalidad.", nota=LOGRO),
             P(-1, FA, 54, "A pesar de que la reforma laboral ha dado lugar", "de empleo estable", inferida=True,
               nota="Valora positivamente la reforma laboral que limitó los contratos temporales, sin un compromiso expreso sobre ella."),
         ]),
    # ---------------- PENSIONES ----------------
    dict(id="pen-1", tema="pensiones", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="La pensión mínima de quien ha trabajado debería ser igual al salario mínimo.",
         contexto="Hoy la pensión mínima es más baja que el salario mínimo, que es lo menos que se puede pagar por trabajar a jornada completa.",
         de_acuerdo="La pensión mínima subiría hasta igualar el salario mínimo.",
         en_desacuerdo="Seguiría siendo más baja que el salario mínimo.",
         posturas=[
             P(2, FA, 57, "Blindaje constitucional del carácter público de las pensiones", "pensión mínima igual al SMI"),
             P(2, POD, 44, "Equiparar la pensión mínima al salario mínimo interprofesional.", "se equipare al SMI"),
             P(1, PSOE, 39, "culminando el proceso de convergencia de las cuantías de las pensiones mínimas", "del conjunto de la sociedad.",
               nota="Propone acercar las pensiones mínimas a «estándares de ingresos», sin fijar el SMI como referencia."),
         ]),
    # ---------------- SANIDAD ----------------
    dict(id="san-1", tema="sanidad", formulada_desde="PP/VOX",
         texto="La sanidad pública debería pagar a clínicas privadas para reducir las listas de espera.",
         contexto="Ya se hace en muchas comunidades autónomas: la sanidad pública paga a una clínica privada para que atienda a pacientes que están esperando. El paciente no paga nada.",
         de_acuerdo="Se usaría más esta fórmula.",
         en_desacuerdo="Se usaría menos o se dejaría de usar.",
         posturas=[
             P(2, VOX, 37, "Fomento de la colaboración público-privada", "a reducir demoras"),
             P(-1, PSOE, 49, "Limitar la privatización de la sanidad", "en la prestación sanitaria."),
             P(-2, FA, 26, "Derogaremos expresamente la Ley 15/1997", "colaboración con entidades privadas"),
             P(-2, POD, 88, "Acabar con la privatización y recuperar la sanidad para lo público.", "para lo público."),
         ]),
    dict(id="san-2", tema="sanidad", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Los inmigrantes sin papeles deberían poder usar la sanidad pública igual que los demás.",
         contexto="Desde 2018 tienen derecho a la sanidad pública, pero con algunos requisitos que no se piden al resto.",
         de_acuerdo="Se quitarían esos requisitos.",
         en_desacuerdo="Seguirían los requisitos, o su acceso se limitaría más (por ejemplo, solo a urgencias).",
         posturas=[
             P(2, FA, 26, "Blindaremos por ley la universalidad de la atención sanitaria", "independientemente de su estatus administrativo."),
             P(2, POD, 69, "incluidas las personas migrantes en situación administrativa irregular", "que impiden recibir atención"),
             P(1, PSOE, 46, "En sanidad, devolvimos la universalidad al Sistema Nacional de Salud", "al Sistema Nacional de Salud", inferida=True,
               nota=LOGRO + " Se entiende que «universalidad» incluye a las personas en situación irregular."),
             P(-2, VOX, 19, "Garantizar la sostenibilidad del sistema sanitario", "salvo casos de urgencia grave."),
         ]),
    # ---------------- EDUCACIÓN ----------------
    dict(id="edu-1", tema="educacion", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Los colegios concertados deberían recibir cada vez menos dinero público.",
         contexto="Los concertados son colegios privados que reciben dinero público y, a cambio, no cobran las clases en la enseñanza obligatoria.",
         de_acuerdo="Irían recibiendo menos dinero público.",
         en_desacuerdo="Seguirían recibiendo lo mismo o más.",
         posturas=[
             P(2, POD, 79, "Avanzaremos hacia una única red educativa de gestión pública directa", "para financiar negocios privados."),
             P(-2, PP, 51, "LOS PADRES ELEGIRÁN COLEGIO, Y NINGÚN CONCIERTO EDUCATIVO SE ELIMINARÁ", "DEMANDA SUFICIENTE."),
             P(-1, VOX, 41, "Garantizar la libre elección de centro educativo en todos los niveles", "sea un impedimento para ello.", inferida=True,
               nota="La libre elección de centro sin barreras económicas supone mantener la red concertada."),
         ]),
    dict(id="edu-2", tema="educacion", formulada_desde="PP/VOX",
         texto="Todos los alumnos de España deberían tener garantizado poder estudiar en castellano.",
         contexto="En las comunidades con otra lengua oficial (catalán, valenciano, euskera, gallego), cada comunidad decide cuántas clases se dan en cada lengua. En Cataluña, la mayoría se dan en catalán.",
         de_acuerdo="Cualquier alumno podría recibir las clases en castellano, viva donde viva.",
         en_desacuerdo="Cada comunidad seguiría decidiendo en qué lengua se dan las clases.",
         posturas=[
             P(2, PP, 32, "Garantizaremos el derecho constitucional de recibir enseñanza en castellano", "y en toda la Nación"),
             P(2, VOX, 41, "Se garantizará la educación en español en todo el territorio nacional.", "en todo el territorio nacional."),
             P(-1, FA, 32, "Lanzaremos un Plan Estatal para el aprendizaje y divulgación de las lenguas cooficiales", "como lengua vehicular en Cataluña.", inferida=True,
               nota="Defiende la inmersión en catalán, lo que choca con garantizar la enseñanza en castellano en toda España."),
         ]),
    dict(id="edu-3", tema="educacion", formulada_desde="PP/VOX",
         texto="Para pasar de curso en la ESO deberían tener que aprobarse todas las asignaturas.",
         contexto="Hoy, en la ESO, se pasa de curso con una o dos asignaturas suspendidas, y con más si los profesores del alumno lo deciden.",
         de_acuerdo="Solo se pasaría de curso con todo aprobado.",
         en_desacuerdo="Se podría seguir pasando con alguna asignatura suspendida.",
         posturas=[
             P(2, PP, 52, "En la ESO volverá a pasarse de curso con las asignaturas aprobadas.", "antes de tener que repetir."),
             P(1, VOX, 41, "Derogación de la LOMLOE", "la responsabilidad personal.", inferida=True,
               nota="Propone sustituir la ley educativa actual, que permite pasar de curso con suspensos, y recuperar la «exigencia»."),
         ]),
    # ---------------- INMIGRACIÓN ----------------
    dict(id="inm-1", tema="inmigracion", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Debería darse permiso para vivir y trabajar, de una vez, a los inmigrantes que ya viven en España sin papeles.",
         contexto="Lo normal es pedirlo caso a caso: por ejemplo, demostrando que se llevan años en España y se tiene trabajo o familia aquí. En 2026 se abrió además un proceso extraordinario para que muchas personas lo pidieran a la vez.",
         de_acuerdo="Recibirían permiso de forma general, sin ir caso a caso.",
         en_desacuerdo="Se seguiría yendo caso a caso, o sería más difícil conseguirlo.",
         posturas=[
             P(2, FA, 126, "Culminar la regularización extraordinaria de 2026", "por retrasos de la Administración."),
             P(2, POD, 67, "Establecimiento de un procedimiento permanente de regularización de las personas migrantes.", "de las personas migrantes."),
             P(-2, PP, 19, "PROHIBIREMOS POR LEY LAS REGULARIZACIONES MASIVAS E INDISCRIMINADAS", "SERÁ EXCEPCIONAL."),
             P(-2, VOX, 15, "Prohibición de las regularizaciones masivas.", "podrá regularizar su situación."),
         ]),
    dict(id="inm-2", tema="inmigracion", formulada_desde="PP/VOX",
         texto="Las ayudas sociales y la vivienda pública deberían ser primero para quienes tienen nacionalidad española.",
         contexto="Hoy, para la mayoría de ayudas y viviendas públicas cuenta lo que se gana y el tiempo que se lleva viviendo en el lugar, pero no la nacionalidad.",
         de_acuerdo="Tener la nacionalidad española daría prioridad.",
         en_desacuerdo="La nacionalidad seguiría sin contar.",
         posturas=[
             P(2, VOX, 19, "Acceso preferente de los españoles a vivienda pública", "prestaciones y servicios sociales."),
             P(-1, PP, 32, "Estos criterios se aplicarán dentro de los límites constitucionales y europeos", "exclusivamente en la nacionalidad.",
               nota="Propone dar prioridad según el arraigo y la cotización, pero no exclusivamente por nacionalidad."),
             P(-1, POD, 12, "impidiendo que se rechace a personas por su origen, nacionalidad", "situación administrativa", inferida=True,
               nota="Se refiere a la discriminación en el acceso al alquiler."),
             P(-1, FA, 126, "Suprimiremos trabas administrativas para el acceso efectivo a derechos", "empadronamiento flexible", inferida=True,
               nota="Propone facilitar el acceso a derechos a las personas migrantes, no priorizar por nacionalidad."),
         ]),
    dict(id="inm-3", tema="inmigracion", formulada_desde="PP/VOX",
         texto="Los menores extranjeros que llegan solos a España deberían, antes que nada, volver con su familia o a su país.",
         contexto="Hoy quedan al cuidado de las comunidades autónomas. Ya se les puede devolver con su familia o a su país, pero solo si se considera lo mejor para el menor.",
         de_acuerdo="Lo primero que se intentaría sería su vuelta.",
         en_desacuerdo="Se seguiría decidiendo caso a caso, o se facilitaría que se queden en España.",
         posturas=[
             P(2, PP, 20, "PROMOVEREMOS EL REGRESO DE LOS MENORES CON SUS FAMILIAS COMO OBJETIVO PRIORITARIO.", "OBJETIVO PRIORITARIO."),
             P(2, VOX, 15, "Devolución de menores extranjeros no acompañados", "a sus padres"),
             P(-1, POD, 65, "se garantizará la atención integral y regularización de los menores extranjeros no acompañados", "no acompañados", inferida=True,
               nota="Propone regularizar a estos menores en España, no su retorno."),
         ]),
    # ---------------- ENERGÍA Y MEDIO AMBIENTE ----------------
    dict(id="ene-1", tema="energia", formulada_desde="PP/VOX",
         texto="Las centrales nucleares deberían seguir funcionando más años de lo previsto.",
         contexto="Está previsto cerrar todas las centrales nucleares de España entre 2027 y 2035. La primera sería Almaraz (Cáceres), en 2027 y 2028.",
         de_acuerdo="Se retrasaría su cierre.",
         en_desacuerdo="Se cerrarían cuando está previsto, o antes.",
         posturas=[
             P(2, PP, 54, "ELIMINAREMOS EL CALENDARIO DE CIERRE", "COFRENTES Y TRILLO."),
             P(2, VOX, 12, "Se garantizará la supervivencia de las centrales nucleares actuales", "derogando el calendario de cierre."),
             P(-2, FA, 64, "Cumpliremos el calendario de cierre de las centrales nucleares.", "de las centrales nucleares."),
             P(-2, POD, 103, "Defenderemos el cumplimiento del calendario de cierre de las centrales nucleares", "comenzando por Almaraz"),
             P(-2, PSOE, 66, "Mantener el calendario de cierre de las centrales nucleares hasta 2035", "hasta 2035"),
         ]),
    dict(id="ene-2", tema="energia", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Las ciudades deberían prohibir o limitar la entrada de los coches que más contaminan.",
         contexto="Son las «zonas de bajas emisiones». La ley ya obliga a crearlas a los municipios de más de 50.000 habitantes. Que un coche pueda entrar depende de su etiqueta ambiental de la DGT.",
         de_acuerdo="Estas zonas se mantendrían o se ampliarían.",
         en_desacuerdo="Se eliminarían o dejarían de ser obligatorias.",
         posturas=[
             P(2, PSOE, 71, "Impulsar las Zonas de Bajas Emisiones y la movilidad sostenible en las ciudades", "en las ciudades"),
             P(2, POD, 95, "Implantar de forma acelerada las Zonas de Bajas Emisiones", "Zonas de Bajas Emisiones"),
             P(-2, VOX, 29, "Acabar con todas las imposiciones climáticas", "como la imposición de ZBE."),
         ]),
    # ---------------- MODELO TERRITORIAL ----------------
    dict(id="ter-1", tema="territorial", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="El Estado debería perdonar a las comunidades autónomas parte del dinero que le deben.",
         contexto="Desde 2012, el Estado ha prestado mucho dinero a las comunidades autónomas para pagar sus gastos, y muchas le deben grandes cantidades.",
         de_acuerdo="Esa parte de la deuda pasaría a ser del Estado.",
         en_desacuerdo="Cada comunidad seguiría debiendo todo lo que debe.",
         posturas=[
             P(2, PSOE, 61, "Avanzaremos en la asunción parcial por el Estado de 83.000 millones de euros de deuda autonómica", "de deuda autonómica"),
             P(2, FA, 104, "Condonación de deuda autonómica condicionada", "bajadas de impuestos a rentas altas."),
             P(-1, PP, 33, "Cada Comunidad responderá de sus decisiones y de su deuda.", "y de su deuda.",
               nota="El mismo punto propone una reestructuración multilateral de la deuda autonómica."),
         ]),
    dict(id="ter-2", tema="territorial", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Los diputados deberían poder hablar en catalán, euskera o gallego en el Congreso.",
         contexto="Ya pueden hacerlo desde 2023, con traducción simultánea.",
         de_acuerdo="Seguiría siendo así.",
         en_desacuerdo="En el Congreso se hablaría solo en castellano.",
         posturas=[
             P(2, PSOE, 91, "Consolidaremos el uso de las lenguas cooficiales en las Cortes Generales", "en las Cortes Generales"),
             P(1, FA, 141, "Aprobaremos una ley del plurilingüismo", "con las instituciones del Estado.", inferida=True,
               nota="Propone el uso de las lenguas cooficiales en las instituciones del Estado en general."),
             P(-2, PP, 37, "Propondremos la reforma del Reglamento de la Cámara", "lengua común de todos los españoles."),
         ]),
    dict(id="ter-3", tema="territorial", formulada_desde="PP/VOX",
         texto="Algunas comunidades autónomas deberían poder pactar con el Gobierno su propia forma de financiarse, distinta de la del resto.",
         contexto="Las comunidades pagan la sanidad, la educación y otros servicios sobre todo con impuestos que se reparten con reglas comunes. El País Vasco y Navarra tienen desde hace mucho un sistema propio: cobran sus impuestos y pagan al Estado una cantidad pactada. Otras, como Cataluña, piden algo parecido.",
         de_acuerdo="Otras comunidades, como Cataluña, podrían tener un sistema propio.",
         en_desacuerdo="Todas, salvo el País Vasco y Navarra, seguirían con las mismas reglas.",
         posturas=[
             P(-2, PP, 33, "Ninguna de las Comunidades que actualmente integran el régimen común saldrá de él", "al margen de este sistema."),
             P(1, FA, 103, "debe acomodar la voluntad de mayor autogobierno que han expresado algunas comunidades autónomas", "federalismo social y plurinacional.", inferida=True,
               nota="Propone que el modelo de financiación acoja la voluntad de más autogobierno de algunas comunidades."),
         ]),
    # ---------------- INSTITUCIONES Y JUSTICIA ----------------
    dict(id="ins-1", tema="instituciones", formulada_desde="PP/VOX",
         texto="Los propios jueces, y no el Congreso y el Senado, deberían elegir a la mayoría de los miembros del órgano que gobierna a los jueces.",
         contexto="Ese órgano es el Consejo General del Poder Judicial: decide nombramientos, ascensos y sanciones de los jueces. Tiene 20 miembros; 12 son jueces y hoy los eligen el Congreso y el Senado, con un acuerdo amplio entre partidos.",
         de_acuerdo="Esos 12 miembros los votarían los propios jueces.",
         en_desacuerdo="Los seguirían eligiendo el Congreso y el Senado.",
         posturas=[
             P(2, PP, 27, "Los jueces y magistrados de todas las categorías elegirán a los doce vocales judiciales", "del Consejo General del Poder Judicial."),
             P(2, VOX, 55, "Modificar la Ley Orgánica del Poder Judicial para que los doce vocales", "por y entre los propios jueces y magistrados"),
             P(-2, FA, 148, "Los vocales del turno judicial se seguirán eligiendo por mayoría de tres quintos", "por mayoría absoluta"),
         ]),
    dict(id="ins-2", tema="instituciones", formulada_desde="PP/VOX",
         texto="Deberían retirarse los monumentos y símbolos que homenajean la dictadura de Franco.",
         contexto="Hoy la ley ya obliga a retirarlos de calles y edificios públicos, aunque aún quedan algunos, como el Arco de la Victoria de Madrid.",
         de_acuerdo="Se seguirían retirando, también los que aún quedan.",
         en_desacuerdo="Dejaría de ser obligatorio retirarlos.",
         posturas=[
             P(2, POD, 137, "Retiraremos los símbolos, honores y reconocimientos franquistas", "exaltación de la dictadura"),
             P(2, PSOE, 98, "Ampliar la red de Lugares de Memoria Democrática, retirar simbología franquista", "retirar simbología franquista"),
             P(-1, PP, 37, "Derogaremos la mal llamada «ley de memoria democrática»", "«ley de memoria democrática»", inferida=True,
               nota="Propone derogar la ley de memoria democrática, que es la que obliga a retirar estos símbolos."),
             P(-1, VOX, 30, "Superación de las divisivas leyes ideológicas", "tratando de imponer una verdad oficial.", inferida=True,
               nota="Propone dejar atrás («superación») la ley de memoria democrática, que es la que obliga a retirar estos símbolos."),
         ]),
    dict(id="ins-3", tema="instituciones", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Insultar al Rey u ofender a España y a sus símbolos, como la bandera, debería seguir siendo delito.",
         contexto="Hoy son delito: se castigan con multas y, en algunos casos, con cárcel.",
         de_acuerdo="Seguirían castigándose, igual o con más dureza.",
         en_desacuerdo="Dejarían de ser delito.",
         posturas=[
             P(-2, FA, 142, "Derogaremos los artículos del Código Penal que castigan", "los delitos contra la Corona"),
             P(2, VOX, 56, "Las penas por las ofensas y ultrajes a España y sus símbolos o emblemas deben agravarse", "quede impune."),
             P(1, PP, 37, "Llevaremos a cabo una reforma legal que rehabilite y proteja los símbolos del Estado", "proteja los símbolos del Estado", inferida=True,
               nota="Propone reforzar la protección legal de los símbolos, sin mencionar el Código Penal."),
         ]),
    # ---------------- DERECHOS SOCIALES E IGUALDAD ----------------
    dict(id="der-1", tema="derechos", formulada_desde="PP/VOX",
         texto="Debería haber juzgados dedicados solo a la violencia contra las mujeres por parte de sus parejas o exparejas.",
         contexto="Existen desde 2005. Sus jueces están especializados en estos casos y pueden tomar medidas rápidas para proteger a la víctima, como una orden de alejamiento.",
         de_acuerdo="Estos juzgados se mantendrían o habría más.",
         en_desacuerdo="Estos casos los llevarían los juzgados de siempre, como cualquier otro delito.",
         posturas=[
             P(2, FA, 38, "Crearemos más Juzgados de Violencia sobre la Mujer", "Centros de Crisis 24 horas."),
             P(1, PSOE, 82, "Garantizar la valoración forense del riesgo en todos los juzgados de violencia sobre la mujer", "equipos multidisciplinares especializados.", inferida=True,
               nota="Propone reforzar estos juzgados."),
             P(1, POD, 54, "Ello implica revisar tanto las pruebas selectivas de especialización", "fiscalía contra la violencia sobre la mujer.", inferida=True,
               nota="Propone reforzar la especialización de estos juzgados y ampliarla a las violencias sexuales."),
             P(1, PP, 17, "Cada año rendiremos cuentas del cumplimiento del Pacto de Estado contra la Violencia de Género.", "contra la Violencia de Género.", inferida=True,
               nota="Se compromete con el Pacto de Estado contra la Violencia de Género, que incluye reforzar estos juzgados."),
             P(-1, VOX, 30, "Derogar las leyes que han criminalizado a los hombres y desprotegido a las mujeres.", "desprotegido a las mujeres.", inferida=True,
               nota="Propone derogar las leyes de violencia de género, que son las que crearon estos juzgados."),
         ]),
    dict(id="der-2", tema="derechos", formulada_desde="PP/VOX",
         texto="Las personas mayores de 16 años deberían poder cambiar el sexo de su DNI solo con pedirlo.",
         contexto="Es así desde 2023: no hacen falta informes médicos ni tratamientos. Para los menores de 16 hay requisitos adicionales.",
         de_acuerdo="Seguiría siendo así.",
         en_desacuerdo="Haría falta algo más que pedirlo, como antes de 2023, cuando se exigían informes médicos.",
         posturas=[
             P(-2, PP, 35, "eliminaremos la libre autodeterminación registral del sexo", "autodeterminación registral del sexo"),
             P(2, FA, 123, "autodeterminación de las personas trans, intersex y no binarias", "intersex y no binarias"),
             P(1, PSOE, 97, "Garantizar que la Ley 4/2023 sea el suelo común de derechos", "en toda España", inferida=True,
               nota="La Ley 4/2023 incluye la rectificación registral por declaración de la persona."),
             P(1, POD, 52, "El Estado debe reconocer todos sus derechos a las personas no binarias", "reconocerles su identidad.", inferida=True,
               nota="Propone reconocer la identidad declarada de las personas no binarias en los documentos oficiales."),
         ]),
    dict(id="der-3", tema="derechos", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="El derecho al aborto debería estar en la Constitución.",
         contexto="Hoy la mujer puede decidir abortar hasta la semana 14 de embarazo y, después, solo en algunos casos. Lo regula una ley normal, que el Parlamento puede cambiar por mayoría. En 2026 se empezó a reformar la Constitución para incluirlo, pero no se ha terminado.",
         de_acuerdo="Sería mucho más difícil cambiarlo o quitarlo en el futuro.",
         en_desacuerdo="Seguiría siendo más fácil de cambiar.",
         posturas=[
             P(2, PSOE, 81, "Blindar constitucionalmente el derecho a la interrupción voluntaria del embarazo.", "voluntaria del embarazo."),
             P(2, FA, 28, "Reformaremos el artículo 43 de la Constitución para incluir el derecho al aborto", "el derecho al aborto"),
             P(2, POD, 51, "Incorporar expresamente el derecho al aborto en la Constitución", "en la Constitución"),
             P(-1, VOX, 52, "Defensa del derecho a la vida desde su concepción hasta la muerte natural", "fin de la cultura de la muerte.", inferida=True,
               nota="Defender la vida «desde su concepción» se entiende contrario a reconocer el aborto como derecho constitucional."),
         ]),
    # ---------------- SEGURIDAD ----------------
    dict(id="seg-1", tema="seguridad", formulada_desde="PP/VOX",
         texto="Las multas por causar desórdenes en la calle, por ejemplo durante una protesta, deberían ser más altas.",
         contexto="Son multas que pone la Administración, sin pasar por un juez, cuando el hecho no llega a ser delito. Van desde 100 euros en los casos leves hasta decenas de miles en los más graves.",
         de_acuerdo="Subirían esas multas.",
         en_desacuerdo="Se quedarían igual o bajarían.",
         posturas=[
             P(2, PP, 16, "Elevaremos la multa mínima a 3.000 euros", "durante desórdenes multitudinarios"),
             P(-2, FA, 142, "Reduciremos las multas excesivas", "capacidad de ingresos de las personas sancionadas»"),
             P(-1, POD, 133, "Derogar la Ley Mordaza y reformar la legislación que limita los derechos fundamentales.", "los derechos fundamentales.", inferida=True,
               nota="Propone sustituir la ley que regula estas multas por una «regulación garantista»."),
         ]),
    dict(id="seg-2", tema="seguridad", formulada_desde="PP/VOX",
         texto="Las penas por causar disturbios violentos en la calle deberían ser más duras.",
         contexto="Hoy se castigan con entre 6 meses y 3 años de cárcel, y más en los casos graves.",
         de_acuerdo="Subirían esas penas.",
         en_desacuerdo="Se quedarían igual o bajarían.",
         posturas=[
             P(2, PP, 16, "Reformaremos el delito de desórdenes públicos", "por participar en disturbios violentos"),
             P(-1, FA, 142, "Reduciremos las multas excesivas", "«criterios de proporcionalidad»", inferida=True,
               nota="Dentro del apartado «Acabar con la criminalización de la protesta social»; se refiere a multas, no a penas por disturbios violentos."),
         ]),
    # ---------------- EXTERIOR Y DEFENSA ----------------
    dict(id="ext-1", tema="exterior", formulada_desde="PP/VOX",
         texto="España debería gastar más dinero en defensa (ejército y armamento).",
         contexto="En 2025 los países de la OTAN acordaron gastar el 5 % de su riqueza en defensa y seguridad de aquí a 2035. España consiguió quedar fuera de ese objetivo.",
         de_acuerdo="Subiría el gasto militar.",
         en_desacuerdo="Se quedaría igual o bajaría.",
         posturas=[
             P(2, VOX, 47, "Aumento de la inversión en Defensa", "Aumento de la inversión en Defensa"),
             P(1, PP, 21, "La Defensa será una verdadera política de Estado", "cumplir nuestros compromisos internacionales.", inferida=True,
               nota="Cumplir los compromisos internacionales de gasto implica aumentarlo."),
             P(-1, PSOE, 105, "rechazando el aumento del gasto militar al 5% del PIB", "nuestro Estado del bienestar.",
               nota="Rechaza el objetivo del 5 % del PIB, no cualquier aumento."),
             P(-2, FA, 130, "Reducción del gasto militar y rechazo al objetivo de la OTAN", "Reducción del gasto militar y rechazo al objetivo de la OTAN"),
             P(-2, POD, 28, "Revertiremos en los Presupuestos Generales del Estado el mayor aumento del gasto militar", "de la historia de la democracia"),
         ]),
    dict(id="ext-2", tema="exterior", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="España debería salir de la OTAN.",
         contexto="La OTAN es una alianza militar de Estados Unidos, Canadá y la mayoría de países europeos: si atacan a uno, los demás se comprometen a defenderlo. España está dentro desde 1982.",
         de_acuerdo="España dejaría la alianza.",
         en_desacuerdo="España seguiría en ella.",
         posturas=[
             P(2, POD, 28, "Impulsaremos la salida de España de la OTAN", "del Tratado del Atlántico Norte"),
             P(-2, PP, 21, "Reforzaremos cuando sea necesario los contingentes españoles de la OTAN", "de la OTAN"),
             P(-1, PSOE, 105, "Somos aliados, no vasallos.", "no vasallos.", inferida=True,
               nota="Se presenta como aliado dentro de la OTAN."),
         ]),
    dict(id="ext-3", tema="exterior", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="España debería romper relaciones con Israel: cerrar su embajada y dejar de comerciar con ese país.",
         contexto="España reconoció a Palestina en 2024 y en 2025 prohibió comprar y vender armas a Israel, pero mantiene relaciones con los dos países.",
         de_acuerdo="Se cerraría la embajada y se cortaría el comercio con Israel.",
         en_desacuerdo="Se mantendrían la embajada y el comercio.",
         posturas=[
             P(2, POD, 34, "Ruptura de las relaciones diplomáticas, culturales y comerciales con Israel.", "comerciales con Israel."),
             P(1, FA, 132, "suspensión efectiva del Acuerdo de Asociación UE-Israel", "Acuerdo de Asociación UE-Israel",
               nota="Propone suspender el acuerdo comercial UE-Israel y un embargo de armas, no la ruptura diplomática."),
             P(-1, PP, 57, "Impulsaremos soluciones diplomáticas para la resolución de conflictos", "países árabes de la región.", inferida=True,
               nota="Considera a Israel un socio clave."),
         ]),
    dict(id="ext-4", tema="exterior", formulada_desde="PP/VOX",
         texto="España debería seguir enviando ayuda militar a Ucrania.",
         contexto="Desde que Rusia invadió Ucrania en 2022, España le envía armas y material militar, además de ayuda económica y humanitaria.",
         de_acuerdo="Seguiría enviándola.",
         en_desacuerdo="Dejaría de enviar ayuda militar (no la económica ni la humanitaria).",
         posturas=[
             P(2, PP, 56, "Mantendremos el apoyo político, económico, militar y humanitario a Ucrania", "mientras dure su agresión."),
             P(1, PSOE, 88, "con Ucrania frente a Putin", "con Ucrania frente a Putin", inferida=True, nota=LOGRO),
             P(-1, POD, 37, "Defenderemos una solución diplomática y negociada al conflicto de Ucrania", "impulsando un alto el fuego", inferida=True,
               nota="Propone una solución negociada; no menciona expresamente el apoyo militar."),
         ]),
]

TEMAS = [
    ("vivienda", "Vivienda"), ("fiscalidad", "Impuestos"), ("empleo", "Empleo"), ("pensiones", "Pensiones"),
    ("sanidad", "Sanidad"), ("educacion", "Educación"), ("inmigracion", "Inmigración"),
    ("energia", "Energía y medio ambiente"), ("territorial", "Comunidades autónomas"),
    ("instituciones", "Instituciones y justicia"), ("derechos", "Derechos sociales e igualdad"),
    ("seguridad", "Seguridad"), ("exterior", "Exterior y defensa"),
]
NOMBRES = {FA: "Frente Amplio", POD: "Podemos", PP: "PP", PSOE: "PSOE", VOX: "Vox"}

# --- Ensamblar preguntas.json ---
salida = []
for q in PREGUNTAS:
    pos = {p: {"valor": None, "cita": None, "pagina": None, "inferida": False, "nota": None} for p in PARTIDOS}
    for x in q["posturas"]:
        pos[x["partido"]] = {k: x[k] for k in ("valor", "cita", "pagina", "inferida", "nota")}
    salida.append({k: q[k] for k in ("id", "tema", "texto", "contexto", "de_acuerdo", "en_desacuerdo", "formulada_desde")} | {"posturas": pos})

datos = {
    "version": "2026-11-19",
    "escala": {"-2": "Muy en contra", "-1": "En contra", "0": "Neutral", "1": "A favor", "2": "Muy a favor", "null": "No se pronuncia"},
    "partidos": [{"id": p, "nombre": NOMBRES[p], "pdf": f"{p}.pdf"} for p in PARTIDOS],
    "temas": [{"id": i, "nombre": n} for i, n in TEMAS],
    "preguntas": salida,
}

# --- Catálogo: propuestas citadas en las posturas + otras revisadas y no usadas ---
EXTRA = [
    (PP, "vivienda", 41, "CONSTRUIREMOS UN MILLÓN DE VIVIENDAS.", "CONSTRUIREMOS UN MILLÓN DE VIVIENDAS.", "Construir un millón de viviendas movilizando suelo público y privado."),
    (PP, "vivienda", 43, "EL OCUPA SALDRÁ EN 48 HORAS POR ORDEN JUDICIAL.", "desde el primer día.", "Ley para que el propietario recupere en 48 horas una vivienda ocupada."),
    (PSOE, "vivienda", 100, "desalojo de viviendas ocupadas en 48 horas", "desalojo de viviendas ocupadas en 48 horas", "Desalojo de viviendas ocupadas en 48 horas."),
    (VOX, "vivienda", 24, "Desalojo de la vivienda okupada en menos de 24 horas", "por su legítimo titular, el propietario.", "Desalojo de viviendas ocupadas en menos de 24 horas."),
    (VOX, "vivienda", 24, "Tipo 0% de IVA para la compra de tu primera vivienda habitual", "-de nueva construcción-", "IVA del 0 % en la compra de la primera vivienda nueva."),
    (PP, "vivienda", 43, "Reduciremos el IVA de la compra de primera vivienda del 10% al 4%", "para menores de 40 años", "IVA del 4 % en la compra de la primera vivienda para menores de 40 años."),
    (POD, "vivienda", 10, "Impuesto para las viviendas vacías.", "Impuesto para las viviendas vacías.", "Crear un impuesto sobre las viviendas vacías."),
    (FA, "vivienda", 12, "Tramitaremos la extinción progresiva y definitiva de todas las licencias de Viviendas de Uso Turístico (VUT)", "dentro de las zonas tensionadas", "Extinguir en tres años las licencias de pisos turísticos en zonas tensionadas."),
    (PP, "fiscalidad", 47, "aplicaremos un IVA del 0% a los alimentos básicos", "las conservas.", "IVA del 0 % para los alimentos básicos mientras dure la crisis de inflación."),
    (PSOE, "fiscalidad", 49, "Reforzar la tasa Tobin aumentando el tipo impositivo del 0,2% al 0,4%.", "del 0,2% al 0,4%.", "Subir el impuesto sobre transacciones financieras del 0,2 % al 0,4 %."),
    (FA, "empleo", 7, "blindaremos por ley un Salario Mínimo Interprofesional", "del salario medio neto", "Fijar por ley el SMI en el 60 % del salario medio neto."),
    (POD, "empleo", 41, "Aumentaremos el SMI hasta los 1.800 euros al mes", "en una legislatura", "Subir el SMI a 1.800 euros mensuales en la legislatura."),
    (PSOE, "empleo", 41, "Recuperar los salarios de tramitación", "en los supuestos legalmente establecidos", "Recuperar los salarios de tramitación en los despidos."),
    (PP, "empleo", 46, "Los nuevos autónomos no pagarán cuota a la Seguridad Social durante su primer año", "durante su primer año", "Cuota cero para los nuevos autónomos el primer año."),
    (VOX, "empleo", 9, "Cuota de cero euros si los ingresos no llegan al Salario Mínimo Interprofesional", "al Salario Mínimo Interprofesional", "Cuota cero para autónomos con ingresos inferiores al SMI."),
    (PP, "pensiones", 34, "Aseguraremos que mantengan su poder adquisitivo y suban cada año con el IPC.", "con el IPC.", "Revalorizar las pensiones cada año con el IPC."),
    (PSOE, "pensiones", 40, "Blindar constitucionalmente el sistema público de pensiones y su revalorización conforme al IPC", "conforme al IPC", "Blindar en la Constitución la revalorización de las pensiones con el IPC."),
    (PP, "pensiones", 34, "Incentivaremos la jubilación activa mediante deducciones en el IRPF.", "deducciones en el IRPF.", "Deducciones en el IRPF para quien compatibilice pensión y trabajo."),
    (PSOE, "sanidad", 49, "Incorporaremos progresivamente a la sanidad pública los tratamientos básicos", "para toda la población adulta", "Incorporar la salud bucodental básica de adultos a la sanidad pública."),
    (PP, "educacion", 44, "LA ESCUELA INFANTIL DE CERO A TRES AÑOS SERÁ GRATUITA.", "SERÁ GRATUITA.", "Escuela infantil de 0 a 3 años gratuita."),
    (VOX, "educacion", 51, "la gratuidad real de la educación infantil de 0 a 3 años.", "de 0 a 3 años.", "Educación infantil de 0 a 3 años gratuita."),
    (POD, "educacion", 83, "Suprimiremos la enseñanza de cualquier religión en cualquier colegio.", "en cualquier colegio.", "Suprimir la enseñanza de la religión en todos los colegios."),
    (PP, "inmigracion", 19, "Prohibiremos el uso del burka y el niqab en los espacios públicos.", "en los espacios públicos.", "Prohibir el burka y el niqab en espacios públicos."),
    (VOX, "inmigracion", 42, "Prohibición del burka y el niqab en todos los espacios públicos", "en todos los espacios públicos", "Prohibir el burka y el niqab en espacios públicos."),
    (VOX, "inmigracion", 19, "Gravamen sobre las remesas al extranjero.", "Gravamen sobre las remesas al extranjero.", "Impuesto sobre el dinero que se envía al extranjero."),
    (PP, "seguridad", 17, "AMPLIAREMOS LA PRISIÓN PERMANENTE REVISABLE", "Y A LOS DEPREDADORES SEXUALES.", "Ampliar la prisión permanente revisable a más delitos."),
    (VOX, "seguridad", 45, "Ampliación de la prisión permanente revisable.", "Ampliación de la prisión permanente revisable.", "Ampliar la prisión permanente revisable."),
    (VOX, "seguridad", 45, "Reducción de la edad de responsabilidad penal del menor", "Reducción de la edad de responsabilidad penal del menor", "Rebajar la edad de responsabilidad penal."),
    (POD, "seguridad", 133, "que incluya expresamente la prohibición del uso de pelotas de goma", "pelotas de goma", "Prohibir el uso policial de pelotas de goma."),
    (PP, "territorial", 15, "Recuperaremos en el Código Penal el delito de sedición", "el delito de sedición", "Recuperar el delito de sedición."),
    (VOX, "territorial", 56, "Ilegalización de los partidos políticos, asociaciones u organizaciones", "su unidad e integridad territorial.", "Ilegalizar las organizaciones que atenten contra la unidad de España."),
    (FA, "territorial", 8, "proponemos avanzar hacia una República Federal y Plurinacional", "República Federal y Plurinacional", "Avanzar hacia una república federal y plurinacional."),
    (POD, "instituciones", 128, "que la ciudadanía decida de forma separada y directa entre monarquía y república", "entre monarquía y república", "Referéndum para elegir entre monarquía y república."),
    (PP, "instituciones", 25, "Derogaremos la Ley de Amnistía", "Derogaremos la Ley de Amnistía", "Derogar la Ley de Amnistía."),
    (PP, "instituciones", 26, "Promoveremos las reformas necesarias para que una segunda prórroga consecutiva", "la convocatoria de elecciones.", "Elecciones obligatorias tras dos prórrogas presupuestarias seguidas."),
    (POD, "energia", 19, "Garantizaremos la gratuidad de todo el transporte público de viajeros", "de todo el transporte público de viajeros", "Transporte público gratuito."),
    (FA, "energia", 71, "Aplicaremos la retirada de nuevas calderas fósiles desde 2027", "desde 2027", "Retirar las nuevas calderas de combustibles fósiles desde 2027."),
    (POD, "exterior", 28, "Salida de la OTAN y cierre de las bases militares estadounidenses de Rota y Morón.", "de Rota y Morón.", "Cerrar las bases militares estadounidenses de Rota y Morón."),
    (FA, "exterior", 131, "Aprobaremos una ley específica de embargo integral de armas a Israel", "de armas a Israel", "Ley de embargo integral de armas a Israel."),
    (PSOE, "derechos", 97, "Culminar la reforma del Código Penal para penalizar las llamadas «terapias de conversión»", "«terapias de conversión»", "Castigar penalmente las llamadas terapias de conversión."),
    (PP, "derechos", 35, "Garantizaremos que el sexo biológico sea el criterio para las categorías deportivas femeninas.", "deportivas femeninas.", "Sexo biológico como criterio para las categorías deportivas femeninas."),
    (VOX, "derechos", 43, "Compromiso con la defensa del deporte femenino", "criterios biológicos", "Criterios biológicos en el deporte femenino."),
]

ETIQ = {2: "Muy a favor", 1: "A favor", 0: "Neutral", -1: "En contra", -2: "Muy en contra"}
catalogo = {p: [] for p in PARTIDOS}
for q in PREGUNTAS:
    for x in q["posturas"]:
        res = f"{ETIQ[x['valor']]} de: «{q['texto']}»" + (" (postura inferida)" if x["inferida"] else "")
        catalogo[x["partido"]].append({"tema": q["tema"], "resumen": res, "cita_literal": x["cita"], "pagina": x["pagina"], "usada_en": q["id"]})
for partido, tema, pag, ini, fin, res in EXTRA:
    catalogo[partido].append({"tema": tema, "resumen": res, "cita_literal": cita(partido, pag, ini, fin), "pagina": pag, "usada_en": None})

if ERRORES:
    print("\n".join(ERRORES))
    sys.exit(1)

(RAIZ / "data" / "catalogo").mkdir(parents=True, exist_ok=True)
orden = [t for t, _ in TEMAS]
for p, items in catalogo.items():
    items.sort(key=lambda e: (orden.index(e["tema"]), e["pagina"]))
    (RAIZ / "data" / "catalogo" / f"{p}.json").write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("catálogo:", {p: len(v) for p, v in catalogo.items()})

(RAIZ / "data" / "preguntas.json").write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"{len(salida)} preguntas")
from collections import Counter
print(Counter(q["formulada_desde"] for q in salida))
print(Counter(q["tema"] for q in salida))
for p in PARTIDOS:
    n = sum(1 for q in salida if q["posturas"][p]["valor"] is not None)
    inf = sum(1 for q in salida if q["posturas"][p]["inferida"])
    print(f"{p:14} se pronuncia en {n}/{len(salida)} (inferidas: {inf})")
