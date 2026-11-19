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

## Fase 1: Extracción (`pipeline/`) `[~]`

- [ ] `pipeline/extract.py`: texto por página con PyMuPDF → `data/textos/<PARTIDO>.json` (`[{pagina, texto}]`, página física + 1)
- [ ] Normalización para búsquedas: espacios, guiones de corte, comillas tipográficas, ligaduras
- [ ] `requirements.txt`
- [ ] Commit de la fase

## Fase 2: Catálogo de propuestas

- [ ] `data/catalogo/<PARTIDO>.json` con `{tema, resumen, cita_literal, pagina}`
- [ ] Temas: vivienda, fiscalidad, empleo, pensiones, sanidad, educación, inmigración, energía y medio ambiente, modelo territorial, instituciones y justicia, derechos sociales e igualdad, seguridad, exterior y defensa
- [ ] Citas exactas, como máximo unas 40 palabras
- [ ] Commit de la fase

## Fase 3: Afirmaciones y posturas

- [ ] ~30 afirmaciones (2-3 por tema) en `data/preguntas.json`
- [ ] Cada una separa a los partidos (si todos coinciden, se descarta)
- [ ] Medidas concretas, una sola idea, redacción neutra
- [ ] Equilibrio: ~mitad formuladas como propuesta de un bloque y ~mitad del otro
- [ ] Posturas en {-2..2, null} con cita y página siempre que no sean null
- [ ] Revisión de las dudas de interpretación con el usuario
- [ ] Commit de la fase

## Fase 4: Verificador de citas

- [ ] `pipeline/verify_quotes.py`: la cita existe en el texto y en la página indicada (rapidfuzz ≥ 0,95)
- [ ] Validación del esquema (valores, cita y página obligatorias si valor ≠ null)
- [ ] Sale con código ≠ 0 y lista los errores si algo falla
- [ ] Tests con pytest
- [ ] Commit de la fase

## Fase 5: Web (`web/`, Vite + Svelte + TypeScript)

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
