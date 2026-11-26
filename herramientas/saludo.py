#!/usr/bin/env python3
"""Genera el saludo Win95 del README del perfil (media/saludo.svg) con el texto en trazos (Tahoma de Wine)."""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FUENTES = "/usr/share/wine/fonts/"
REG, BOLD = TTFont(FUENTES + "tahoma.ttf"), TTFont(FUENTES + "tahomabd.ttf")


def texto(font, s, x, y, size, fill, anchor="start"):
    """Devuelve (path, ancho) del texto s con la línea de base en y."""
    gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
    esc = size / font["head"].unitsPerEm
    ancho = sum(hmtx[cmap[ord(c)]][0] for c in s) * esc
    if anchor == "middle":
        x -= ancho / 2
    pen = SVGPathPen(gs)
    cx = x
    for c in s:
        g = cmap[ord(c)]
        gs[g].draw(TransformPen(pen, (esc, 0, 0, -esc, cx, y)))
        cx += hmtx[g][0] * esc
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>', ancho


def bisel(x, y, w, h, hundido=False):
    a, b = ("#808080", "#fff") if hundido else ("#fff", "#000")
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{b}"/>'
            f'<rect x="{x}" y="{y}" width="{w-1}" height="{h-1}" fill="{a}"/>'
            f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="{h-2}" fill="#808080"/>'
            f'<rect x="{x+1}" y="{y+1}" width="{w-3}" height="{h-3}" fill="#dfdfdf"/>'
            f'<rect x="{x+2}" y="{y+2}" width="{w-4}" height="{h-4}" fill="#c0c0c0"/>')


W, H = 600, 300
X, Y, DW, DH = 14, 14, 572, 272
p = []
p.append(bisel(X, Y, DW, DH))
p.append(f'<rect x="{X+4}" y="{Y+4}" width="{DW-8}" height="34" fill="#000080"/>')
p.append(texto(BOLD, "FeroxShark.exe", X + 14, Y + 28, 20, "#fff")[0])
bx = X + DW - 36
p.append(bisel(bx, Y + 9, 26, 24))
p.append(texto(BOLD, "×", bx + 13, Y + 28, 22, "#000", "middle")[0])
# ícono de información
ix, iy = X + 62, Y + 96
p.append(f'<path d="M{ix-8} {iy+26} l-6 18 l20 -14 z" fill="#fff" stroke="#000" stroke-width="2" stroke-linejoin="round"/>')
p.append(f'<circle cx="{ix}" cy="{iy}" r="30" fill="#fff" stroke="#000" stroke-width="2"/>')
p.append(f'<path d="M{ix-9} {iy+26} l-5 14 l16 -11 z" fill="#fff"/>')
p.append(texto(BOLD, "i", ix, iy + 15, 44, "#0000c8", "middle")[0])
tx = X + 118
p.append(texto(BOLD, "Hi, I'm Ferox.", tx, Y + 104, 40, "#000")[0])
p.append(texto(REG, "I build tools for Linux", tx, Y + 148, 26, "#000")[0])
p.append(texto(REG, "and AI agent workflows.", tx, Y + 182, 26, "#000")[0])
okw, okh = 132, 42
okx, oky = X + (DW - okw) // 2, Y + DH - okh - 22
p.append(f'<rect x="{okx-1}" y="{oky-1}" width="{okw+2}" height="{okh+2}" fill="#000"/>')
p.append(bisel(okx, oky, okw, okh))
p.append(f'<rect x="{okx+7}" y="{oky+7}" width="{okw-14}" height="{okh-14}" fill="none" stroke="#000" stroke-width="1.5" stroke-dasharray="2 2"/>')
p.append(texto(REG, "OK", okx + okw / 2, oky + 29, 22, "#000", "middle")[0])
dialogo = "".join(p)

# glitch breve: el diálogo tiembla y dos franjas de color cruzan, ~0,3 s cada 6 s
glitch = f'''<g opacity="0">
<animate attributeName="opacity" values="0;0;1;0;1;0;0" keyTimes="0;.9;.91;.93;.95;.97;1" dur="6s" repeatCount="indefinite"/>
<rect x="{X-6}" y="{Y+70}" width="{DW*0.62:.0f}" height="12" fill="#ff2fd0" opacity=".75"/>
<rect x="{X+DW*0.35:.0f}" y="{Y+150}" width="{DW*0.6:.0f}" height="8" fill="#2fffa0" opacity=".7"/>
</g>'''
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="FeroxShark.exe. Hi, I'm Ferox. I build tools for Linux and AI agent workflows.">
<title>Hi, I'm Ferox. I build tools for Linux and AI agent workflows.</title>
<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;5 0;-4 0;0 0;0 0" keyTimes="0;.9;.92;.94;.96;1" dur="6s" repeatCount="indefinite"/>{dialogo}</g>
{glitch}
</svg>
'''
sal = sys.argv[1] if len(sys.argv) > 1 else "saludo.svg"
open(sal, "w").write(svg)
print(sal, len(svg), "bytes")
