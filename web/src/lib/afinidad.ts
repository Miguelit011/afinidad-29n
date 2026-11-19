/**
 * Cálculo de afinidad entre las respuestas de una persona y las posturas de los
 * partidos. Función pura: no lee ni escribe estado, no hace E/S.
 *
 * Para cada partido, solo sobre las preguntas que la persona ha respondido (no
 * saltado) y en las que el partido tiene postura (no null):
 *
 *   afinidad = Σ w · (1 − |u − p| / 4) / Σ w
 *
 * u ∈ {-2..2} es la respuesta, p ∈ {-2..2} la postura del partido y w = 2 si la
 * persona marcó la pregunta como importante, 1 si no. Se devuelve en porcentaje.
 * Si no hay ninguna pregunta válida, la afinidad es null (no 0).
 */

export type Valor = -2 | -1 | 0 | 1 | 2;

export interface Respuesta {
  /** null = pregunta saltada */
  valor: Valor | null;
  importante: boolean;
}

export interface PreguntaCalculo {
  id: string;
  tema: string;
  posturas: Record<string, { valor: Valor | null }>;
}

export interface ResultadoPartido {
  partido: string;
  /** 0–100, o null si no hay ninguna pregunta válida */
  afinidad: number | null;
  /** preguntas respondidas por la persona en las que el partido se pronuncia */
  validas: number;
  /** preguntas respondidas (no saltadas) por la persona */
  respondidas: number;
  /** validas / respondidas (0–1), o null si la persona no ha respondido nada */
  cobertura: number | null;
  /** afinidad (0–100 o null) por tema */
  porTema: Record<string, number | null>;
}

export function calcularAfinidad(
  preguntas: readonly PreguntaCalculo[],
  respuestas: Readonly<Record<string, Respuesta | undefined>>,
  partidos: readonly string[],
): ResultadoPartido[] {
  const respondidas = preguntas.filter((q) => {
    const r = respuestas[q.id];
    return r !== undefined && r.valor !== null;
  });
  const temas = [...new Set(preguntas.map((q) => q.tema))];

  return partidos.map((partido) => {
    let num = 0;
    let den = 0;
    let validas = 0;
    const porTemaAcc = new Map<string, { num: number; den: number }>(temas.map((t) => [t, { num: 0, den: 0 }]));

    for (const q of respondidas) {
      const p = q.posturas[partido]?.valor ?? null;
      if (p === null) continue;
      const r = respuestas[q.id] as Respuesta;
      const u = r.valor as Valor;
      const w = r.importante ? 2 : 1;
      const s = 1 - Math.abs(u - p) / 4;
      num += w * s;
      den += w;
      validas += 1;
      const acc = porTemaAcc.get(q.tema)!;
      acc.num += w * s;
      acc.den += w;
    }

    const porTema: Record<string, number | null> = {};
    for (const [t, acc] of porTemaAcc) porTema[t] = acc.den > 0 ? (100 * acc.num) / acc.den : null;

    return {
      partido,
      afinidad: den > 0 ? (100 * num) / den : null,
      validas,
      respondidas: respondidas.length,
      cobertura: respondidas.length > 0 ? validas / respondidas.length : null,
      porTema,
    };
  });
}
