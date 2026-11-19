<script lang="ts">
  import Inicio from './componentes/Inicio.svelte';
  import Cuestionario from './componentes/Cuestionario.svelte';
  import Resultados from './componentes/Resultados.svelte';
  import Metodologia from './componentes/Metodologia.svelte';
  import type { Respuesta } from './lib/afinidad';
  import { REPO_URL } from './lib/datos';

  type Pantalla = 'inicio' | 'preguntas' | 'resultados' | 'metodologia';

  // Las respuestas solo viven en memoria: no se guardan en el navegador ni se envían.
  let pantalla = $state<Pantalla>('inicio');
  let anterior = $state<Pantalla>('inicio');
  let respuestas = $state<Record<string, Respuesta>>({});
  let indice = $state(0);

  function ir(destino: Pantalla) {
    if (destino === 'metodologia' && pantalla !== 'metodologia') anterior = pantalla;
    pantalla = destino;
    window.scrollTo({ top: 0 });
  }

  function empezar() {
    respuestas = {};
    indice = 0;
    ir('preguntas');
  }

  function reiniciar() {
    respuestas = {};
    indice = 0;
    ir('inicio');
  }
</script>

<a class="saltar visualmente-oculto" href="#contenido">Saltar al contenido</a>

<header class="cabecera">
  <div class="contenedor fila">
    <span class="marca">
      <!-- Logotipo: una urna estilizada, sin colores -->
      <svg class="logo" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <rect x="3.5" y="9" width="17" height="11.5" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.8" />
        <path d="M8.5 9V4.5h7V9" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" />
        <path d="M8 13h8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
      </svg>
      Afinidad 29N
    </span>
    <nav aria-label="Principal">
      {#if pantalla !== 'metodologia'}
        <button class="enlace-boton" onclick={() => ir('metodologia')}>Metodología</button>
      {/if}
    </nav>
  </div>
</header>

<main id="contenido" class="contenedor">
  {#if pantalla === 'inicio'}
    <Inicio onEmpezar={empezar} onMetodologia={() => ir('metodologia')} />
  {:else if pantalla === 'preguntas'}
    <Cuestionario bind:respuestas bind:indice onTerminar={() => ir('resultados')} />
  {:else if pantalla === 'resultados'}
    <Resultados {respuestas} onReiniciar={reiniciar} onMetodologia={() => ir('metodologia')} />
  {:else}
    <Metodologia onVolver={() => ir(anterior)} />
  {/if}
</main>

<footer class="pie">
  <div class="contenedor">
    <p><strong>Mide afinidad con programas, no es una recomendación de voto.</strong></p>
    <p class="suave">
      Tus respuestas no salen de tu navegador: no hay servidor, cookies, analítica ni almacenamiento. Código y
      datos abiertos en <a href={REPO_URL} rel="noopener noreferrer">GitHub</a>.
    </p>
  </div>
</footer>

<style>
  .saltar:focus {
    position: fixed !important;
    top: 8px;
    left: 8px;
    width: auto;
    height: auto;
    clip: auto;
    padding: 0.5rem 1rem;
    background: var(--superficie);
    z-index: 10;
  }
  /* Cabecera fija translúcida: la navegación queda a mano sin tapar el contenido */
  .cabecera {
    position: sticky;
    top: 0;
    z-index: 5;
    background: color-mix(in srgb, var(--fondo) 80%, transparent);
    backdrop-filter: saturate(1.4) blur(12px);
    -webkit-backdrop-filter: saturate(1.4) blur(12px);
    border-bottom: 1px solid color-mix(in srgb, var(--borde) 70%, transparent);
    margin-bottom: 2rem;
  }
  @supports not (backdrop-filter: blur(1px)) {
    .cabecera {
      background: var(--fondo);
    }
  }
  .fila {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 60px;
  }
  .marca {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 700;
    letter-spacing: -0.01em;
  }
  .logo {
    width: 1.35rem;
    height: 1.35rem;
    flex-shrink: 0;
  }
  nav :global(.enlace-boton) {
    font-size: 0.95rem;
    font-weight: 500;
  }
  main {
    min-height: 60vh;
    padding-bottom: 3rem;
  }
  .pie {
    border-top: 1px solid var(--borde);
    padding: 1.5rem 0 2.5rem;
    font-size: 0.92rem;
  }
  .pie p:last-child {
    margin-bottom: 0;
  }
</style>
