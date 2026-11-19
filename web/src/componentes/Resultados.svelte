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

  const pct = (x: number | null) => (x === null ? '—' : `${Math.round(x)} %`);
  // Intensidad de gris de la celda (0–100) para el mapa de calor; el número siempre se muestra.
  const intensidad = (x: number | null) => (x === null ? 0 : Math.round(15 + x * 0.75));

  function textoRespuesta(r: Respuesta | undefined) {
    if (!r) return 'Sin responder';
    if (r.valor === null) return 'Saltada';
    return ETIQUETA_RESPUESTA[String(r.valor)] + (r.importante ? ' · importante' : '');
  }
</script>

<section aria-labelledby="titulo-resultados" class="resultados">
  <h1 id="titulo-resultados" tabindex="-1" use:enfocar>Tus resultados</h1>

  <div class="aviso" role="note">
    <strong>Mide afinidad con programas, no es una recomendación de voto.</strong> El resultado depende de las
    afirmaciones elegidas y de lo que cada programa dice (o no dice) sobre ellas.
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
    <ol class="barras">
      {#each ordenados as r (r.partido)}
        <li class="barra-fila">
          <div class="barra-cabecera">
            <span class="nombre">{nombrePartido(r.partido)}</span>
            <span class="valor">{r.afinidad === null ? 'Sin datos' : pct(r.afinidad)}</span>
          </div>
          <div class="barra-pista" aria-hidden="true">
            <div class="barra-relleno" style:width="{r.afinidad ?? 0}%"></div>
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
                <td
                  class:oscura={v !== null && v >= 60}
                  style:background="color-mix(in srgb, var(--barra) {intensidad(v)}%, var(--superficie))"
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
                  Ver en el programa de {nombrePartido(p)}, p. {s.pagina}<span class="visualmente-oculto">
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
    font-size: clamp(1.7rem, 6vw, 2.2rem);
  }
  h2 {
    font-size: 1.3rem;
    margin-top: 2rem;
  }
  .explicacion {
    font-size: 0.95rem;
  }
  .barras {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .barra-fila {
    margin-bottom: 1.1rem;
  }
  .barra-cabecera {
    display: flex;
    justify-content: space-between;
    font-weight: 600;
    margin-bottom: 0.3rem;
  }
  .valor {
    font-variant-numeric: tabular-nums;
  }
  .barra-pista {
    height: 14px;
    background: var(--barra-fondo);
    border-radius: 7px;
    overflow: hidden;
  }
  .barra-relleno {
    height: 100%;
    background: var(--barra);
    border-radius: 7px;
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
    border: 1px solid var(--borde);
    border-radius: var(--radio);
  }
  .mapa {
    border-collapse: collapse;
    width: 100%;
    min-width: 34rem;
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
  .mapa td {
    font-variant-numeric: tabular-nums;
  }
  .mapa td.oscura {
    color: var(--acento-texto);
    font-weight: 600;
  }
  .detalle {
    display: grid;
    gap: 0.6rem;
  }
  summary {
    cursor: pointer;
    display: grid;
    grid-template-columns: auto 1fr;
    column-gap: 0.5rem;
  }
  summary .tu {
    grid-column: 2;
    font-size: 0.9rem;
  }
  .posturas {
    list-style: none;
    padding: 0;
    margin: 1rem 0 0;
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
