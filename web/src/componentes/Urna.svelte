<!--
  Ilustración de la portada: una urna translúcida con sobres sepia dentro y un sobre que entra por la
  ranura. Decorativa (aria-hidden). Animación única al llegar: la urna se funde y el sobre cae a la
  ranura 250 ms después, con ease-out (rápido al principio, suave al encajar). Movimiento reducido: solo fundido.
-->
<script lang="ts">
  // Componente sin estado: solo dibuja la ilustración.
</script>

<svg class="urna" viewBox="0 0 220 200" aria-hidden="true" focusable="false">
  <!-- sombra en el suelo -->
  <ellipse cx="110" cy="189" rx="80" ry="7" class="sombra" />

  <!-- sobres ya depositados, vistos a través del cristal -->
  <g class="dentro">
    <rect x="48" y="150" width="50" height="32" rx="3" transform="rotate(-8 73 166)" class="sobre" />
    <rect x="96" y="154" width="50" height="30" rx="3" transform="rotate(6 121 169)" class="sobre" />
    <rect x="132" y="146" width="44" height="34" rx="3" transform="rotate(-14 154 163)" class="sobre" />
    <path d="M52 154l23 13 23-17" transform="rotate(-8 73 166)" class="solapa" />
  </g>

  <!-- cuerpo de cristal -->
  <rect x="30" y="72" width="160" height="112" rx="14" class="cristal" />
  <path d="M44 92l22-14M44 108l40-26" class="brillo" />

  <!-- rótulo -->
  <rect x="78" y="116" width="64" height="30" rx="7" class="rotulo" />
  <text x="110" y="137" text-anchor="middle" class="rotulo-texto">29N</text>

  <!-- sobre que entra por la ranura (detrás de la tapa) -->
  <g class="sobre-cae">
    <rect x="84" y="4" width="52" height="64" rx="4" class="sobre" />
    <path d="M84 9l26 20 26-20" class="solapa" />
  </g>

  <!-- tapa con ranura -->
  <rect x="20" y="58" width="180" height="20" rx="8" class="tapa" />
  <rect x="72" y="65" width="76" height="6" rx="3" class="ranura" />
</svg>

<style>
  .urna {
    display: block;
    width: 100%;
    height: auto;
    overflow: visible;
    animation: fundido 400ms ease both;
  }
  .sombra {
    fill: var(--texto);
    opacity: 0.08;
  }
  .sobre {
    fill: var(--sepia);
    stroke: var(--sepia-oscuro);
    stroke-width: 1.5;
  }
  .solapa {
    fill: none;
    stroke: var(--sepia-oscuro);
    stroke-width: 1.5;
    stroke-linejoin: round;
  }
  .cristal {
    fill: var(--superficie);
    fill-opacity: 0.45;
    stroke: var(--texto);
    stroke-opacity: 0.75;
    stroke-width: 2.5;
  }
  .brillo {
    stroke: var(--superficie);
    stroke-width: 4;
    stroke-linecap: round;
    opacity: 0.9;
  }
  .rotulo {
    fill: var(--superficie);
    stroke: var(--borde);
    stroke-width: 1.5;
  }
  .rotulo-texto {
    fill: var(--texto);
    font: 700 17px system-ui, sans-serif;
    letter-spacing: 0.02em;
  }
  .tapa {
    fill: var(--acento);
  }
  .ranura {
    fill: var(--fondo);
    opacity: 0.85;
  }

  /* El sobre cae a la ranura una vez: es el gesto que resume la web (votar) */
  .sobre-cae {
    animation: caer 700ms var(--ease-out) 250ms both;
  }
  @keyframes caer {
    from {
      opacity: 0;
      transform: translateY(-34px);
    }
  }
  @media (prefers-reduced-motion: reduce) {
    .sobre-cae {
      animation: fundido 300ms ease both;
    }
  }
</style>
