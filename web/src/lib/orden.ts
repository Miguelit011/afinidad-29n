import type { ResultadoPartido } from './afinidad';

/** Fisher–Yates. Devuelve una copia barajada; `azar` se puede inyectar en tests. */
export function barajar<T>(lista: readonly T[], azar: () => number = Math.random): T[] {
  const copia = [...lista];
  for (let i = copia.length - 1; i > 0; i--) {
    const j = Math.floor(azar() * (i + 1));
    [copia[i], copia[j]] = [copia[j], copia[i]];
  }
  return copia;
}

/**
 * Ordena de mayor a menor afinidad. Los empates quedan en orden aleatorio
 * (se baraja antes y la ordenación es estable) y los «sin datos», al final.
 * Se compara con el valor redondeado que se muestra, para que dos partidos que
 * aparecen con el mismo porcentaje se consideren empatados.
 */
export function ordenarPorAfinidad(
  resultados: readonly ResultadoPartido[],
  azar: () => number = Math.random,
): ResultadoPartido[] {
  const clave = (r: ResultadoPartido) => (r.afinidad === null ? -1 : Math.round(r.afinidad));
  return barajar(resultados, azar).sort((a, b) => clave(b) - clave(a));
}
