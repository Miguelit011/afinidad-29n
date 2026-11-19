# Afinidad 29N

Test de afinidad con los programas electorales de las **elecciones generales del 29 de noviembre de 2026**.
Respondes a 33 afirmaciones sobre medidas concretas y ves tu afinidad con el programa de cada candidatura,
en global y tema a tema, con la cita literal y la página del PDF que respaldan cada postura.

**Web:** https://miguelit011.github.io/afinidad-29n/

> Mide afinidad con programas, no es una recomendación de voto.

## Cómo funciona

- **Fuente única: los programas oficiales en PDF** de Frente Amplio, Podemos, PP, PSOE y Vox
  (`Programas_Electorales/`). No se usan declaraciones, mítines ni trayectorias.
- **33 afirmaciones en 13 temas** que separan a los partidos. Si todos coinciden en una medida, se descarta.
  16 parten de propuestas de Frente Amplio, Podemos o PSOE y 17 de propuestas de PP o Vox.
- **Posturas de −2 a +2, o «no se pronuncia»**, siempre con cita literal y página. Las posturas
  inferidas y los logros ya aprobados cuentan como ±1, y las inferidas se marcan en la web.
- **Fórmula:** `afinidad = Σ w · (1 − |u − p| / 4) / Σ w`, solo sobre las afirmaciones que has respondido
  y en las que el partido se pronuncia. `w = 2` si marcas la afirmación como importante, si no `w = 1`.
  Se muestra la cobertura y se avisa cuando es inferior al 60 %.
- **Privacidad:** todo se calcula en el navegador. No hay servidor, cookies, analítica ni almacenamiento,
  y una Content-Security-Policy (`connect-src 'none'`) impide que la página envíe datos.

La metodología completa, con sus limitaciones, está en la propia web (enlace «Metodología»).

## Estructura

| Ruta | Contenido |
|---|---|
| `Programas_Electorales/` | Los 5 programas en PDF |
| `pipeline/` | Extracción de texto, herramientas de búsqueda y verificador de citas (Python) |
| `data/textos/` | Texto de cada PDF por página física y huella SHA-256 de cada archivo (`fuentes.json`) |
| `data/catalogo/` | Propuestas catalogadas por partido, con tema, cita y página |
| `data/preguntas.json` | Las 33 afirmaciones y la postura codificada de cada partido |
| `web/` | La web (Vite + Svelte + TypeScript) |
| `FASES.md` | Seguimiento del desarrollo y registro de decisiones |

## Reproducir

Requisitos: Python 3.12 o superior y Node 20 o superior.

```bash
# Datos
pip install -r requirements.txt
python pipeline/extract.py          # regenera data/textos/ a partir de los PDF
python pipeline/verify_quotes.py    # comprueba que cada cita está en su página
python -m pytest -q pipeline

# Web
cd web
npm ci
npm test                            # Vitest
npm run dev                         # http://localhost:5173/afinidad-29n/
npm run build                       # genera web/dist/
```

Para buscar en los programas: `python pipeline/buscar.py "texto"` y `python pipeline/paginas.py PARTIDO N`.

## Verificación automática

En cada push a `main`, GitHub Actions (`.github/workflows/deploy.yml`):

1. vuelve a extraer el texto de los PDF y falla si no coincide con `data/textos/`;
2. comprueba cada cita: debe estar en el texto del partido y en la página indicada, y cualquier cifra
   distinta se rechaza aunque el resto coincida;
3. ejecuta los tests de Python y de la web, comprueba los tipos y compila la web.

La web solo se publica si todo pasa.

## Reportar un error

Si crees que una postura está mal codificada, abre una incidencia con la plantilla
**«Error de codificación»**. Indica la afirmación, el partido y la página del PDF que lo demuestra.
