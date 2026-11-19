<script lang="ts">
  import { enfocar } from '../lib/enfocar';
  import { preguntas, partidos } from '../lib/datos';

  let { onEmpezar, onMetodologia }: { onEmpezar: () => void; onMetodologia: () => void } = $props();
</script>

<section aria-labelledby="titulo-inicio">
  <p class="suave antetitulo">Elecciones generales · 29 de noviembre de 2026</p>
  <h1 id="titulo-inicio" tabindex="-1" use:enfocar>¿Con qué programa electoral coincides más?</h1>
  <p class="entradilla">
    Responde a {preguntas.length} afirmaciones sobre medidas concretas y descubre tu afinidad con los programas de
    {partidos.length} candidaturas, en global y tema a tema.
  </p>

  <div class="aviso" role="note">
    <strong>Mide afinidad con programas, no es una recomendación de voto.</strong> Solo tiene en cuenta lo que dicen
    los programas electorales oficiales, no declaraciones ni trayectorias.
  </div>

  <button class="boton empezar" onclick={onEmpezar}>Empezar</button>

  <h2>Cómo funciona</h2>
  <ol class="pasos">
    <li>Lee cada afirmación y di si estás de acuerdo o no. Puedes saltarla y marcar las que son importantes para ti.</li>
    <li>
      Cada partido tiene una postura en cada afirmación, respaldada por una <strong>cita literal de su programa</strong>
      con su página. Si el programa no dice nada, el partido «no se pronuncia».
    </li>
    <li>Al final verás tu afinidad con cada programa y podrás comprobar cada cita en el PDF original.</li>
  </ol>

  <h2>Neutralidad y privacidad</h2>
  <ul class="garantias">
    <li>Las afirmaciones están redactadas sin palabras cargadas; la mitad parten de propuestas de un bloque y la mitad del otro.</li>
    <li>Los partidos aparecen en orden aleatorio, sin logos ni colores propios.</li>
    <li>
      Todo se calcula en tu navegador. No hay servidor, base de datos, cookies ni analítica, y no guardamos tus
      respuestas. Tampoco publicamos estadísticas de quienes usan la web.
    </li>
  </ul>
  <p>
    <button class="enlace-boton" onclick={onMetodologia}>Lee la metodología completa</button>: fuentes, criterios,
    fórmula y limitaciones.
  </p>
</section>

<style>
  .antetitulo {
    margin-bottom: 0.3rem;
    font-size: 0.95rem;
  }
  h1 {
    font-size: clamp(1.7rem, 6vw, 2.4rem);
  }
  .entradilla {
    font-size: 1.15rem;
  }
  .empezar {
    width: 100%;
    font-size: 1.15rem;
    margin-bottom: 2rem;
  }
  @media (min-width: 560px) {
    .empezar {
      width: auto;
      min-width: 14rem;
    }
  }
  h2 {
    font-size: 1.25rem;
    margin-top: 1.5rem;
  }
  .pasos li,
  .garantias li {
    margin-bottom: 0.5rem;
  }
</style>
