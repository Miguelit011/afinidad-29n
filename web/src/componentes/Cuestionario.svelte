<script lang="ts">
  import type { Respuesta, Valor } from '../lib/afinidad';
  import { preguntas, nombreTema, ETIQUETA_RESPUESTA } from '../lib/datos';
  import { enfocar } from '../lib/enfocar';

  let {
    respuestas = $bindable(),
    indice = $bindable(),
    onTerminar,
  }: { respuestas: Record<string, Respuesta>; indice: number; onTerminar: () => void } = $props();

  const OPCIONES: Valor[] = [-2, -1, 0, 1, 2];

  const pregunta = $derived(preguntas[indice]);
  const actual = $derived(respuestas[pregunta.id]);
  let importante = $state(false);
  // Sentido del último cambio: la afirmación nueva entra por la derecha al avanzar y por la izquierda al volver.
  let direccion = $state<1 | -1>(1);

  // Al cambiar de pregunta, se recupera lo que la persona marcó (si vuelve atrás).
  $effect.pre(() => {
    importante = respuestas[preguntas[indice].id]?.importante ?? false;
  });

  function responder(valor: Valor | null) {
    respuestas[pregunta.id] = { valor, importante };
    avanzar();
  }

  function avanzar() {
    if (indice < preguntas.length - 1) {
      direccion = 1;
      indice += 1;
      window.scrollTo({ top: 0 });
    } else {
      onTerminar();
    }
  }

  function retroceder() {
    if (indice > 0) {
      direccion = -1;
      indice -= 1;
    }
  }

  function cambiarImportante() {
    // Si ya había respuesta, se actualiza su peso sin obligar a responder de nuevo.
    if (actual) respuestas[pregunta.id] = { ...actual, importante };
  }
</script>

