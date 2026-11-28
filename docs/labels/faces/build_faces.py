"""Builds snippets/gumis-bottle-face.liquid: animated face overlays for the built-in bottle photos.

The bottle photos (assets/getgumis-*-bottle-*.webp) are rendered from the final labels with the
face removed (eyes, cheeks, mouth, sparkles); this script draws those features as SVG in the
photo's pixel space (829 x 1704 crop), following the cylinder of the jar, so CSS can animate them.
Geometry comes from docs/labels/wrap.py (label area x 598-1403, y 642-1675, scale 1.2458).
"""
import math, os

CX, R, SCALE, Y0 = 1000.5, 402.5, 1034 / 830, 642
OX, OY, W, H = 586, 150, 829, 1704


def place(ax, ay, inner, cls=''):
    a = (ax - 400) * SCALE / R
    x = CX + R * math.sin(a) - OX
    y = Y0 + ay * SCALE - OY
    sx = SCALE * math.cos(a)
    c = f' class="{cls}"' if cls else ''
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({sx:.4f} {SCALE:.4f}) translate({-ax} {-ay})">'
            f'<g{c}>{inner}</g></g>')


def star(x, y, s, c):
    return (f'<path transform="translate({x} {y}) scale({s})" d="M0 -30 C 4 -6, 6 -4, 30 0 C 6 4, 4 6, 0 30 '
            f'C -4 6, -6 4, -30 0 C -6 -4, -4 -6, 0 -30 Z" fill="{c}"/>')


def faces():
    out = {}
    b = '#3A5BD9'
    lash = lambda pts: ''.join(f'<line x1="{a}" y1="{bb}" x2="{c}" y2="{d}"/>' for a, bb, c, d in pts)
    awake = lambda cx: (f'<g class="f-pupil"><circle cx="{cx}" cy="425" r="30" fill="{b}"/>'
                        f'<circle cx="{cx + 10}" cy="414" r="9" fill="#fff"/></g>')
    out['sleep'] = ''.join([
        place(280, 425, awake(280), 'f-open'),
        place(520, 425, awake(520), 'f-open'),
        place(280, 430, f'<path d="M190 400 q90 90 180 0" stroke="{b}" stroke-width="22" fill="none" stroke-linecap="round"/>'
              f'<g stroke="{b}" stroke-width="10" stroke-linecap="round">{lash([(205,432,190,460),(245,452,238,482)])}</g>', 'f-breathe f-closed'),
        place(520, 430, f'<path d="M430 400 q90 90 180 0" stroke="{b}" stroke-width="22" fill="none" stroke-linecap="round"/>'
              f'<g stroke="{b}" stroke-width="10" stroke-linecap="round">{lash([(595,432,610,460),(555,452,562,482)])}</g>', 'f-breathe f-closed'),
        place(190, 510, '<ellipse cx="190" cy="510" rx="60" ry="34" fill="#C9D9F5"/>', 'f-blush'),
        place(610, 510, '<ellipse cx="610" cy="510" rx="60" ry="34" fill="#C9D9F5"/>', 'f-blush'),
        place(400, 515, f'<path d="M370 510 q30 22 60 0" stroke="{b}" stroke-width="12" fill="none" stroke-linecap="round"/>', 'f-snore'),
        place(400, 522, f'<ellipse cx="400" cy="522" rx="22" ry="26" fill="{b}"/>', 'f-yawn'),
        place(165, 330, f'<text x="165" y="345" font-family="Fredoka, sans-serif" font-weight="700" font-size="58" fill="{b}" text-anchor="middle">z</text>', 'f-z f-z1'),
        place(165, 330, f'<text x="165" y="345" font-family="Fredoka, sans-serif" font-weight="700" font-size="72" fill="{b}" text-anchor="middle">z</text>', 'f-z f-z2'),
        place(165, 330, f'<text x="165" y="345" font-family="Fredoka, sans-serif" font-weight="700" font-size="88" fill="{b}" text-anchor="middle">Z</text>', 'f-z f-z3'),
    ])
    g = '#D6246E'
    out['glow'] = ''.join([
        place(280, 400, f'<path d="M190 430 q90 -90 180 0" stroke="{g}" stroke-width="22" fill="none" stroke-linecap="round"/>', 'f-squint'),
        place(520, 400, f'<path d="M430 430 q90 -90 180 0" stroke="{g}" stroke-width="22" fill="none" stroke-linecap="round"/>', 'f-wink'),
        place(190, 500, '<ellipse cx="190" cy="500" rx="60" ry="34" fill="#FFD3E2"/>', 'f-blush'),
        place(610, 500, '<ellipse cx="610" cy="500" rx="60" ry="34" fill="#FFD3E2"/>', 'f-blush'),
        place(400, 512, f'<path d="M350 500 q50 50 100 0" stroke="{g}" stroke-width="12" fill="none" stroke-linecap="round"/>', 'f-grin'),
        place(150, 330, star(150, 330, 0.9, g), 'f-twinkle f-t1'),
        place(660, 600, star(660, 600, 0.7, '#FF8A3D'), 'f-twinkle f-t2'),
        place(120, 620, star(120, 620, 0.5, g), 'f-twinkle f-t3'),
        place(400, 300, f'<path d="M400 330 C 360 300, 360 260, 400 275 C 440 260, 440 300, 400 330 Z" fill="{g}"/>', 'f-heart'),
    ])
    o = '#E8641A'
    out['power'] = ''.join([
        place(280, 410, f'<g class="f-pupil"><circle cx="280" cy="410" r="34" fill="{o}"/><circle cx="292" cy="398" r="10" fill="#fff"/></g>', 'f-look'),
        place(520, 410, f'<g class="f-pupil"><circle cx="520" cy="410" r="34" fill="{o}"/><circle cx="532" cy="398" r="10" fill="#fff"/></g>', 'f-look'),
        place(275, 345, f'<path d="M200 330 L350 360" stroke="{o}" stroke-width="20" stroke-linecap="round"/>', 'f-brow f-brow-l'),
        place(525, 345, f'<path d="M600 330 L450 360" stroke="{o}" stroke-width="20" stroke-linecap="round"/>', 'f-brow f-brow-r'),
        place(190, 505, '<ellipse cx="190" cy="505" rx="60" ry="34" fill="#FFE0C7"/>', 'f-blush'),
        place(610, 505, '<ellipse cx="610" cy="505" rx="60" ry="34" fill="#FFE0C7"/>', 'f-blush'),
        place(150, 330, f'<path d="M150 300 q-22 34 0 46 q22 -12 0 -46 Z" fill="#7EC8F0"/>', 'f-sweat'),
        place(400, 512, f'<path d="M340 500 q60 46 120 0 Z" fill="{o}"/><path d="M360 506 h80" stroke="#fff" stroke-width="8" stroke-linecap="round"/>', 'f-grin2'),
    ])
    return out


f = faces()
liquid = ['{%- comment -%} Generated by docs/labels/faces/build_faces.py: do not edit by hand. {%- endcomment -%}',
          '{%- case name -%}']
for k, svg in f.items():
    liquid.append(f"  {{%- when '{k}' -%}}")
    liquid.append(f'    <svg class="g-face g-face--{k}" viewBox="0 0 {W} {H}" aria-hidden="true" focusable="false">{svg}</svg>')
liquid.append('{%- endcase -%}')
root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
open(os.path.join(root, 'snippets', 'gumis-bottle-face.liquid'), 'w').write('\n'.join(liquid) + '\n')
print('ok')
