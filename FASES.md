# Fases de desarrollo: test de afinidad 29N

Seguimiento del desarrollo. Cada casilla se marca (`[x]`) al completarse y verificarse.
Leyenda: `[ ]` pendiente · `[~]` en curso · `[x]` completada · `[!]` bloqueada (requiere decisión)

Última actualización: 2026-11-19

---

## Fase 0: Verificar los PDF `[x]`

- [x] Comprobar que cada PDF es el programa de las generales del 29-11-2026
  - [x] FRENTE_AMPLIO.pdf: portada (p. 1, vectorial) «Elecciones Generales · 29N 2026»
  - [x] PODEMOS.pdf: p. 5 «programa de cara a las elecciones generales del 29N»; PDF creado el 17-11-2026, posterior a la nota de prensa del 16-11
  - [x] PP.pdf: p. 6 «unas elecciones tan determinantes como las del próximo 29 de noviembre»; p. 64 «2026»
  - [x] PSOE.pdf: p. 1 «Programa Elecciones Generales 29 noviembre 2026»
  - [x] VOX.pdf: p. 3 «Programa electoral 29 de noviembre de 2026»
- [x] Detectar PDF escaneados: ninguno. Los 5 tienen capa de texto (maquetados en InDesign/Word); las páginas sin texto son fotos, portadillas o fondos (revisadas visualmente). No hace falta OCR.
- [x] Confirmación del usuario de qué PDF se incluyen: se incluyen los 5

**Resultado:**

| PDF | Págs. | Caracteres | Fecha del PDF | Elección | Capa de texto |
|---|---|---|---|---|---|
| FRENTE_AMPLIO | 151 | 347 k | 17-11-2026 | Generales 29N 2026 | Sí |
| PODEMOS | 141 | 354 k | 17-11-2026 | Generales 29N 2026 | Sí |
| PP | 64 | 158 k | 10-11-2026 | Generales 29N 2026 | Sí |
| PSOE | 114 | 251 k | 14-11-2026 | Generales 29N 2026 | Sí |
| VOX | 66 | 48 k | 04-11-2026 | Generales 29N 2026 | Sí |

Notas para la Fase 1: hay guiones blandos (U+00AD) en los cortes de palabra («elec­ ciones») y viñetas (●, •) que habrá que normalizar. La paginación impresa no coincide con la física (p. ej., en FRENTE_AMPLIO la física 27 lleva impreso el 31 y la física 56 el 62), así que usaremos siempre la física, como está especificado.

## Fase 1: Extracción (`pipeline/`) `[x]`

- [x] `pipeline/extract.py`: texto por página con PyMuPDF → `data/textos/<PARTIDO>.json` (`[{pagina, texto}]`, página física + 1), más `data/textos/fuentes.json` con el SHA-256 de cada PDF
- [x] Normalización (`pipeline/normalizar.py`): `limpiar` (guiones blandos y de corte, ligaduras y espacios, para el texto guardado) y `normalizar` (además comillas, rayas, viñetas y minúsculas, para comparar); 7 tests con pytest
- [x] Comprobado: 0 guiones blandos, ligaduras o caracteres corruptos restantes; orden de lectura correcto en páginas a varias columnas
- [x] `requirements.txt`
- [x] Commit de la fase

## Fase 2: Catálogo de propuestas `[x]`

- [x] `data/catalogo/<PARTIDO>.json` con `{tema, resumen, cita_literal, pagina, usada_en}` (162 propuestas: las 120 citadas en posturas y 42 revisadas y descartadas por consenso o por falta de contraste)
- [x] Temas: vivienda, fiscalidad, empleo, pensiones, sanidad, educación, inmigración, energía y medio ambiente, modelo territorial, instituciones y justicia, derechos sociales e igualdad, seguridad, exterior y defensa
- [x] Citas exactas, como máximo unas 40 palabras: se recortan automáticamente del texto extraído entre una frase de inicio y otra de fin (`pipeline/construir_datos.py`)
- [x] Herramientas de apoyo: `pipeline/buscar.py` (búsqueda normalizada) y `pipeline/paginas.py` (lectura por página)
- [x] Mejora de la normalización: se unen los guiones de corte en titulares en mayúsculas («SOCIEDA- DES»)
- [x] Commit de la fase
- Limitación: el catálogo no es exhaustivo. VOX y PP se leyeron completos; en FRENTE_AMPLIO, PODEMOS y PSOE se leyeron las secciones de cada tema y se buscaron las medidas en disputa.

