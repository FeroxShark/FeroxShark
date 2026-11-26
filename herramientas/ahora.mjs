// Reescribe la lista "Working on" del README: los repos de ahora.json, del último push al más viejo.
// Sólo repos públicos y no archivados. Corre en la Action programada con el GITHUB_TOKEN por defecto.
import { readFile, writeFile } from 'node:fs/promises';

const INICIO = '<!-- ahora:inicio -->';
const FIN = '<!-- ahora:fin -->';
const cfg = JSON.parse(await readFile(new URL('./ahora.json', import.meta.url), 'utf8'));
const headers = { Accept: 'application/vnd.github+json', 'User-Agent': 'perfil-ahora' };
if (process.env.GITHUB_TOKEN) headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;

const filas = [];
for (const p of cfg.repos) {
  const r = await fetch(`https://api.github.com/repos/${cfg.owner}/${p.repo}`, { headers });
  if (r.status === 404) continue; // privado o borrado: no se muestra
  if (!r.ok) throw new Error(`${p.repo}: HTTP ${r.status}`);
  const j = await r.json();
  if (j.private || j.archived) continue;
  filas.push({ ...p, url: j.html_url, pushed: j.pushed_at });
}
filas.sort((a, b) => b.pushed.localeCompare(a.pushed));

// Fecha corta: el año sólo si no es el actual.
const fecha = (d) => {
  const f = new Date(d);
  const anio = f.getUTCFullYear() !== new Date().getUTCFullYear();
  return f.toLocaleDateString('en-US', { month: 'short', day: 'numeric', ...(anio && { year: 'numeric' }), timeZone: 'UTC' });
};
const bloque = [
  INICIO,
  '| Project | Updated |',
  '|:--|:--|',
  ...filas.slice(0, cfg.max).map((f) => `| **[${f.name}](${f.url})**<br><sub>${f.what}</sub> | ${fecha(f.pushed)} |`),
  FIN,
].join('\n');

const ruta = process.argv[2] ?? 'README.md';
const readme = await readFile(ruta, 'utf8');
const i = readme.indexOf(INICIO), k = readme.indexOf(FIN);
if (i < 0 || k < i) throw new Error(`faltan los marcadores ${INICIO} … ${FIN} en ${ruta}`);
const nuevo = readme.slice(0, i) + bloque + readme.slice(k + FIN.length);
if (nuevo !== readme) await writeFile(ruta, nuevo);
console.log(nuevo === readme ? 'sin cambios' : 'actualizado', filas.map((f) => f.repo).join(' '));
