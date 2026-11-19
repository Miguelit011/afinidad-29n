/** Acción de Svelte: mueve el foco al elemento al montarlo (para lectores de pantalla y teclado). */
export function enfocar(nodo: HTMLElement) {
  nodo.focus({ preventScroll: true });
}
