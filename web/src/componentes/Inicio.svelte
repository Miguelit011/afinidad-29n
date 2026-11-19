<script lang="ts">
  import { enfocar } from '../lib/enfocar';
  import { preguntas, partidos } from '../lib/datos';
  import Urna from './Urna.svelte';

  let { onEmpezar, onMetodologia }: { onEmpezar: () => void; onMetodologia: () => void } = $props();
</script>

<!--
  Entrada (solo la ve quien llega, una vez por visita). Coreografía:
  titular = protagonista (0 ms, sube 12 px) · etiqueta de fecha = decoración (solo fundido, a la vez)
  entradilla 70 ms · aviso 110 ms · botón 140 ms (huecos decrecientes: se lee como una ola, no como una cola).
  Lo que queda por debajo no se mueve.
-->
<section aria-labelledby="titulo-inicio" class="inicio">
  <div class="portada">
    <div class="ilustracion">
      <Urna />
    </div>
    <div class="texto-portada">
    <p class="etiqueta-tema aparece" style="--desde: 0px">Elecciones generales · 29 de noviembre de 2026</p>
    <h1 id="titulo-inicio" tabindex="-1" use:enfocar class="aparece" style="--desde: 12px">
      ¿Con qué programa electoral coincides más?
    </h1>
    <p class="entradilla suave aparece" style="--retraso: 70ms; --desde: 8px">
      Responde a {preguntas.length} afirmaciones sobre medidas concretas y descubre tu afinidad con los programas de
      {partidos.length} candidaturas, en global y tema a tema.
    </p>

    <div class="aviso aparece" role="note" style="--retraso: 110ms; --desde: 6px">
      <svg class="aviso-icono" viewBox="0 0 20 20" aria-hidden="true" focusable="false">
        <circle cx="10" cy="10" r="8.25" fill="none" stroke="currentColor" stroke-width="1.5" />
        <path d="M10 9v5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
        <circle cx="10" cy="6.2" r="1" fill="currentColor" />
      </svg>
      <p>
        <strong>Mide afinidad con programas, no es una recomendación de voto.</strong> Solo tiene en cuenta lo que dicen
        los programas electorales oficiales, no declaraciones ni trayectorias.
      </p>
    </div>

    <div class="accion aparece" style="--retraso: 140ms; --desde: 6px">
      <button class="boton empezar" onclick={onEmpezar}>
        Empezar el test
        <svg class="flecha" viewBox="0 0 20 20" aria-hidden="true" focusable="false">
          <path d="M4 10h11m-4.5-4.5L15 10l-4.5 4.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </button>
      <p class="meta suave">{preguntas.length} afirmaciones · menos de 10 minutos · anónimo</p>
    </div>
    </div>
  </div>

  <h2>Cómo funciona</h2>
  <ol class="pasos">
    <li class="tarjeta">
      <span class="numero" aria-hidden="true">1</span>
      <p>Lee cada afirmación y di si estás de acuerdo o no. Puedes saltarla y marcar las que son importantes para ti.</p>
    </li>
    <li class="tarjeta">
      <span class="numero" aria-hidden="true">2</span>
      <p>
        Cada partido tiene una postura en cada afirmación, respaldada por una <strong>cita literal de su programa</strong>
        con su página. Si el programa no dice nada, el partido «no se pronuncia».
      </p>
    </li>
    <li class="tarjeta">
      <span class="numero" aria-hidden="true">3</span>
      <p>Al final verás tu afinidad con cada programa y podrás comprobar cada cita en el PDF original.</p>
    </li>
  </ol>

  <h2>Neutralidad y privacidad</h2>
  <ul class="garantias">
    <li>
      <svg class="check" viewBox="0 0 20 20" aria-hidden="true" focusable="false">
        <path d="M5 10.5l3.2 3.2L15 7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
      <span>Las afirmaciones están redactadas sin palabras cargadas; la mitad parten de propuestas de un bloque y la mitad del otro.</span>
    </li>
    <li>
      <svg class="check" viewBox="0 0 20 20" aria-hidden="true" focusable="false">
        <path d="M5 10.5l3.2 3.2L15 7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
      <span>
        Los partidos aparecen en orden aleatorio y con el mismo tratamiento. Sus logotipos, tomados de su propio
        programa, solo sirven para identificarlos en los resultados.
      </span>
    </li>
    <li>
      <svg class="check" viewBox="0 0 20 20" aria-hidden="true" focusable="false">
        <path d="M5 10.5l3.2 3.2L15 7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
      <span>
        Todo se calcula en tu navegador. No hay servidor, base de datos, cookies ni analítica, y no guardamos tus
        respuestas. Tampoco publicamos estadísticas de quienes usan la web.
      </span>
    </li>
  </ul>
  <p>
    <button class="enlace-boton" onclick={onMetodologia}>Lee la metodología completa</button>: fuentes, criterios,
    fórmula y limitaciones.
  </p>