<section aria-labelledby="enunciado" class="cuestionario">
  <div class="progreso">
    <div class="progreso-texto">
      <span id="texto-progreso">Afirmación {indice + 1} de {preguntas.length}</span>
      <span class="suave porcentaje" aria-hidden="true">{Math.round(((indice + 1) / preguntas.length) * 100)} %</span>
    </div>
    <div
      class="pista"
      role="progressbar"
      aria-labelledby="texto-progreso"
      aria-valuemin="1"
      aria-valuemax={preguntas.length}
      aria-valuenow={indice + 1}
    >
      <div class="relleno" style:transform="scaleX({(indice + 1) / preguntas.length})"></div>
    </div>
  </div>

  <!-- La afirmación, su tema y su explicación cambian juntos, como un solo bloque -->
  {#key indice}
    <div class="afirmacion" style:--dir={direccion}>
      <p class="etiqueta-tema">{nombreTema(pregunta.tema)}</p>
      <h1 id="enunciado" tabindex="-1" use:enfocar>{pregunta.texto}</h1>
      <!-- La explicación se muestra siempre: qué hay hoy y qué supone cada respuesta -->
      <div class="contexto">
        <p class="contexto-titulo">Para entenderlo</p>
        <p class="contexto-texto">{pregunta.contexto}</p>
        <dl class="efectos">
          <div>
            <dt>Si estás de acuerdo</dt>
            <dd>{pregunta.de_acuerdo}</dd>
          </div>
          <div>
            <dt>Si estás en desacuerdo</dt>
            <dd>{pregunta.en_desacuerdo}</dd>
          </div>
        </dl>
      </div>
    </div>
  {/key}

  <label class="importante">
    <input type="checkbox" bind:checked={importante} onchange={cambiarImportante} />
    <span>Esto es importante para mí <span class="suave">(cuenta doble)</span></span>
  </label>

  <div class="opciones" role="group" aria-label="Tu respuesta">
    {#each OPCIONES as v (v)}
      <button
        class="boton secundario opcion"
        class:elegida={actual?.valor === v}
        aria-pressed={actual?.valor === v}
        onclick={() => responder(v)}
      >
        {ETIQUETA_RESPUESTA[String(v)]}
      </button>
    {/each}
    <button
      class="boton secundario opcion saltar"
      class:elegida={actual !== undefined && actual.valor === null}
      aria-pressed={actual !== undefined && actual.valor === null}
      onclick={() => responder(null)}
    >
      No lo sé · Saltar
    </button>
  </div>

  <div class="navegacion">
    <button class="boton secundario" onclick={retroceder} disabled={indice === 0}>← Anterior</button>
    {#if actual !== undefined}
      <button class="boton secundario" onclick={avanzar}>
        {indice < preguntas.length - 1 ? 'Siguiente →' : 'Ver resultados →'}
      </button>
    {/if}
  </div>
</section>

<style>
  .progreso {
    margin-bottom: 1.75rem;
  }
  .progreso-texto {
    display: flex;
    justify-content: space-between;
    font-size: 0.92rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
  }
  .porcentaje {
    font-variant-numeric: tabular-nums;
  }
  .pista {
    height: 6px;
    border-radius: 999px;
    background: var(--barra-fondo);
    overflow: hidden;
  }
  /* Se anima transform (no width): no recalcula el diseño y va fluido en móviles */
  .relleno {
    height: 100%;
    background: var(--barra);
    border-radius: inherit;
    transform-origin: left center;
    transition: transform 300ms var(--ease-out);
  }

  /* Cambio de afirmación: fundido corto con un pequeño desplazamiento en el sentido de la navegación.
     Se ve 33 veces por test, así que es breve (180 ms) y no bloquea nada. */
  @keyframes cambiar {
    from {
      opacity: 0;
      transform: translateX(calc(12px * var(--dir, 1)));
    }
  }
  .afirmacion {
    animation: cambiar 180ms var(--ease-out);
  }
  @media (prefers-reduced-motion: reduce) {
    .afirmacion {
      animation-name: fundido;
    }
    .relleno {
      transition: none;
    }
  }

  .etiqueta-tema {
    margin-bottom: 0.8rem;
  }
  h1 {
    font-size: clamp(1.4rem, 5.2vw, 1.9rem);
    line-height: 1.25;
    letter-spacing: -0.02em;
    margin-bottom: 1.1rem;
  }
  .contexto {
    background: var(--superficie);
    border-radius: var(--radio);
    box-shadow: var(--sombra-1);
    outline: 1px solid transparent;
    outline-offset: -1px;
    padding: 1rem 1.15rem;
    margin-bottom: 1.25rem;
  }
  .contexto-titulo {
    margin: 0 0 0.35rem;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--texto-suave);
  }
  .contexto-texto {
    margin: 0;
    font-size: 0.98rem;
    line-height: 1.55;
  }
  /* Qué supone cada respuesta: dos líneas cortas separadas del contexto por un filete */
  .efectos {
    margin: 0.9rem 0 0;
    padding-top: 0.85rem;
    border-top: 1px solid var(--borde);
    display: grid;
    gap: 0.6rem;
  }
  .efectos dt {
    font-size: 0.85rem;
    font-weight: 700;
  }
  .efectos dd {
    margin: 0.1rem 0 0;
    font-size: 0.98rem;
    line-height: 1.5;
  }
  @media (min-width: 640px) {
    .efectos {
      grid-template-columns: 1fr 1fr;
      gap: 1.25rem;
    }
    /* Mismo orden que los botones: el desacuerdo a la izquierda */
    .efectos > div:first-child {
      order: 2;
    }
  }

  /* «Importante» como una píldora que cambia de aspecto al marcarla */
  .importante {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    min-height: 44px;
    padding: 0.4rem 1rem 0.4rem 0.8rem;
    margin-bottom: 1.25rem;
    border-radius: 999px;
    background: var(--superficie-2);
    cursor: pointer;
    font-size: 0.95rem;
    transition:
      background-color 150ms ease,
      box-shadow 150ms ease;
  }
  .importante:has(input:checked) {
    background: var(--superficie);
    box-shadow: 0 0 0 1.5px var(--texto);
  }
  .importante input {
    width: 1.2rem;
    height: 1.2rem;
    margin: 0;
    accent-color: var(--acento);
  }

  .opciones {
    display: grid;
    gap: 0.55rem;
    margin-bottom: 1.5rem;
  }
  .opcion {
    min-height: 52px;
  }
  .opcion.elegida {
    background: var(--acento);
    color: var(--acento-texto);
    box-shadow: none;
  }
  /* Saltar no es una respuesta: se separa y se distingue de la escala */
  .opciones .saltar {
    margin-top: 0.35rem;
    background: transparent;
    box-shadow: inset 0 0 0 1px var(--borde);
    color: var(--texto-suave);
  }
  .opciones .saltar.elegida {
    background: var(--acento);
    color: var(--acento-texto);
    box-shadow: none;
  }
  @media (hover: hover) and (pointer: fine) {
    .opcion.elegida:hover,
    .opciones .saltar.elegida:hover {
      background: var(--acento-hover);
    }
  }
  @media (min-width: 640px) {
    .opciones {
      grid-template-columns: repeat(5, 1fr);
    }
    .opciones .saltar {
      grid-column: 1 / -1;
      justify-self: center;
      min-width: 12rem;
    }
    .opcion {
      font-size: 0.95rem;
      padding: 0.6em 0.5em;
      text-align: center;
      min-height: 64px;
    }
  }
  .navegacion {
    display: flex;
    justify-content: space-between;
    gap: 0.6rem;
    flex-wrap: wrap;
  }
</style>
