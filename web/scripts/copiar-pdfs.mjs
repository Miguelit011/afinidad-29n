// Copia los programas en PDF a public/programas/ para que los enlaces
// «.pdf#page=N» de la web funcionen. Se ejecuta antes de dev y de build.
import { copyFileSync, mkdirSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const raiz = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const origen = join(raiz, 'Programas_Electorales');
const destino = join(raiz, 'web', 'public', 'programas');

mkdirSync(destino, { recursive: true });
const pdfs = readdirSync(origen).filter((f) => f.toLowerCase().endsWith('.pdf'));
for (const f of pdfs) copyFileSync(join(origen, f), join(destino, f));
console.log(`PDF copiados a public/programas/: ${pdfs.join(', ')}`);
