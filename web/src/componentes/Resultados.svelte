<script lang="ts">
  import { calcularAfinidad, type Respuesta } from '../lib/afinidad';
  import { barajar, ordenarPorAfinidad } from '../lib/orden';
  import {
    preguntas,
    partidos,
    temas,
    nombrePartido,
    ETIQUETA_RESPUESTA,
    ETIQUETA_POSTURA,
    urlPdf,
    urlLogo,
  } from '../lib/datos';
  import { enfocar } from '../lib/enfocar';

  let {
    respuestas,
    onReiniciar,
    onMetodologia,
  }: { respuestas: Record<string, Respuesta>; onReiniciar: () => void; onMetodologia: () => void } = $props();

  const COBERTURA_MINIMA = 0.6;

  // Se calcula una sola vez al entrar: el orden aleatorio no debe cambiar mientras se mira.
  // svelte-ignore state_referenced_locally
  const resultados = calcularAfinidad(preguntas, respuestas, partidos.map((p) => p.id));
  const ordenados = ordenarPorAfinidad(resultados);
  const ordenColumnas = barajar(partidos.map((p) => p.id));
  const respondidas = resultados[0]?.respondidas ?? 0;
  const temasRespondidos = temas.filter((t) =>
    preguntas.some((q) => q.tema === t.id && respuestas[q.id] && respuestas[q.id].valor !== null),
  );
  const porPartido = Object.fromEntries(resultados.map((r) => [r.partido, r]));

  // Retraso de cada barra al entrar: huecos de 60, 50, 40 y 30 ms (decrecientes, no uniformes).
  const RETRASOS = [0, 60, 110, 150, 180];

  const pct = (x: number | null) => (x === null ? '—' : `${Math.round(x)} %`);
  // Tramo del mapa de calor (1-5, de 20 en 20 puntos); el número siempre se muestra.
  const tramo = (x: number | null) => (x === null ? null : Math.min(5, Math.floor(x / 20) + 1));

  function textoRespuesta(r: Respuesta | undefined) {
    if (!r) return 'Sin responder';
    if (r.valor === null) return 'Saltada';
    return ETIQUETA_RESPUESTA[String(r.valor)] + (r.importante ? ' · importante' : '');
  }
</script>

