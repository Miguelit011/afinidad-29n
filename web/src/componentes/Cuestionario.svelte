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
  let verContexto = $state(false);

  // Al cambiar de pregunta, se recupera lo que la persona marcó (si vuelve atrás).
  $effect.pre(() => {
    importante = respuestas[preguntas[indice].id]?.importante ?? false;
    verContexto = false;
  });

  function responder(valor: Valor | null) {
    respuestas[pregunta.id] = { valor, importante };
    avanzar();
  }

  function avanzar() {
    if (indice < preguntas.length - 1) {
      indice += 1;
      window.scrollTo({ top: 0 });
    } else {
      onTerminar();
    }
  }

  function retroceder() {
    if (indice > 0) indice -= 1;
  }

  function cambiarImportante() {
    // Si ya había respuesta, se actualiza su peso sin obligar a responder de nuevo.
    if (actual) respuestas[pregunta.id] = { ...actual, importante };
  }
</script>

<section aria-labelledby="enunciado" class="cuestionario">
  <div class="progreso">
    <span id="texto-progreso">Afirmación {indice + 1} de {preguntas.length}</span>
    <progress max={preguntas.length} value={indice + 1} aria-labelledby="texto-progreso"></progress>
  </div>

  {#key indice}
    <p class="tema suave">{nombreTema(pregunta.tema)}</p>
    <h1 id="enunciado" tabindex="-1" use:enfocar>{pregunta.texto}</h1>
  {/key}

  <div class="contexto">
    <button
      class="enlace-boton"
      aria-expanded={verContexto}
      aria-controls="contexto-texto"
      onclick={() => (verContexto = !verContexto)}
    >
      {verContexto ? 'Ocultar contexto' : 'Contexto'}
    </button>
    <div id="contexto-texto" hidden={!verContexto}>
      <p class="tarjeta">{pregunta.contexto}</p>
    </div>
  </div>

  <label class="importante">
    <input type="checkbox" bind:checked={importante} onchange={cambiarImportante} />
    Esto es importante para mí <span class="suave">(cuenta doble)</span>
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
      Saltar
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
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    margin-bottom: 1.5rem;
    font-size: 0.95rem;
  }
  progress {
    width: 100%;
    height: 8px;
    appearance: none;
    border: none;
    border-radius: 4px;
    background: var(--barra-fondo);
    overflow: hidden;
  }
  progress::-webkit-progress-bar {
    background: var(--barra-fondo);
  }
  progress::-webkit-progress-value {
    background: var(--barra);
  }
  progress::-moz-progress-bar {
    background: var(--barra);
  }
  .tema {
    margin-bottom: 0.3rem;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  h1 {
    font-size: clamp(1.35rem, 5vw, 1.8rem);
    margin-bottom: 1rem;
  }
  .contexto {
    margin-bottom: 1rem;
  }
  .contexto .tarjeta {
    margin-top: 0.6rem;
  }
  .importante {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    min-height: 44px;
    margin-bottom: 1rem;
    cursor: pointer;
  }
  .importante input {
    width: 1.3rem;
    height: 1.3rem;
    accent-color: var(--acento);
  }
  .opciones {
    display: grid;
    gap: 0.6rem;
    margin-bottom: 1.5rem;
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
    }
  }
  .opcion.elegida {
    background: var(--acento);
    color: var(--acento-texto);
    border-color: var(--acento);
  }
  .navegacion {
    display: flex;
    justify-content: space-between;
    gap: 0.6rem;
    flex-wrap: wrap;
  }
</style>
