import { describe, expect, it } from 'vitest';
import { calcularAfinidad, type PreguntaCalculo, type Respuesta, type Valor } from './afinidad';
import { barajar, ordenarPorAfinidad } from './orden';
import { preguntas as preguntasReales, partidos as partidosReales } from './datos';

// Datos sintéticos: 4 preguntas, 2 temas, 3 partidos.
const P: PreguntaCalculo[] = [
  { id: 'q1', tema: 'a', posturas: { X: { valor: 2 }, Y: { valor: -2 }, Z: { valor: null } } },
  { id: 'q2', tema: 'a', posturas: { X: { valor: 1 }, Y: { valor: 0 }, Z: { valor: -1 } } },
  { id: 'q3', tema: 'b', posturas: { X: { valor: -2 }, Y: { valor: 2 }, Z: { valor: null } } },
  { id: 'q4', tema: 'b', posturas: { X: { valor: 0 }, Y: { valor: -1 }, Z: { valor: null } } },
];
const PARTIDOS = ['X', 'Y', 'Z'];

const r = (valor: Valor | null, importante = false): Respuesta => ({ valor, importante });
const de = (res: ReturnType<typeof calcularAfinidad>, p: string) => res.find((x) => x.partido === p)!;

/** Responde exactamente lo que dice el partido (y salta donde no se pronuncia). */
function espejo(preguntas: readonly PreguntaCalculo[], partido: string) {
  return Object.fromEntries(preguntas.map((q) => [q.id, r(q.posturas[partido].valor)]));
}

/** Responde lo más lejos posible del partido en cada pregunta. */
function opuesto(preguntas: readonly PreguntaCalculo[], partido: string) {
  return Object.fromEntries(
    preguntas.map((q) => {
      const p = q.posturas[partido].valor;
      return [q.id, r(p === null ? null : p >= 0 ? -2 : 2)];
    }),
  );
}

describe('partido espejo', () => {
  it.each(PARTIDOS)('quien responde como %s obtiene 100 % con ese partido', (p) => {
    expect(de(calcularAfinidad(P, espejo(P, p), PARTIDOS), p).afinidad).toBe(100);
  });

  it.each(partidosReales.map((p) => p.id))('con los datos reales: espejo de %s → 100 %', (p) => {
    const res = calcularAfinidad(preguntasReales, espejo(preguntasReales, p), partidosReales.map((x) => x.id));
    expect(de(res, p).afinidad).toBe(100);
    expect(de(res, p).cobertura).toBe(1);
  });
});

describe('opuesto total', () => {
  it('estar en el extremo contrario en todo da 0 %', () => {
    // Solo preguntas en las que X tiene postura extrema (±2): q1 (+2) y q3 (−2).
    const resp = { q1: r(-2), q3: r(2) };
    const res = calcularAfinidad(P, resp, PARTIDOS);
    expect(de(res, 'X').afinidad).toBe(0);
  });

  it.each(partidosReales.map((p) => p.id))('con los datos reales: opuesto de %s cuando sus posturas son ±2 → 0 %', (p) => {
    const extremas = preguntasReales.filter((q) => Math.abs(q.posturas[p].valor ?? 0) === 2);
    const res = calcularAfinidad(extremas, opuesto(extremas, p), [p]);
    expect(res[0].afinidad).toBe(0);
  });
});