## Fase 3: Afirmaciones y posturas `[x]`

- [x] 33 afirmaciones en `data/preguntas.json` (2-4 por tema; pensiones solo 1, porque PP y VOX apenas concretan)
- [x] Cada una separa a los partidos (si todos coinciden, se descarta)
- [x] Medidas concretas, una sola idea, redacción neutra y `contexto` explicativo
- [x] Equilibrio: 16 formuladas a partir de propuestas de FRENTE_AMPLIO/PODEMOS/PSOE y 17 de PP/VOX (campo `formulada_desde`)
- [x] Posturas en {-2..2, null} con cita y página siempre que no sean null; campos `inferida` y `nota`
- [x] Revisión de las dudas de interpretación con el usuario (ver registro de decisiones)
- [x] Cobertura: FRENTE_AMPLIO 28/33, PP 25/33, PODEMOS 23/33, PSOE 22/33, VOX 22/33
- [x] Commit de la fase

## Fase 4: Verificador de citas `[x]`

- [x] `pipeline/verify_quotes.py`: la cita existe en el texto y en la página indicada (coincidencia normalizada exacta; si no, rapidfuzz ≥ 95 **y** todas las cifras de la cita presentes en el fragmento alineado)
- [x] Validación del esquema (valores, cita y página obligatorias si valor ≠ null, temas, ids, que cada pregunta separe a los partidos); también verifica el catálogo
- [x] Sale con código ≠ 0 y lista los errores (indicando en qué página está la cita si es otra)
- [x] Tests con pytest (25 en total), incluida la integración con los datos reales
- [x] Prueba de mutación: una cifra cambiada (similitud 99,1) y una página errónea se detectan
- [x] Commit de la fase

## Fase 5: Web (`web/`, Vite + Svelte + TypeScript) `[x]`

- [x] Proyecto base con `base: '/afinidad-29n/'`
- [x] `web/src/lib/afinidad.ts` (función pura: afinidad, cobertura, por tema, `null` sin datos)
- [x] Pantalla Inicio (qué es, cómo funciona, aviso de neutralidad y privacidad, "Empezar")
- [x] Pantalla Preguntas (una por pantalla, progreso, 5 opciones + Saltar, "importante", contexto, volver atrás)
- [x] Pantalla Resultados (barras globales, cobertura con aviso < 60 %, heatmap tema × partido, detalle con cita y enlace `.pdf#page=N`, reiniciar)
- [x] Pantalla Metodología (fuentes con fecha, criterios, escala, fórmula, limitaciones, repo)
- [x] Copia de los PDF a `web/public/programas/` en el build
- [x] Mobile-first, accesible (contraste, teclado, aria), en español: revisado en Chrome (390 px y 1280 px, tema claro y oscuro, solo teclado); Lighthouse: accesibilidad 100, buenas prácticas 100
- [x] Correcciones de la revisión: mapa de calor en 5 tramos con contraste ≥ 5,3:1 en ambos temas (antes 3,05:1 en grises medios), columna de temas fija al desplazar, «Saltar» diferenciado de la escala, indicador +/− en los desplegables, «p. N» sin corte de línea
- [x] Privacidad: sin backend, cookies, analítica ni localStorage de respuestas
- [x] Neutralidad: orden aleatorio, colores neutros, sin logos, aviso "no es una recomendación de voto"
- [x] Commit de la fase

## Fase 6: Tests (Vitest) `[x]`

- [x] Partido espejo → 100 % (para cada partido)
- [x] Opuesto total → 0 %
- [x] Saltadas no cuentan, peso ×2 y `null` excluido
- [x] Cobertura correcta y "sin datos" → `null`
- [x] Commit de la fase

## Fase 7: CI/CD `[x]`

- [x] `.github/workflows/deploy.yml` (push a `main`; en pull requests solo verifica)
- [x] Python: reextracción de los PDF con `git diff --exit-code data/textos` (extracción determinista, comprobado) + `verify_quotes.py` + pytest
- [x] Node: `npm ci` + svelte-check + Vitest + build
- [x] Despliegue con `actions/deploy-pages` (bloqueado si falla algo)
- [x] Repo público en GitHub y Pages activado («Source: GitHub Actions»)
- [x] Primera ejecución correcta (los 3 jobs); web en https://miguelit011.github.io/afinidad-29n/ revisada: test completo sin errores de consola y sin peticiones de red durante el test
- [x] Commit de la fase

## Extras

