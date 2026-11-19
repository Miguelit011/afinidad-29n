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
| PSOE | 114 | 251 k | 15-11-2026 | Generales 29N 2026 | Sí |
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

## Fase 5: Web (`web/`, Vite + Svelte + TypeScript) `[~]`

- [ ] Proyecto base con `base: '/afinidad-29n/'`
- [ ] `web/src/lib/afinidad.ts` (función pura: afinidad, cobertura, por tema, `null` sin datos)
- [ ] Pantalla Inicio (qué es, cómo funciona, aviso de neutralidad y privacidad, "Empezar")
- [ ] Pantalla Preguntas (una por pantalla, progreso, 5 opciones + Saltar, "importante", contexto, volver atrás)
- [ ] Pantalla Resultados (barras globales, cobertura con aviso < 60 %, heatmap tema × partido, detalle con cita y enlace `.pdf#page=N`, reiniciar)
- [ ] Pantalla Metodología (fuentes con fecha, criterios, escala, fórmula, limitaciones, repo)
- [ ] Copia de los PDF a `web/public/programas/` en el build
- [ ] Mobile-first, accesible (contraste, teclado, aria), en español
- [ ] Privacidad: sin backend, cookies, analítica ni localStorage de respuestas
- [ ] Neutralidad: orden aleatorio, colores neutros, sin logos, aviso "no es una recomendación de voto"
- [ ] Commit de la fase

## Fase 6: Tests (Vitest)

- [ ] Partido espejo → 100 % (para cada partido)
- [ ] Opuesto total → 0 %
- [ ] Saltadas no cuentan, peso ×2 y `null` excluido
- [ ] Cobertura correcta y "sin datos" → `null`
- [ ] Commit de la fase

## Fase 7: CI/CD

- [ ] `.github/workflows/deploy.yml` (push a `main`)
- [ ] Python: `verify_quotes.py` + pytest
- [ ] Node: Vitest + build
- [ ] Despliegue con `actions/deploy-pages` (bloqueado si falla algo)
- [ ] Repo en GitHub y Pages activado
- [ ] Commit de la fase

## Extras

- [ ] README (qué es, enlace, metodología resumida, cómo reproducir, cómo reportar errores)
- [ ] Plantilla de issue para errores de codificación
- [ ] `.gitignore` (node_modules, dist, venv, `__pycache__`)

---

## Registro de decisiones

| Fecha | Decisión |
|---|---|
| 2026-11-19 | Inicio del proyecto. |
| 2026-11-19 | Fase 0: se incluyen los 5 programas (FRENTE_AMPLIO, PODEMOS, PP, PSOE, VOX); todos son de las generales del 29N 2026 y ninguno necesita OCR. PODEMOS sí publicó programa (PDF del 17-11). |
| 2026-11-19 | Fase 3, criterios de codificación: (a) los logros pasados que describe un partido cuentan como postura con intensidad ±1; (b) las posturas que requieren una inferencia corta desde la cita se codifican con ±1 y se marcan como `inferida` (la web lo indica); (c) se aceptan afirmaciones en las que solo se pronuncian partidos de un bloque si difieren en intensidad (jornada de 35 h, pensión mínima = SMI); (d) en seguridad se incluyen «derogar la Ley de Seguridad Ciudadana de 2015» y «endurecer penas por disturbios violentos», con las posturas contrarias inferidas. |