</section>

<style>
  .portada {
    padding: 0.5rem 0 1rem;
    margin-bottom: 1.5rem;
  }
  .ilustracion {
    width: 132px;
    margin-bottom: 1rem;
  }
  /* En escritorio: texto a la izquierda y urna a la derecha */
  @media (min-width: 760px) {
    .portada {
      display: grid;
      grid-template-columns: 1fr 230px;
      gap: 2.5rem;
      align-items: center;
    }
    .ilustracion {
      order: 2;
      width: 100%;
      margin: 0;
    }
  }
  .etiqueta-tema {
    margin-bottom: 1rem;
  }
  h1 {
    font-size: clamp(2rem, 7.5vw, 3.1rem);
    letter-spacing: -0.03em;
    line-height: 1.08;
    margin-bottom: 0.9rem;
  }
  .entradilla {
    font-size: clamp(1.1rem, 3.2vw, 1.25rem);
    line-height: 1.5;
    max-width: 38rem;
    margin-bottom: 1.6rem;
  }
  .aviso p {
    margin: 0;
  }
  .accion {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  .empezar {
    width: 100%;
    min-height: 56px;
    font-size: 1.1rem;
  }
  .flecha {
    width: 1.15rem;
    height: 1.15rem;
    transition: transform 200ms var(--ease-out);
  }
  @media (hover: hover) and (pointer: fine) {
    .empezar:hover .flecha {
      transform: translateX(3px);
    }
  }
  .meta {
    margin: 0;
    font-size: 0.92rem;
    text-align: center;
  }
  @media (min-width: 560px) {
    .accion {
      flex-direction: row;
      align-items: center;
      gap: 1.1rem;
    }
    .empezar {
      width: auto;
      min-width: 14rem;
    }
    .meta {
      text-align: left;
    }
  }
  h2 {
    font-size: 1.3rem;
    margin-top: 2.5rem;
  }
  .pasos {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 0.75rem;
  }
  .pasos li {
    display: flex;
    align-items: flex-start;
    gap: 0.9rem;
  }
  /* En escritorio, tres columnas con el número encima */
  @media (min-width: 720px) {
    .pasos {
      grid-template-columns: repeat(3, 1fr);
    }
    .pasos li {
      flex-direction: column;
      gap: 0.6rem;
    }
  }
  .pasos p {
    margin: 0;
    font-size: 0.98rem;
  }
  .numero {
    display: inline-grid;
    place-items: center;
    width: 2rem;
    height: 2rem;
    border-radius: 999px;
    background: var(--acento);
    color: var(--acento-texto);
    font-weight: 700;
    font-size: 0.95rem;
    font-variant-numeric: tabular-nums;
    flex-shrink: 0;
  }
  .garantias {
    list-style: none;
    padding: 0;
    margin: 0 0 1.2rem;
  }
  .garantias li {
    display: flex;
    gap: 0.6rem;
    margin-bottom: 0.7rem;
  }
  .check {
    width: 1.25rem;
    height: 1.25rem;
    flex-shrink: 0;
    margin-top: 0.2rem;
  }
</style>
