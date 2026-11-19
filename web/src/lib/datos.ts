import type { Valor } from './afinidad';
import preguntasJson from '../../../data/preguntas.json';
import fuentesJson from '../../../data/textos/fuentes.json';

export interface Postura {
  valor: Valor | null;
  cita: string | null;
  pagina: number | null;
  inferida: boolean;
  nota: string | null;
}

export interface Pregunta {
  id: string;
  tema: string;
  texto: string;
  contexto: string;
  de_acuerdo: string;
  en_desacuerdo: string;
  formulada_desde: string;
  posturas: Record<string, Postura>;
}

export interface Partido {
  id: string;
  nombre: string;
  pdf: string;
}

export interface Tema {
  id: string;
  nombre: string;
}

export interface Fuente {
  partido: string;
  archivo: string;
  sha256: string;
  paginas: number;
  fecha_pdf: string | null;
}

interface Datos {
  version: string;
  partidos: Partido[];
  temas: Tema[];
  preguntas: Pregunta[];
}

const datos = preguntasJson as unknown as Datos;

export const version = datos.version;
export const partidos: Partido[] = datos.partidos;
export const temas: Tema[] = datos.temas;
export const preguntas: Pregunta[] = datos.preguntas;
export const fuentes: Fuente[] = fuentesJson as Fuente[];

export const nombrePartido = (id: string) => partidos.find((p) => p.id === id)?.nombre ?? id;
export const nombreTema = (id: string) => temas.find((t) => t.id === id)?.nombre ?? id;

export const ETIQUETA_RESPUESTA: Record<string, string> = {
  '-2': 'Muy en desacuerdo',
  '-1': 'En desacuerdo',
  '0': 'Neutral',
  '1': 'De acuerdo',
  '2': 'Muy de acuerdo',
};

export const ETIQUETA_POSTURA: Record<string, string> = {
  '-2': 'Muy en contra',
  '-1': 'En contra',
  '0': 'Neutral',
  '1': 'A favor',
  '2': 'Muy a favor',
  null: 'No se pronuncia',
};

export const urlPdf = (partido: string, pagina: number) => {
  const p = partidos.find((x) => x.id === partido);
  return `${import.meta.env.BASE_URL}programas/${p?.pdf ?? `${partido}.pdf`}#page=${pagina}`;
};

// Ficha con el logotipo recortado de la portada o contraportada del propio programa (pipeline/logos.py).
export const urlLogo = (partido: string) => `${import.meta.env.BASE_URL}logos/${partido}.png`;

export const REPO_URL = 'https://github.com/Miguelit011/afinidad-29n';
