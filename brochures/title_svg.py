"""The leaflet's "Boiler Care Plans" title as outlined SVG paths with one gradient fill.

Gradient text done with CSS (background-clip: text) leaves hairline seams in some PDF viewers when you zoom,
and gradient-filled live text drops its clip in others. Plain paths with an axial gradient draw the same
everywhere, on screen and in print.
"""
import os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "site", "fonts", "google", "urbanist-v18-L0x-DF02iFML4hGCyMqlbS0.woff2")


def title_svg(lines=("Boiler", "Care Plans"), size=30, leading=1.02, weight=800, c1="#8a3ff5", c2="#1592e6"):
    vf = TTFont(FONT)
    font = instantiateVariableFont(vf, {"wght": weight})
    tmp = os.path.join(HERE, ".urbanist-800.ttf")
    font.flavor = None
    font.save(tmp)
    blob = hb.Blob.from_file_path(tmp)
    hbfont = hb.Font(hb.Face(blob))
    upm = font["head"].unitsPerEm
    gs = font.getGlyphSet()
    names = font.getGlyphOrder()
    scale = size / upm
    shaped = []
    for text in lines:
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(hbfont, buf, {"kern": True, "liga": True})
        shaped.append((buf.glyph_infos, buf.glyph_positions, sum(p.x_advance for p in buf.glyph_positions) * scale))
    os.remove(tmp)
    width = max(w for *_, w in shaped)
    asc = font["hhea"].ascent * scale
    cap = font["OS/2"].sCapHeight * scale
    desc = -font["hhea"].descent * scale
    top = (size * leading - asc - desc) / 2 + asc - cap   # where the capitals sat in a normal line of text
    step = size * leading
    paths = []
    for i, (infos, poss, w) in enumerate(shaped):
        x = (width - w) / 2
        base = cap + i * step
        for info, pos in zip(infos, poss):
            pen = SVGPathPen(gs)
            tp = TransformPen(pen, (scale, 0, 0, -scale, x + pos.x_offset * scale, base - pos.y_offset * scale))
            gs[names[info.codepoint]].draw(tp)
            if pen.getCommands():
                paths.append(pen.getCommands())
            x += pos.x_advance * scale
    height = size * leading * len(lines) - top            # same total height as the old text heading
    label = " ".join(lines)
    return (f'<svg class="htitle" viewBox="0 0 {width:.2f} {height:.2f}" width="{width:.2f}pt" height="{height:.2f}pt" '
            f'role="img" aria-label="{label}"><defs><linearGradient id="hg" x1="0" y1="0" x2="{width:.2f}" y2="{height * .35:.2f}" '
            f'gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>'
            f'</linearGradient></defs><path fill="url(#hg)" d="{" ".join(paths)}"/></svg>'), top


if __name__ == "__main__":
    print(title_svg()[0][:300])
