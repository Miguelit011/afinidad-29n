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
         texto="Debería haber por ley un precio máximo para los alquileres en las zonas donde alquilar una vivienda se ha vuelto muy caro.",
         contexto="La ley de vivienda de 2023 ya permite poner ese tope, pero solo en las zonas que su comunidad autónoma declare «tensionadas», es decir, con alquileres muy caros o que suben mucho. Cada comunidad decide si lo hace.",
         posturas=[
             P(2, FA, 13, "Limitaremos por ley el precio del alquiler", "en todas las zonas tensionadas"),
             P(2, POD, 8, "Bajar los alquileres un 40% por ley.", "de los precios del alquiler"),
             P(1, PSOE, 30, "Congelar temporalmente las rentas", "en los mercados tensionados."),
             P(-2, PP, 42, "Eliminaremos las zonas tensionadas", "menos oferta en el mercado del alquiler."),
             P(-1, VOX, 23, "Recuperar la seguridad jurídica y una oferta de alquileres", "Derogación de la Ley de Vivienda.", inferida=True,
               nota="La Ley de Vivienda es la norma que permite limitar el alquiler en zonas tensionadas; el programa propone derogarla."),
         ]),
    dict(id="viv-2", tema="vivienda", formulada_desde="PP/VOX",
         texto="Debería eliminarse la ley de vivienda aprobada en 2023.",
         contexto="Es la ley que permite poner un tope al alquiler en las zonas más caras y que da más protección frente a los desahucios a las familias vulnerables. Si se elimina, esas normas dejarían de aplicarse.",
         posturas=[
             P(2, PP, 42, "DEROGAREMOS LA LEY DE VIVIENDA.", "propietarios e inquilinos."),
             P(2, VOX, 23, "Recuperar la seguridad jurídica y una oferta de alquileres", "Derogación de la Ley de Vivienda."),
             P(-1, PSOE, 24, "En 2023, aprobamos la primera Ley por el Derecho a la Vivienda", "de la democracia", nota=LOGRO),
             P(-1, FA, 14, "La declaración de Zona de Mercado Residencial Tensionado (ZMRT) será obligatoria y automática", "establecidos en la Ley de Vivienda", inferida=True,
               nota="Propone aplicar de forma obligatoria mecanismos de la Ley de Vivienda, lo que supone mantenerla."),
         ]),
    # ---------------- FISCALIDAD ----------------
    dict(id="fis-1", tema="fiscalidad", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Las personas que más ganan deberían pagar más impuestos por sus ingresos.",
         contexto="Cada año se paga un impuesto por lo que se gana (el IRPF, el de la declaración de la renta). Cuanto más se gana, mayor es el porcentaje que se paga. Hoy, por la parte más alta de los ingresos se paga entre el 45 % y el 54 %, según la comunidad autónoma.",
         posturas=[
             P(2, POD, 21, "Reforma del IRPF para que las rentas más altas contribuyan más.", "contribuyan más."),
             P(2, FA, 46, "Ampliaremos el número de tramos del IRPF", "para rentas a partir de 300.000 euros."),
             P(1, PSOE, 48, "Introducir progresividad a la imposición del capital.", "rentas de capital más elevadas.",
               nota="Solo se refiere a las rentas del capital, no a las del trabajo."),
             P(-1, VOX, 9, "Reforma del sistema de tributación sobre la renta (IRPF).", "Simplificación y bajada del IRPF.", inferida=True,
               nota="Propone bajar el IRPF con carácter general, sin referirse expresamente a las rentas altas."),
         ]),
    dict(id="fis-2", tema="fiscalidad", formulada_desde="PP/VOX",
         texto="Las empresas deberían pagar menos impuestos por sus beneficios.",
         contexto="Las empresas pagan un impuesto por lo que ganan (el Impuesto sobre Sociedades). Hoy es, en general, el 25 % de sus beneficios, y algo menos para las empresas pequeñas.",
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
         texto="Las grandes fortunas deberían pagar un impuesto estatal, igual en toda España, que ninguna comunidad autónoma pueda quitar.",
         contexto="El patrimonio es todo lo que tiene una persona: casas, dinero, acciones… El impuesto sobre el patrimonio lo gestionan las comunidades autónomas, y algunas en la práctica no lo cobran. Desde 2022 existe además un impuesto estatal para las grandes fortunas, que se aprobó como temporal.",
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
         texto="La jornada laboral máxima debería bajar por ley a 35 horas a la semana o menos, sin que baje el sueldo.",
         contexto="Hoy el máximo legal es de 40 horas a la semana (de media a lo largo del año). Se ha propuesto bajarlo a 37,5 horas, pero no se ha aprobado.",
         posturas=[
             P(2, POD, 41, "Reduciremos la jornada laboral a 30 horas semanales", "comenzando con una bajada a 35 horas"),
             P(2, FA, 7, "Avanzaremos hacia la jornada laboral máxima de 32 horas semanales", "sin reducción salarial"),
             P(1, PSOE, 41, "Completar la reducción de la jornada a 37,5 horas", "hacia las 35 horas.",
               nota="Por ley hasta 37,5 horas; las 35 horas, mediante la negociación colectiva."),
         ]),
    dict(id="emp-2", tema="empleo", formulada_desde="PP/VOX",
         texto="Debería eliminarse la reforma laboral de 2021.",
         contexto="Esa reforma limitó los contratos temporales para que hubiera más contratos fijos. También dio más peso a los convenios de cada sector: los acuerdos sobre sueldos y condiciones de trabajo que firman sindicatos y empresarios.",
         posturas=[
             P(1, VOX, 13, "Derogar la legislación laboral de Sánchez", "agravado la precariedad", inferida=True,
               nota="Se entiende que «la legislación laboral de Sánchez» incluye la reforma laboral de 2021."),
             P(-1, PSOE, 36, "Con la reforma laboral, España ha alcanzado los 22,8 millones de ocupados", "por primera vez en 17 años", nota=LOGRO),
             P(-1, FA, 54, "A pesar de que la reforma laboral ha dado lugar", "de empleo estable", inferida=True,
               nota="Valora positivamente la reforma, sin un compromiso expreso sobre ella."),
         ]),
    # ---------------- PENSIONES ----------------
    dict(id="pen-1", tema="pensiones", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="La pensión más baja que cobra quien ha trabajado y cotizado debería ser igual al salario mínimo.",
         contexto="Hoy esa pensión mínima es más baja que el salario mínimo interprofesional, que es lo menos que se puede pagar por ley por una jornada completa. El Gobierno lo fija cada año.",
         posturas=[
             P(2, FA, 57, "Blindaje constitucional del carácter público de las pensiones", "pensión mínima igual al SMI"),
             P(2, POD, 44, "Equiparar la pensión mínima al salario mínimo interprofesional.", "se equipare al SMI"),
             P(1, PSOE, 39, "culminando el proceso de convergencia de las cuantías de las pensiones mínimas", "del conjunto de la sociedad.",
               nota="Propone acercar las pensiones mínimas a «estándares de ingresos», sin fijar el SMI como referencia."),
         ]),
    # ---------------- SANIDAD ----------------
    dict(id="san-1", tema="sanidad", formulada_desde="PP/VOX",
         texto="La sanidad pública debería pagar a clínicas privadas para que atiendan a sus pacientes y así reducir las listas de espera.",
         contexto="Ya se hace en muchas comunidades autónomas: la sanidad pública paga a un centro privado para que opere o atienda a pacientes que están esperando. El paciente no paga nada.",
         posturas=[
             P(2, VOX, 37, "Fomento de la colaboración público-privada", "a reducir demoras"),
             P(-1, PSOE, 49, "Limitar la privatización de la sanidad", "en la prestación sanitaria."),
             P(-2, FA, 26, "Derogaremos expresamente la Ley 15/1997", "colaboración con entidades privadas"),
             P(-2, POD, 88, "Acabar con la privatización y recuperar la sanidad para lo público.", "para lo público."),
         ]),
    dict(id="san-2", tema="sanidad", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Las personas inmigrantes sin permiso de residencia («sin papeles») deberían poder usar la sanidad pública igual que el resto de personas que viven en España.",
         contexto="Desde 2018 la ley les reconoce el derecho a la sanidad pública, pero con algunos requisitos que no se piden al resto.",
         posturas=[
             P(2, FA, 26, "Blindaremos por ley la universalidad de la atención sanitaria", "independientemente de su estatus administrativo."),
             P(2, POD, 69, "incluidas las personas migrantes en situación administrativa irregular", "que impiden recibir atención"),
             P(1, PSOE, 46, "En sanidad, devolvimos la universalidad al Sistema Nacional de Salud", "al Sistema Nacional de Salud", inferida=True,
               nota=LOGRO + " Se entiende que «universalidad» incluye a las personas en situación irregular."),
             P(-2, VOX, 19, "Garantizar la sostenibilidad del sistema sanitario", "salvo casos de urgencia grave."),
         ]),
    # ---------------- EDUCACIÓN ----------------
    dict(id="edu-1", tema="educacion", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Debería reducirse poco a poco el dinero público que reciben los colegios concertados.",
         contexto="Hay colegios públicos, privados y concertados. Los concertados son de propiedad privada, pero reciben dinero público y, a cambio, las clases son gratuitas en la enseñanza obligatoria.",
         posturas=[
             P(2, POD, 79, "Avanzaremos hacia una única red educativa de gestión pública directa", "para financiar negocios privados."),
             P(-2, PP, 51, "LOS PADRES ELEGIRÁN COLEGIO, Y NINGÚN CONCIERTO EDUCATIVO SE ELIMINARÁ", "DEMANDA SUFICIENTE."),
             P(-1, VOX, 41, "Garantizar la libre elección de centro educativo en todos los niveles", "sea un impedimento para ello.", inferida=True,
               nota="La libre elección de centro sin barreras económicas supone mantener la red concertada."),
         ]),
    dict(id="edu-2", tema="educacion", formulada_desde="PP/VOX",
         texto="En todas las comunidades autónomas, los alumnos deberían tener garantizado poder recibir las clases en castellano.",
         contexto="En las comunidades con otra lengua oficial (catalán, valenciano, euskera, gallego…), cada comunidad decide cuántas clases se dan en cada lengua. En Cataluña, por ejemplo, la mayoría de las clases se dan en catalán (lo que se llama «inmersión lingüística»).",
         posturas=[
             P(2, PP, 32, "Garantizaremos el derecho constitucional de recibir enseñanza en castellano", "y en toda la Nación"),
             P(2, VOX, 41, "Se garantizará la educación en español en todo el territorio nacional.", "en todo el territorio nacional."),
             P(-1, FA, 32, "Lanzaremos un Plan Estatal para el aprendizaje y divulgación de las lenguas cooficiales", "como lengua vehicular en Cataluña.", inferida=True,
               nota="Defiende la inmersión en catalán, lo que choca con garantizar la enseñanza en castellano en toda España."),
         ]),
    dict(id="edu-3", tema="educacion", formulada_desde="PP/VOX",
         texto="Debería cambiarse la ley de educación actual (la LOMLOE) por una ley nueva.",
         contexto="La LOMLOE, de 2020, es la ley que marca hoy cómo funcionan colegios e institutos: qué se estudia, cuándo se puede pasar de curso con asignaturas suspendidas o cuánto cuenta la asignatura de religión.",
         posturas=[
             P(2, PP, 51, "Acordaremos con docentes, inspectores, expertos y familias un nuevo marco educativo", "que sustituya a la LOMLOE."),
             P(2, VOX, 41, "Derogación de la LOMLOE", "basada en el esfuerzo"),
             P(-1, FA, 41, "Impulsaremos una reforma de la LOMLOE", "como competencia clave", inferida=True,
               nota="Propone reformar la LOMLOE, no sustituirla."),
         ]),
    # ---------------- INMIGRACIÓN ----------------
    dict(id="inm-1", tema="inmigracion", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Debería darse permiso para vivir y trabajar en España, de forma general, a las personas inmigrantes que ya viven aquí sin papeles.",
         contexto="La vía habitual es caso a caso: por ejemplo, demostrar que se lleva años en España y se tiene trabajo o familia aquí (lo que se llama «arraigo»). En 2026 se abrió además un proceso extraordinario para que muchas personas pudieran pedirlo a la vez.",
         posturas=[
             P(2, FA, 126, "Culminar la regularización extraordinaria de 2026", "por retrasos de la Administración."),
             P(2, POD, 67, "Establecimiento de un procedimiento permanente de regularización de las personas migrantes.", "de las personas migrantes."),
             P(-2, PP, 19, "PROHIBIREMOS POR LEY LAS REGULARIZACIONES MASIVAS E INDISCRIMINADAS", "SERÁ EXCEPCIONAL."),
             P(-2, VOX, 15, "Prohibición de las regularizaciones masivas.", "podrá regularizar su situación."),
         ]),
    dict(id="inm-2", tema="inmigracion", formulada_desde="PP/VOX",
         texto="Las ayudas sociales y la vivienda pública deberían dar prioridad a las personas con nacionalidad española.",
         contexto="Hoy, para la mayoría de ayudas y para las viviendas públicas se tiene en cuenta lo que se gana y el tiempo que se lleva viviendo en el lugar, pero no la nacionalidad.",
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
         texto="Los menores extranjeros que llegan solos a España deberían, como primera opción, volver con su familia o a su país.",
         contexto="Hoy quedan a cargo de las comunidades autónomas, que se ocupan de su cuidado. La ley ya permite devolverlos con su familia o a su país, pero solo si se considera que es lo mejor para el menor.",
         posturas=[
             P(2, PP, 20, "PROMOVEREMOS EL REGRESO DE LOS MENORES CON SUS FAMILIAS COMO OBJETIVO PRIORITARIO.", "OBJETIVO PRIORITARIO."),
             P(2, VOX, 15, "Devolución de menores extranjeros no acompañados", "a sus padres"),
             P(-1, POD, 65, "se garantizará la atención integral y regularización de los menores extranjeros no acompañados", "no acompañados", inferida=True,
               nota="Propone regularizar a estos menores en España, no su retorno."),
         ]),
    # ---------------- ENERGÍA Y MEDIO AMBIENTE ----------------
    dict(id="ene-1", tema="energia", formulada_desde="PP/VOX",
         texto="Las centrales nucleares deberían seguir funcionando más años de lo que está previsto.",
         contexto="El calendario acordado en 2019 prevé cerrar todas las centrales nucleares de España entre 2027 y 2035. La primera sería Almaraz (Cáceres), en 2027 y 2028.",
         posturas=[
             P(2, PP, 54, "ELIMINAREMOS EL CALENDARIO DE CIERRE", "COFRENTES Y TRILLO."),
             P(2, VOX, 12, "Se garantizará la supervivencia de las centrales nucleares actuales", "derogando el calendario de cierre."),
             P(-2, FA, 64, "Cumpliremos el calendario de cierre de las centrales nucleares.", "de las centrales nucleares."),
             P(-2, POD, 103, "Defenderemos el cumplimiento del calendario de cierre de las centrales nucleares", "comenzando por Almaraz"),
             P(-2, PSOE, 66, "Mantener el calendario de cierre de las centrales nucleares hasta 2035", "hasta 2035"),
         ]),
    dict(id="ene-2", tema="energia", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Las ciudades deberían limitar la entrada de los coches y otros vehículos que más contaminan.",
         contexto="Son las llamadas «zonas de bajas emisiones»: los vehículos más contaminantes, según su etiqueta ambiental de la DGT, no pueden entrar o solo pueden hacerlo con limitaciones. La ley ya obliga a crearlas a los municipios de más de 50.000 habitantes.",
         posturas=[
             P(2, PSOE, 71, "Impulsar las Zonas de Bajas Emisiones y la movilidad sostenible en las ciudades", "en las ciudades"),
             P(2, POD, 95, "Implantar de forma acelerada las Zonas de Bajas Emisiones", "Zonas de Bajas Emisiones"),
             P(-2, VOX, 29, "Acabar con todas las imposiciones climáticas", "como la imposición de ZBE."),
         ]),
    # ---------------- MODELO TERRITORIAL ----------------
    dict(id="ter-1", tema="territorial", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="El Estado debería perdonar a las comunidades autónomas una parte del dinero que le deben.",
         contexto="Desde 2012, el Estado ha prestado mucho dinero a las comunidades autónomas para que pudieran pagar sus gastos, y muchas le deben grandes cantidades. Si se perdona una parte, esa deuda pasaría a ser del Estado.",
         posturas=[
             P(2, PSOE, 61, "Avanzaremos en la asunción parcial por el Estado de 83.000 millones de euros de deuda autonómica", "de deuda autonómica"),
             P(2, FA, 104, "Condonación de deuda autonómica condicionada", "bajadas de impuestos a rentas altas."),
             P(-1, PP, 33, "Cada Comunidad responderá de sus decisiones y de su deuda.", "y de su deuda.",
               nota="El mismo punto propone una reestructuración multilateral de la deuda autonómica."),
         ]),
    dict(id="ter-2", tema="territorial", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Los diputados deberían poder hablar en catalán, euskera o gallego en el Congreso.",
         contexto="Ya pueden hacerlo desde 2023, con traducción simultánea. Estar en desacuerdo significa que en el Congreso se hable solo en castellano.",
         posturas=[
             P(2, PSOE, 91, "Consolidaremos el uso de las lenguas cooficiales en las Cortes Generales", "en las Cortes Generales"),
             P(1, FA, 141, "Aprobaremos una ley del plurilingüismo", "con las instituciones del Estado.", inferida=True,
               nota="Propone el uso de las lenguas cooficiales en las instituciones del Estado en general."),
             P(-2, PP, 37, "Propondremos la reforma del Reglamento de la Cámara", "lengua común de todos los españoles."),
         ]),
    dict(id="ter-3", tema="territorial", formulada_desde="PP/VOX",
         texto="Todas las comunidades autónomas que hoy se financian con las mismas reglas deberían seguir así: ninguna debería pactar por su cuenta con el Gobierno un sistema propio.",
         contexto="Las comunidades autónomas pagan la sanidad, la educación y otros servicios sobre todo con impuestos que se reparten con unas reglas comunes. El País Vasco y Navarra tienen desde hace mucho un sistema propio: recaudan sus impuestos y pagan al Estado una cantidad pactada. Otras comunidades, como Cataluña, piden un sistema propio.",
         posturas=[
             P(2, PP, 33, "Ninguna de las Comunidades que actualmente integran el régimen común saldrá de él", "al margen de este sistema."),
             P(-1, FA, 103, "debe acomodar la voluntad de mayor autogobierno que han expresado algunas comunidades autónomas", "federalismo social y plurinacional.", inferida=True,
               nota="Propone que el modelo de financiación acoja la voluntad de más autogobierno de algunas comunidades."),
         ]),
    # ---------------- INSTITUCIONES Y JUSTICIA ----------------
    dict(id="ins-1", tema="instituciones", formulada_desde="PP/VOX",
         texto="Los 12 jueces que forman parte del Consejo General del Poder Judicial deberían ser elegidos por los propios jueces, y no por el Congreso y el Senado.",
         contexto="El Consejo General del Poder Judicial (CGPJ) es el órgano que gobierna a los jueces: decide sus nombramientos, ascensos y sanciones. Tiene 20 miembros. Hoy los 12 que son jueces los eligen el Congreso y el Senado, con un acuerdo amplio entre partidos (tres quintos de los votos).",
         posturas=[
             P(2, PP, 27, "Los jueces y magistrados de todas las categorías elegirán a los doce vocales judiciales", "del Consejo General del Poder Judicial."),
             P(2, VOX, 55, "Modificar la Ley Orgánica del Poder Judicial para que los doce vocales", "por y entre los propios jueces y magistrados"),
             P(-2, FA, 148, "Los vocales del turno judicial se seguirán eligiendo por mayoría de tres quintos", "por mayoría absoluta"),
         ]),
    dict(id="ins-2", tema="instituciones", formulada_desde="PP/VOX",
         texto="Debería eliminarse la Ley de Memoria Democrática.",
         contexto="Es una ley de 2022 sobre las víctimas de la Guerra Civil y de la dictadura de Franco. Entre otras cosas, ayuda a localizar e identificar a desaparecidos enterrados en fosas comunes, reconoce a las víctimas y obliga a retirar los símbolos que ensalzan la dictadura.",
         posturas=[
             P(2, PP, 37, "Derogaremos la mal llamada «ley de memoria democrática»", "«ley de memoria democrática»"),
             P(1, VOX, 30, "Superación de las divisivas leyes ideológicas", "tales como la de Memoria Democrática", inferida=True,
               nota="Se entiende que «superación» equivale a derogación."),
             P(-2, FA, 146, "Desarrollo reglamentario de la Ley de Memoria Democrática", "de la dictadura franquista"),
             P(-1, PSOE, 98, "Con la Ley de Memoria Democrática las hemos situado en el centro de las políticas públicas.", "de las políticas públicas.", nota=LOGRO),
             P(-1, POD, 71, "Llevar a la práctica las propuestas de la Comisión de Memoria del Pueblo Gitano", "de la Ley de Memoria Democrática", inferida=True,
               nota="Propone aplicar disposiciones de la ley, lo que supone mantenerla."),
         ]),
    dict(id="ins-3", tema="instituciones", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Insultar al Rey o a la Familia Real, u ofender a España y a sus símbolos (como la bandera), debería dejar de ser delito.",
         contexto="Hoy el Código Penal castiga estas conductas con multas y, en algunos casos, con cárcel. Estar en desacuerdo significa que sigan siendo delito.",
         posturas=[
             P(2, FA, 142, "Derogaremos los artículos del Código Penal que castigan", "los delitos contra la Corona"),
             P(-2, VOX, 56, "Las penas por las ofensas y ultrajes a España y sus símbolos o emblemas deben agravarse", "quede impune."),
             P(-1, PP, 37, "Llevaremos a cabo una reforma legal que rehabilite y proteja los símbolos del Estado", "proteja los símbolos del Estado", inferida=True,
               nota="Propone reforzar la protección legal de los símbolos, sin mencionar el Código Penal."),
         ]),
    # ---------------- DERECHOS SOCIALES E IGUALDAD ----------------
    dict(id="der-1", tema="derechos", formulada_desde="PP/VOX",
         texto="Deberían eliminarse las leyes que tratan de forma específica la violencia contra las mujeres por parte de sus parejas o exparejas (violencia de género).",
         contexto="La ley de violencia de género de 2004 trata esta violencia de forma separada: tiene juzgados especializados, castiga con más pena algunos delitos cuando el agresor es un hombre y la víctima su pareja o expareja, y da ayudas y protección a las víctimas.",
         posturas=[
             P(2, VOX, 30, "Derogar las leyes que han criminalizado a los hombres y desprotegido a las mujeres.", "desprotegido a las mujeres."),
             P(-1, PP, 17, "Cada año rendiremos cuentas del cumplimiento del Pacto de Estado contra la Violencia de Género.", "contra la Violencia de Género.", inferida=True,
               nota="Se compromete con el Pacto de Estado contra la Violencia de Género, cuyo marco son estas leyes."),
             P(-2, PSOE, 82, "Aprobar una Ley Orgánica contra la Violencia Vicaria como manifestación de la violencia de género", "como manifestación de la violencia de género"),
             P(-1, FA, 38, "blindaremos con carácter plurianual las partidas estructurales del Pacto de Estado", "contra la Violencia de Género", inferida=True,
               nota="Se compromete con el Pacto de Estado contra la Violencia de Género."),
             P(-1, POD, 51, "Este fondo garantizará la financiación pública de todas las medidas", "contra las violencias machistas", inferida=True,
               nota="Propone reforzar la financiación de las políticas contra la violencia machista."),
         ]),
    dict(id="der-2", tema="derechos", formulada_desde="PP/VOX",
         texto="Para cambiar el sexo que consta en el Registro Civil y en el DNI no debería bastar con que la persona lo pida.",
         contexto="Desde la ley de 2023 (conocida como «ley trans»), las personas mayores de 16 años pueden cambiarlo solo con pedirlo, sin informes médicos ni tratamientos. Para los menores de 16 hay requisitos adicionales.",
         posturas=[
             P(2, PP, 35, "eliminaremos la libre autodeterminación registral del sexo", "autodeterminación registral del sexo"),
             P(-2, FA, 123, "autodeterminación de las personas trans, intersex y no binarias", "intersex y no binarias"),
             P(-1, PSOE, 97, "Garantizar que la Ley 4/2023 sea el suelo común de derechos", "en toda España", inferida=True,
               nota="La Ley 4/2023 incluye la rectificación registral por declaración de la persona."),
             P(-1, POD, 52, "El Estado debe reconocer todos sus derechos a las personas no binarias", "reconocerles su identidad.", inferida=True,
               nota="Propone reconocer la identidad declarada de las personas no binarias en los documentos oficiales."),
         ]),
    dict(id="der-3", tema="derechos", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="El derecho al aborto debería incluirse en la Constitución.",
         contexto="Hoy el aborto lo regula una ley de 2010: la mujer puede decidir abortar hasta la semana 14 de embarazo, y después solo en algunos casos, como un riesgo grave para su salud. Si está en la Constitución, es mucho más difícil cambiarlo. En 2026 se inició una reforma de la Constitución para incluirlo, que no se ha completado.",
         posturas=[
             P(2, PSOE, 81, "Blindar constitucionalmente el derecho a la interrupción voluntaria del embarazo.", "voluntaria del embarazo."),
             P(2, FA, 28, "Reformaremos el artículo 43 de la Constitución para incluir el derecho al aborto", "el derecho al aborto"),
             P(2, POD, 51, "Incorporar expresamente el derecho al aborto en la Constitución", "en la Constitución"),
             P(-1, VOX, 52, "Defensa del derecho a la vida desde su concepción hasta la muerte natural", "fin de la cultura de la muerte.", inferida=True,
               nota="Defender la vida «desde su concepción» se entiende contrario a reconocer el aborto como derecho constitucional."),
         ]),
    # ---------------- SEGURIDAD ----------------
    dict(id="seg-1", tema="seguridad", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="Debería eliminarse la Ley de Seguridad Ciudadana de 2015.",
         contexto="Esta ley regula, entre otras cosas, las multas que la Administración puede poner sin pasar por un juez por conductas relacionadas con el orden público, por ejemplo en manifestaciones. Sus críticos la llaman «ley mordaza».",
         posturas=[
             P(2, FA, 142, "Derogaremos por completo la Ley Mordaza.", "la Ley Mordaza."),
             P(2, POD, 133, "Derogar la Ley Mordaza y reformar la legislación que limita los derechos fundamentales.", "los derechos fundamentales."),
             P(2, PSOE, 99, "Aprobar una nueva Ley de Seguridad Ciudadana que sustituya a la Ley Orgánica 4/2015", "a la Ley Orgánica 4/2015"),
             P(-1, PP, 16, "Elevaremos la multa mínima a 3.000 euros", "durante desórdenes multitudinarios", inferida=True,
               nota="Propone endurecer las multas administrativas por desórdenes, no derogar la ley."),
         ]),
    dict(id="seg-2", tema="seguridad", formulada_desde="PP/VOX",
         texto="Las penas por participar en disturbios violentos en la calle deberían ser más duras.",
         contexto="Hoy el Código Penal castiga los «desórdenes públicos» (alterar la paz en grupo con violencia o amenazas) con entre 6 meses y 3 años de cárcel, y más en los casos graves.",
         posturas=[
             P(2, PP, 16, "Reformaremos el delito de desórdenes públicos", "por participar en disturbios violentos"),
             P(-1, FA, 142, "Reduciremos las multas excesivas", "«criterios de proporcionalidad»", inferida=True,
               nota="Dentro del apartado «Acabar con la criminalización de la protesta social»; se refiere a multas, no a penas por disturbios violentos."),
         ]),
    # ---------------- EXTERIOR Y DEFENSA ----------------
    dict(id="ext-1", tema="exterior", formulada_desde="PP/VOX",
         texto="España debería gastar más dinero en defensa (ejército y armamento).",
         contexto="En 2025 los países de la OTAN acordaron gastar en defensa y seguridad el 5 % de su riqueza (PIB) de aquí a 2035. España consiguió quedar fuera de ese objetivo.",
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
         contexto="La OTAN es una alianza militar de Estados Unidos, Canadá y la mayoría de países europeos: si uno es atacado, los demás se comprometen a defenderlo. España forma parte desde 1982, y en 1986 se votó en referéndum seguir dentro.",
         posturas=[
             P(2, POD, 28, "Impulsaremos la salida de España de la OTAN", "del Tratado del Atlántico Norte"),
             P(-2, PP, 21, "Reforzaremos cuando sea necesario los contingentes españoles de la OTAN", "de la OTAN"),
             P(-1, PSOE, 105, "Somos aliados, no vasallos.", "no vasallos.", inferida=True,
               nota="Se presenta como aliado dentro de la OTAN."),
         ]),
    dict(id="ext-3", tema="exterior", formulada_desde="FRENTE_AMPLIO/PODEMOS/PSOE",
         texto="España debería romper relaciones con Israel: retirar su embajada y dejar de comerciar con ese país.",
         contexto="España reconoció a Palestina como Estado en 2024 y en 2025 prohibió comprar y vender armas a Israel, pero mantiene relaciones diplomáticas con los dos.",
         posturas=[
             P(2, POD, 34, "Ruptura de las relaciones diplomáticas, culturales y comerciales con Israel.", "comerciales con Israel."),
             P(1, FA, 132, "suspensión efectiva del Acuerdo de Asociación UE-Israel", "Acuerdo de Asociación UE-Israel",
               nota="Propone suspender el acuerdo comercial UE-Israel y un embargo de armas, no la ruptura diplomática."),
             P(-1, PP, 57, "Impulsaremos soluciones diplomáticas para la resolución de conflictos", "países árabes de la región.", inferida=True,
               nota="Considera a Israel un socio clave."),
         ]),
    dict(id="ext-4", tema="exterior", formulada_desde="PP/VOX",
         texto="España debería seguir enviando ayuda militar a Ucrania.",
         contexto="Desde que Rusia invadió Ucrania en 2022, España le envía armas y material militar, además de ayuda económica y humanitaria. Estar en desacuerdo significa dejar de enviar ayuda militar.",
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
    salida.append({k: q[k] for k in ("id", "tema", "texto", "contexto", "formulada_desde")} | {"posturas": pos})

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
