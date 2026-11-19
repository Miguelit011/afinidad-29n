<script lang="ts">
  import { enfocar } from '../lib/enfocar';
  import { preguntas, partidos, fuentes, version, nombrePartido, REPO_URL, urlPdf } from '../lib/datos';

  let { onVolver }: { onVolver: () => void } = $props();

  const total = preguntas.length;
  const deBloque = (b: string) => preguntas.filter((q) => q.formulada_desde === b).length;
  const cobertura = partidos.map((p) => ({
    nombre: p.nombre,
    n: preguntas.filter((q) => q.posturas[p.id].valor !== null).length,
    inferidas: preguntas.filter((q) => q.posturas[p.id].inferida).length,
  }));
  const fecha = (iso: string | null) => (iso ? new Date(`${iso}T12:00:00`).toLocaleDateString('es-ES', { dateStyle: 'long' }) : '—');
</script>

<article aria-labelledby="titulo-metodologia" class="metodologia">
  <h1 id="titulo-metodologia" tabindex="-1" use:enfocar>Metodología</h1>
  <p class="suave">Versión de los datos: {fecha(version)}.</p>

  <h2>Qué mide</h2>
  <p>
    Esta web compara tus respuestas con lo que dicen los programas electorales oficiales para las elecciones generales
    del 29 de noviembre de 2026. <strong>Mide afinidad con programas, no es una recomendación de voto</strong>: no tiene
    en cuenta declaraciones, mítines, trayectorias ni lo que un partido ha hecho en el gobierno.
  </p>

  <h2>Fuentes</h2>
  <p>
    La única fuente son los programas en PDF. Se han analizado los programas de estas {partidos.length} candidaturas; la
    selección no sigue un criterio formal (como la representación parlamentaria o las encuestas) y otras candidaturas
    podrían añadirse. Se verificó en la portada o la introducción que cada PDF corresponde a estas elecciones y que tiene
    capa de texto (no hizo falta reconocimiento óptico).
  </p>
  <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
  <div class="tabla-scroll" role="region" aria-label="Fuentes" tabindex="0">
    <table>
      <thead>
        <tr><th scope="col">Partido</th><th scope="col">Fecha del PDF</th><th scope="col">Páginas</th><th scope="col">Huella SHA-256</th></tr>
      </thead>
      <tbody>
        {#each fuentes as f (f.partido)}
          <tr>
            <th scope="row"><a href={urlPdf(f.partido, 1)} target="_blank" rel="noopener noreferrer">{nombrePartido(f.partido)}</a></th>
            <td>{fecha(f.fecha_pdf)}</td>
            <td>{f.paginas}</td>
            <td><code title={f.sha256}>{f.sha256.slice(0, 12)}…</code></td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
  <p class="suave nota-tabla">
    La fecha es la de creación que figura en el propio PDF. La huella permite comprobar que el archivo es el mismo que se
    analizó. Los números de página son los del PDF (física), no los impresos.
  </p>

  <h2>Cómo se eligieron las afirmaciones</h2>
  <ul>
    <li>Se leyó cada programa y se catalogaron sus propuestas concretas en 13 temas, con cita literal y página.</li>
    <li>
      Se eligieron {total} afirmaciones que <strong>separan a los partidos</strong>: al menos uno a favor y otro en contra o
      con una postura distinta. Si todos coincidían, la afirmación se descartaba (por ejemplo, revalorizar las pensiones
      con el IPC o la escuela gratuita de 0 a 3 años).
    </li>
    <li>Son medidas concretas, con una sola idea y redacción neutra.</li>
    <li>
      Equilibrio: {deBloque('FRENTE_AMPLIO/PODEMOS/PSOE')} parten de propuestas de Frente Amplio, Podemos o PSOE y
      {deBloque('PP/VOX')} de propuestas de PP o Vox, para que estar «de acuerdo» no favorezca sistemáticamente a un
      bloque.
    </li>
  </ul>

  <h2>Cómo se codificó cada postura</h2>
  <p>Cada partido recibe un valor en cada afirmación:</p>
  <ul class="escala">
    <li><strong>+2</strong> muy a favor · <strong>+1</strong> a favor · <strong>0</strong> neutral · <strong>−1</strong> en contra · <strong>−2</strong> muy en contra</li>
    <li><strong>No se pronuncia</strong>: el programa no dice nada sobre la medida. No cuenta ni a favor ni en contra.</li>
  </ul>
  <p>Reglas:</p>
  <ul>
    <li>Toda postura distinta de «no se pronuncia» va acompañada de una <strong>cita literal</strong> del programa y su página.</li>
    <li>
      Una postura <strong>inferida</strong> (que exige una deducción corta a partir de la cita, por ejemplo «derogar la
      Ley X» frente a una medida de esa ley) se codifica como ±1 y se marca como tal.
    </li>
    <li>Cuando un programa presenta una medida como logro ya aprobado, y no como compromiso nuevo, se codifica como ±1.</li>
    <li>
      Un programa automático comprueba, antes de cada publicación, que cada cita existe en el texto del partido y en la
      página indicada. Si alguna falla, la web no se publica.
    </li>
  </ul>

  <h2>Fórmula</h2>
  <p>
    Tu respuesta <em>u</em> va de −2 (muy en desacuerdo) a +2 (muy de acuerdo); la postura del partido <em>p</em>, de −2
    a +2. Cada afirmación pesa <em>w</em> = 2 si la marcas como importante y 1 si no. Para cada partido, y solo en las
    afirmaciones que has respondido y en las que el partido se pronuncia:
  </p>
  <p class="formula" aria-label="afinidad igual a la suma de w por uno menos el valor absoluto de u menos p entre cuatro, dividida por la suma de w">
    afinidad = Σ w · (1 − |u − p| / 4) / Σ w
  </p>
  <p>
    El resultado se expresa en porcentaje: 100 % si coincides en todo y 0 % si estás en el extremo opuesto en todo. La
    <strong>cobertura</strong> es el número de tus respuestas en las que el partido se pronuncia; si es inferior al 60 %,
    se avisa de que el resultado es menos fiable. Si no hay ninguna afirmación válida, se muestra «sin datos». La
    afinidad por tema usa la misma fórmula, limitada a las afirmaciones de cada tema.
  </p>

  <h2>Cobertura de cada programa</h2>
  <ul>
    {#each cobertura as c (c.nombre)}
      <li>{c.nombre}: se pronuncia en {c.n} de {total} afirmaciones ({c.inferidas} inferidas).</li>
    {/each}
  </ul>

  <h2>Limitaciones</h2>
  <ul>
    <li>
      El resultado depende de qué afirmaciones se han elegido. Con otras, podría cambiar. Pensiones tiene una sola
      afirmación porque PP y Vox apenas concretan en ese tema.
    </li>
    <li>
      Los programas tienen extensiones muy distintas (el de Vox es varias veces más corto). Un partido que se pronuncia en
      pocas afirmaciones puede obtener una afinidad alta o baja con poca base: por eso se muestra la cobertura.
    </li>
    <li>
      Codificar exige interpretar. Por eso cada postura enlaza a su cita y página, y las posturas inferidas están
      marcadas.
    </li>
    <li>Todas las afirmaciones pesan lo mismo, salvo las que marques como importantes.</li>
    <li>El catálogo de propuestas no es exhaustivo: se centra en las medidas en las que los partidos discrepan.</li>
    <li>
      Solo se incluyen {partidos.length} candidaturas, elegidas sin un criterio formal. Concurren otras cuyo programa
      no se ha analizado, y que no aparezcan aquí no dice nada sobre su programa.
    </li>
  </ul>

  <h2>Privacidad</h2>
  <p>
    Las opiniones políticas son datos de categoría especial (art. 9 del Reglamento General de Protección de Datos). Por
    eso todo se calcula en tu navegador: no hay servidor, base de datos, cookies, analítica ni almacenamiento local de tus
    respuestas, y la página tiene prohibido por configuración (Content-Security-Policy) enviar datos a ningún sitio. No
    recogemos ni publicamos estadísticas de uso. Además, la ley prohíbe publicar sondeos electorales del 24 al 28 de
    noviembre.
  </p>

  <h2>Datos abiertos y errores</h2>
  <p>
    Todas las afirmaciones, posturas, citas y páginas están en archivos JSON en el
    <a href={REPO_URL} rel="noopener noreferrer">repositorio público</a>, junto con el código para extraer los textos y
    verificar las citas. Si crees que una postura está mal codificada, abre una incidencia con la plantilla «Error de
    codificación» indicando la afirmación, el partido y la página.
  </p>

  <button class="boton secundario" onclick={onVolver}>← Volver</button>
</article>

<style>
  h1 {
    font-size: clamp(2rem, 7vw, 2.6rem);
    letter-spacing: -0.03em;
  }
  h2 {
    font-size: 1.3rem;
    margin-top: 2.2rem;
  }
  li {
    margin-bottom: 0.4rem;
  }
  .tabla-scroll {
    overflow-x: auto;
    border-radius: var(--radio);
    box-shadow: var(--sombra-1);
    outline: 1px solid transparent;
  }
  th {
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--texto-suave);
  }
  tbody tr:last-child td {
    border-bottom: none;
  }
  table {
    border-collapse: collapse;
    width: 100%;
    min-width: 30rem;
    font-size: 0.92rem;
    background: var(--superficie);
  }
  th,
  td {
    padding: 0.5rem 0.6rem;
    border-bottom: 1px solid var(--borde);
    text-align: left;
  }
  .nota-tabla {
    font-size: 0.9rem;
    margin-top: 0.5rem;
  }
  .formula {
    font-family: ui-monospace, 'Cascadia Mono', Menlo, Consolas, monospace;
    background: var(--superficie-2);
    border-radius: var(--radio-sm);
    padding: 0.8rem 1rem;
    overflow-x: auto;
  }
  .escala {
    list-style: none;
    padding: 0;
  }
  .metodologia > .boton {
    margin-top: 1.5rem;
  }
</style>