<section aria-labelledby="titulo-resultados" class="resultados">
  <h1 id="titulo-resultados" tabindex="-1" use:enfocar>Tus resultados</h1>

  <div class="aviso" role="note">
    <svg class="aviso-icono" viewBox="0 0 20 20" aria-hidden="true" focusable="false">
      <circle cx="10" cy="10" r="8.25" fill="none" stroke="currentColor" stroke-width="1.5" />
      <path d="M10 9v5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
      <circle cx="10" cy="6.2" r="1" fill="currentColor" />
    </svg>
    <p>
      <strong>Mide afinidad con programas, no es una recomendación de voto.</strong> El resultado depende de las
      afirmaciones elegidas y de lo que cada programa dice (o no dice) sobre ellas.
    </p>
  </div>

  {#if respondidas === 0}
    <p>No has respondido ninguna afirmación, así que no se puede calcular la afinidad.</p>
    <button class="boton" onclick={onReiniciar}>Volver a empezar</button>
  {:else}
    <h2>Afinidad global</h2>
    <p class="suave explicacion">
      100 % significa coincidencia total en las afirmaciones en las que el partido se pronuncia. Has respondido
      {respondidas} de {preguntas.length}. En caso de empate, el orden es aleatorio.
    </p>
    <!-- Las barras crecen una vez al llegar, en orden de resultado y con huecos decrecientes (ola, no cola) -->
    <ol class="barras tarjeta">
      {#each ordenados as r, i (r.partido)}
        <li class="barra-fila">
          <div class="barra-cabecera">
            <span class="nombre">
              <!-- alt vacío: el nombre va justo al lado, así el lector de pantalla no lo repite -->
              <img class="logo-partido" src={urlLogo(r.partido)} alt="" width="54" height="36" />
              {nombrePartido(r.partido)}
            </span>
            <span class="valor">{r.afinidad === null ? 'Sin datos' : pct(r.afinidad)}</span>
          </div>
          <div class="barra-pista" aria-hidden="true">
            <div
              class="barra-relleno"
              style:transform="scaleX({(r.afinidad ?? 0) / 100})"
              style:animation-delay="{RETRASOS[i] ?? 200}ms"
            ></div>
          </div>
          <p class="cobertura suave">
            Se pronuncia en {r.validas} de tus {r.respondidas} respuestas.
            {#if r.cobertura !== null && r.cobertura < COBERTURA_MINIMA}
              <strong class="baja">Cobertura baja: este resultado es menos fiable.</strong>
            {/if}
          </p>
        </li>
      {/each}
    </ol>

    <h2>Afinidad por tema</h2>
    <p class="suave explicacion">Solo se muestran los temas en los que has respondido. «—»: el partido no se pronuncia.</p>
    <!-- tabindex: permite desplazar la tabla con el teclado en móvil (WCAG 2.1.1) -->
    <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
    <div class="tabla-scroll" role="region" aria-label="Tabla de afinidad por tema" tabindex="0">
      <table class="mapa">
        <caption class="visualmente-oculto">Afinidad por tema y partido, en porcentaje</caption>
        <thead>
          <tr>
            <th scope="col">Tema</th>
            {#each ordenColumnas as p (p)}
              <th scope="col">{nombrePartido(p)}</th>
            {/each}
          </tr>
        </thead>
        <tbody>
          {#each temasRespondidos as t (t.id)}
            <tr>
              <th scope="row">{t.nombre}</th>
              {#each ordenColumnas as p (p)}
                {@const v = porPartido[p].porTema[t.id]}
                {@const n = tramo(v)}
                <td
                  style:background={n ? `var(--mapa-${n})` : null}
                  style:color={n ? `var(--mapa-texto-${n})` : null}
                >
                  {pct(v)}
                </td>
              {/each}
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}

  <h2>Pregunta a pregunta</h2>
  <p class="suave explicacion">
    Despliega cada afirmación para ver la postura de cada partido, la cita literal de su programa y el enlace a la
    página exacta del PDF. Las posturas marcadas como «inferida» no aparecen de forma literal y se han deducido de la
    cita; por eso cuentan con intensidad moderada.
  </p>
  <div class="detalle">
    {#each preguntas as q, i (q.id)}
      <details class="tarjeta">
        <summary>
          <span class="num suave">{i + 1}.</span>
          <span class="enunciado">{q.texto}</span>
          <span class="tu suave">Tú: {textoRespuesta(respuestas[q.id])}</span>
          <svg class="chevron" viewBox="0 0 20 20" aria-hidden="true" focusable="false">
            <path d="M5 7.5l5 5 5-5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </summary>
        <ul class="posturas">
          {#each ordenColumnas as p (p)}
            {@const s = q.posturas[p]}
            <li>
              <p class="postura-cabecera">
                <strong>{nombrePartido(p)}:</strong>
                {ETIQUETA_POSTURA[String(s.valor)]}
                {#if s.inferida}<span class="etiqueta">inferida</span>{/if}
              </p>
              {#if s.valor !== null && s.cita && s.pagina}
                <blockquote>«{s.cita}»</blockquote>
                {#if s.nota}<p class="nota suave">{s.nota}</p>{/if}
                <a href={urlPdf(p, s.pagina)} target="_blank" rel="noopener noreferrer">
                  Ver en el programa de {nombrePartido(p)}, p.&nbsp;{s.pagina}<span class="visualmente-oculto">
                    (se abre en una pestaña nueva)</span
                  >
                </a>
              {/if}
            </li>
          {/each}
        </ul>
      </details>
    {/each}
  </div>

  <div class="acciones">
    <button class="boton" onclick={onReiniciar}>Reiniciar el test</button>
    <button class="boton secundario" onclick={onMetodologia}>Metodología</button>
  </div>
</section>

<style>
  h1 {
    font-size: clamp(2rem, 7vw, 2.6rem);
    letter-spacing: -0.03em;
  }
  h2 {
    font-size: 1.3rem;
    margin-top: 2.5rem;
  }
  .explicacion {
    font-size: 0.95rem;
  }
  .barras {
    list-style: none;
    margin: 0;
    padding: 1.25rem 1.25rem 0.4rem;
  }
  .barra-fila {
    margin-bottom: 1.15rem;
  }
  .barra-cabecera {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.75rem;
    font-weight: 600;
    margin-bottom: 0.55rem;
  }
  .nombre {
    display: inline-flex;
    align-items: center;
    gap: 0.7rem;
    min-width: 0;
  }
  /* Ficha del logotipo: todas del mismo tamaño (3:2), recortadas del propio programa */
  .logo-partido {
    flex-shrink: 0;
    width: 54px;
    height: 36px;
    border-radius: 8px;
    box-shadow: var(--sombra-1);
  }
  .valor {
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    font-variant-numeric: tabular-nums;
  }
  .barra-pista {
    height: 12px;
    background: var(--barra-fondo);
    border-radius: 999px;
    overflow: hidden;
  }
  .barra-relleno {
    width: 100%;
    height: 100%;
    background: var(--barra);
    border-radius: inherit;
    transform-origin: left center;
    animation: crecer 700ms var(--ease-out) both;
  }
  /* Los datos crecen desde su origen (0 %). Pantalla que se ve una vez: admite algo más de duración. */
  @keyframes crecer {
    from {
      transform: scaleX(0);
    }
  }
  @media (prefers-reduced-motion: reduce) {
    .barra-relleno {
      animation: fundido 200ms ease both;
      animation-delay: 0ms !important;
    }
  }
  .cobertura {
    font-size: 0.9rem;
    margin: 0.3rem 0 0;
  }
  .baja {
    display: block;
    color: var(--texto);
  }
  .baja::before {
    content: '⚠ ';
  }
  .tabla-scroll {
    overflow-x: auto;
    border-radius: var(--radio);
    box-shadow: var(--sombra-1);
    outline: 1px solid transparent;
  }
  .mapa {
    border-collapse: collapse;
    width: 100%;
    min-width: 30rem;
    font-size: 0.92rem;
    background: var(--superficie);
  }
  .mapa th,
  .mapa td {
    padding: 0.55rem 0.5rem;
    border-bottom: 1px solid var(--borde);
    text-align: center;
  }
  .mapa th[scope='row'] {
    text-align: left;
    font-weight: 500;
  }
  /* Columna de temas fija al desplazar horizontalmente en pantallas estrechas */
  .mapa th:first-child {
    position: sticky;
    left: 0;
    z-index: 1;
    background: var(--superficie);
    min-width: 7.5rem;
    max-width: 9rem;
    border-right: 1px solid var(--borde);
  }
  .mapa td {
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
  }
  .detalle {
    display: grid;
    gap: 0.6rem;
  }
  .detalle .tarjeta {
    padding: 0;
    transition: box-shadow 200ms ease;
  }
  .detalle .tarjeta[open] {
    box-shadow: var(--sombra-2);
  }
  summary {
    cursor: pointer;
    display: grid;
    grid-template-columns: auto 1fr auto;
    column-gap: 0.6rem;
    padding: 1rem 1.15rem;
    border-radius: var(--radio);
    list-style: none;
    touch-action: manipulation;
    transition: background-color 150ms ease;
  }
  summary::-webkit-details-marker {
    display: none;
  }
  @media (hover: hover) and (pointer: fine) {
    summary:hover {
      background: var(--superficie-2);
    }
  }
  /* Flecha que gira al desplegar: el cambio de estado se ve como continuo */
  .chevron {
    grid-column: 3;
    grid-row: 1;
    width: 1.2rem;
    height: 1.2rem;
    margin-top: 0.2rem;
    color: var(--texto-suave);
    transition: transform 200ms var(--ease-out);
  }
  details[open] .chevron {
    transform: rotate(180deg);
  }
  summary .tu {
    grid-column: 2;
    font-size: 0.9rem;
  }
  .posturas {
    list-style: none;
    padding: 0 1.15rem 0.4rem;
    margin: 0;
  }
  .posturas li {
    border-top: 1px solid var(--borde);
    padding: 0.75rem 0;
  }
  .postura-cabecera {
    margin: 0 0 0.4rem;
  }
  .etiqueta {
    display: inline-block;
    margin-left: 0.4rem;
    padding: 0 0.45rem;
    border: 1px solid var(--borde);
    border-radius: 999px;
    font-size: 0.8rem;
  }
  blockquote {
    margin: 0 0 0.4rem;
    padding-left: 0.8rem;
    border-left: 3px solid var(--borde);
    font-style: italic;
  }
  .nota {
    font-size: 0.9rem;
    margin-bottom: 0.4rem;
  }
  .acciones {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-top: 2rem;
  }
</style>
