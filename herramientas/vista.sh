#!/usr/bin/env bash
# Vista previa del README del perfil: lo renderiza con el markdown real de GitHub y saca capturas
# en oscuro y claro, a 1280 (compu) y 390 (celu). Salida: vista/{oscuro,claro}-{1280,390}.png
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p vista
AVATAR=${AVATAR:-$HOME/diseno/maquetas/perfil-github/img/avatar.png}
cp "$AVATAR" vista/avatar.png
CUERPO=$(gh api markdown -f mode=markdown -f text="$(cat README.md)")
for tema in oscuro claro; do
  if [[ $tema == oscuro ]]; then css=github-markdown-dark; bg='#0d1117'; fg='#e6edf3'; mu='#8d96a0'; bd='#30363d'
  else css=github-markdown-light; bg='#ffffff'; fg='#1f2328'; mu='#59636e'; bd='#d1d9e0'; fi
  cat > "vista/$tema.html" <<HTML
<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<base href="../"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/$css.min.css">
<style>body{margin:0;background:$bg;color:$fg;font:14px -apple-system,'Segoe UI',Helvetica,Arial,sans-serif}
.wrap{max-width:1280px;margin:0 auto;padding:24px 32px;display:flex;gap:24px}aside{width:296px;flex:none}
.av{width:296px;height:296px;border-radius:50%;border:1px solid $bd}aside h1{font-size:24px;margin:16px 0 0}
.u{font-size:20px;color:$mu;font-weight:300;margin:0}.bio{font-size:16px;margin:16px 0}.meta{color:$mu;margin:6px 0}
main{flex:1;min-width:0}.box{border:1px solid $bd;border-radius:6px;padding:24px}.box .markdown-body{background:transparent}
.crumb{font-size:12px;color:$mu;margin-bottom:16px}
@media(max-width:767px){.wrap{display:block;padding:16px}aside{width:auto;display:grid;grid-template-columns:64px 1fr;gap:0 12px;margin-bottom:16px}
.av{width:64px;height:64px;grid-row:span 2}aside h1{margin:4px 0 0;font-size:20px}.u{font-size:16px}.bio,.meta{grid-column:span 2}.box{padding:16px}}</style>
<div class="wrap"><aside><img class="av" src="vista/avatar.png"><h1>Ferox</h1><p class="u">FeroxShark</p>
<p class="bio">$(gh api user --jq .bio)</p><p class="meta">Cordoba, Argentina</p></aside>
<main><div class="box"><div class="crumb">FeroxShark / README.md</div><article class="markdown-body">$CUERPO</article></div></main></div>
HTML
  for w in 1280 390; do
    google-chrome-stable --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files \
      --virtual-time-budget=4000 --window-size=$w,6000 --screenshot="vista/$tema-$w.png" "file://$PWD/vista/$tema.html" 2>/dev/null
  done
done
ls -la vista/*.png