- [x] README (qué es, enlace, metodología resumida, cómo reproducir, cómo reportar errores)
- [x] Plantilla de issue para errores de codificación (`.github/ISSUE_TEMPLATE/error-codificacion.yml`)
- [x] `.gitignore` (node_modules, dist, venv, `__pycache__`)

---

## Registro de decisiones

| Fecha | Decisión |
|---|---|
| 2026-11-19 | Inicio del proyecto. |
| 2026-11-19 | Fase 0: se incluyen los 5 programas (FRENTE_AMPLIO, PODEMOS, PP, PSOE, VOX); todos son de las generales del 29N 2026 y ninguno necesita OCR. PODEMOS sí publicó programa (PDF del 17-11). |
| 2026-11-19 | Fase 5: CSP en producción con `connect-src 'none'` (la página no puede enviar datos); sin fuentes externas. |
| 2026-11-19 | Fase 3, criterios de codificación: (a) los logros pasados que describe un partido cuentan como postura con intensidad ±1; (b) las posturas que requieren una inferencia corta desde la cita se codifican con ±1 y se marcan como `inferida` (la web lo indica); (c) se aceptan afirmaciones en las que solo se pronuncian partidos de un bloque si difieren en intensidad (jornada de 35 h, pensión mínima = SMI); (d) en seguridad se incluyen «derogar la Ley de Seguridad Ciudadana de 2015» y «endurecer penas por disturbios violentos», con las posturas contrarias inferidas. |
| 2026-11-19 | Fase 0: la fecha del PDF del PSOE es la de creación (14-11-2026, 22:02 UTC); el 15-11 era la de modificación. |
| 2026-11-19 | Fase 5: el mapa de calor pasa de un degradado continuo a 5 tramos de gris, porque con un degradado ningún color de texto alcanza 4,5:1 en los grises medios. |
| 2026-11-19 | Selección de partidos: no hay criterio formal; se indica así en Metodología (Fuentes y Limitaciones) y en el README. |
| 2026-11-19 | Publicación: el usuario hará público el repo y activará Pages («Source: GitHub Actions»). |
| 2026-11-19 | Lenguaje claro: el usuario no entendía la mayoría de afirmaciones. Se reescriben las 33 (y sus contextos) sin tecnicismos ni números de ley, manteniendo el mismo sentido para que las posturas codificadas sigan siendo válidas; el contexto pasa a mostrarse siempre («Qué significa») y explica qué hay hoy y, si la afirmación describe lo que ya existe, qué implica estar en desacuerdo. Datos de 2026 tomados de los programas: regularización extraordinaria de 2026 (FRENTE_AMPLIO p. 126, PODEMOS p. 67), reforma constitucional del aborto iniciada en 2026 (PSOE p. 81). Temas renombrados: «Fiscalidad» → «Impuestos», «Modelo territorial» → «Comunidades autónomas». |
| 2026-11-19 | Rediseño visual con la skill `emil-design-eng` (Emil Kowalski, instalada en `~/.claude/skills/` junto con `choreograph`): paleta de grises cálidos (sin tonos asociables a partidos), sombras en capas en vez de bordes, botones que ceden al pulsar (`scale(0.97)`), hover solo con ratón, curvas propias (`--ease-out`), barra de progreso con `scaleX`, cambio de afirmación con fundido de 180 ms en el sentido de la navegación, barras de resultados que crecen una vez con retrasos decrecientes, entrada escalonada solo en la portada. Sin gráficos decorativos que puedan confundirse con un sondeo (prohibidos del 24 al 28-11). Movimiento reducido: solo fundidos. Lighthouse: accesibilidad 100; mapa de calor ≥ 5,35:1. |
| 2026-11-19 | Paleta «de votación» a petición del usuario (más amigable): crema, sepia de la papeleta y el sobre del Senado y tinta marrón; evita rojo, azul, verde, morado, naranja y turquesa. Ilustración de urna en la portada (sobre que cae una vez) y logotipo/favicon de urna. Logotipos de los partidos en los resultados, a petición del usuario: recortados de la contraportada de cada programa por `pipeline/logos.py`, en fichas del mismo tamaño; se actualiza el texto de neutralidad («sin logos») en la portada y se explica en Metodología. Heatmap ≥ 5,30:1; Lighthouse accesibilidad 100. |
| 2026-11-19 | README visual: banner claro/oscuro con la urna (`docs/img/banner-*.svg`), capturas reales de la web, cifras, diagrama Mermaid del proceso y enlaces al test y a la plantilla de errores. No se incluyen capturas con porcentajes por partido, para que no se confundan con un resultado ni con un sondeo. |