describe('fórmula', () => {
  it('una diferencia de un punto vale 75 %', () => {
    const res = calcularAfinidad(P, { q1: r(1) }, PARTIDOS);
    expect(de(res, 'X').afinidad).toBe(75);
  });

  it('las preguntas saltadas no cuentan', () => {
    const conSaltada = calcularAfinidad(P, { q1: r(2), q2: r(null) }, PARTIDOS);
    const sinResponder = calcularAfinidad(P, { q1: r(2) }, PARTIDOS);
    expect(conSaltada).toEqual(sinResponder);
    expect(de(conSaltada, 'X').respondidas).toBe(1);
  });

  it('las preguntas importantes cuentan el doble', () => {
    // q1: X=2, u=2 → 1;  q3: X=−2, u=2 → 0.
    const normal = calcularAfinidad(P, { q1: r(2), q3: r(2) }, PARTIDOS);
    const importante = calcularAfinidad(P, { q1: r(2, true), q3: r(2) }, PARTIDOS);
    expect(de(normal, 'X').afinidad).toBe(50);
    expect(de(importante, 'X').afinidad).toBeCloseTo((2 * 1 + 1 * 0) / 3 * 100, 10);
  });

  it('marcar como importante una pregunta saltada no tiene efecto', () => {
    const a = calcularAfinidad(P, { q1: r(2), q2: r(null, true) }, PARTIDOS);
    const b = calcularAfinidad(P, { q1: r(2) }, PARTIDOS);
    expect(a).toEqual(b);
  });

  it('las posturas null se excluyen', () => {
    // Z solo se pronuncia en q2 (−1). Responder −1 en q2 y cualquier cosa en el resto → 100 %.
    const res = calcularAfinidad(P, { q1: r(2), q2: r(-1), q3: r(-2), q4: r(2) }, PARTIDOS);
    expect(de(res, 'Z').afinidad).toBe(100);
    expect(de(res, 'Z').validas).toBe(1);
  });
});

describe('cobertura y ausencia de datos', () => {
  it('cobertura = preguntas válidas / respondidas', () => {
    const res = calcularAfinidad(P, { q1: r(0), q2: r(0), q3: r(0), q4: r(null) }, PARTIDOS);
    expect(de(res, 'X').cobertura).toBe(1);
    expect(de(res, 'Z').validas).toBe(1);
    expect(de(res, 'Z').respondidas).toBe(3);
    expect(de(res, 'Z').cobertura).toBeCloseTo(1 / 3, 10);
  });

  it('sin preguntas válidas para un partido, la afinidad es null (no 0)', () => {
    const res = calcularAfinidad(P, { q1: r(2) }, PARTIDOS);
    expect(de(res, 'Z').afinidad).toBeNull();
    expect(de(res, 'Z').cobertura).toBe(0);
  });

  it('sin ninguna respuesta, afinidad y cobertura son null', () => {
    const res = calcularAfinidad(P, {}, PARTIDOS);
    for (const x of res) {
      expect(x.afinidad).toBeNull();
      expect(x.cobertura).toBeNull();
      expect(x.respondidas).toBe(0);
    }
  });

  it('afinidad por tema: null en temas sin datos', () => {
    const res = calcularAfinidad(P, { q1: r(2), q2: r(1) }, PARTIDOS);
    expect(de(res, 'X').porTema).toEqual({ a: 100, b: null });
    expect(de(res, 'Y').porTema.a).toBeCloseTo(((1 - 4 / 4) + (1 - 1 / 4)) / 2 * 100, 10);
  });
});

describe('orden de resultados', () => {
  it('ordena de mayor a menor y deja «sin datos» al final', () => {
    // q1 = 2 → X: 100 %, Y: 0 %, Z: sin datos.
    const res = calcularAfinidad(P, { q1: r(2) }, PARTIDOS);
    for (let i = 0; i < 20; i++) {
      expect(ordenarPorAfinidad(res).map((x) => x.partido)).toEqual(['X', 'Y', 'Z']);
    }
  });

  it('los empates salen en orden aleatorio', () => {
    const empate = ['A', 'B', 'C'].map((partido) => ({
      partido, afinidad: 50, validas: 1, respondidas: 1, cobertura: 1, porTema: {},
    }));
    const vistos = new Set<string>();
    for (let i = 0; i < 200; i++) vistos.add(ordenarPorAfinidad(empate).map((x) => x.partido).join(''));
    expect(vistos.size).toBe(6);
  });

  it('barajar no modifica la lista original y conserva los elementos', () => {
    const lista = [1, 2, 3, 4, 5];
    const b = barajar(lista);
    expect(lista).toEqual([1, 2, 3, 4, 5]);
    expect([...b].sort()).toEqual(lista);
  });
});
