# Builds the getgumis "Dreaming" label range (Sleep, Glow, Power) from sleep-label.html.
t = open('sleep-label.html').read()
L0 = t.index('<section class="side left">'); L1 = t.index('</section>', L0) + 10
R0 = t.index('<section class="side right">'); R1 = t.index('</section>', R0) + 10
sleep_left = t[L0:L1]; sleep_right = t[R0:R1]
logo = '<div class="logo"><span class="get">get</span><span class="gumis">gum<span class="i">ı</span>s</span></div>'


def eyes_closed(y=400):
    return (f'<path d="M190 {y} q90 90 180 0" stroke="#3B0A2A" stroke-width="22" fill="none" stroke-linecap="round"/>'
            f'<path d="M430 {y} q90 90 180 0" stroke="#3B0A2A" stroke-width="22" fill="none" stroke-linecap="round"/>'
            f'<g stroke="#3B0A2A" stroke-width="10" stroke-linecap="round"><line x1="205" y1="{y+32}" x2="190" y2="{y+60}"/>'
            f'<line x1="245" y1="{y+52}" x2="238" y2="{y+82}"/><line x1="595" y1="{y+32}" x2="610" y2="{y+60}"/>'
            f'<line x1="555" y1="{y+52}" x2="562" y2="{y+82}"/></g>')


def eyes_happy(y=430):
    return (f'<path d="M190 {y} q90 -90 180 0" stroke="#3B0A2A" stroke-width="22" fill="none" stroke-linecap="round"/>'
            f'<path d="M430 {y} q90 -90 180 0" stroke="#3B0A2A" stroke-width="22" fill="none" stroke-linecap="round"/>')


def sparkle(x, y, s=1, c="#D6246E"):
    return (f'<path transform="translate({x} {y}) scale({s})" d="M0 -30 C 4 -6, 6 -4, 30 0 C 6 4, 4 6, 0 30 '
            f'C -4 6, -6 4, -30 0 C -6 -4, -4 -6, 0 -30 Z" fill="{c}"/>')


def eyes_power(y=410):
    return (f'<circle cx="280" cy="{y}" r="34" fill="#3B0A2A"/><circle cx="520" cy="{y}" r="34" fill="#3B0A2A"/>'
            f'<circle cx="292" cy="{y-12}" r="10" fill="#fff"/><circle cx="532" cy="{y-12}" r="10" fill="#fff"/>'
            f'<path d="M200 {y-80} L350 {y-50}" stroke="#3B0A2A" stroke-width="20" stroke-linecap="round"/>'
            f'<path d="M600 {y-80} L450 {y-50}" stroke="#3B0A2A" stroke-width="20" stroke-linecap="round"/>')


def cheeks(c, y):
    return f'<ellipse cx="190" cy="{y}" rx="60" ry="34" fill="{c}"/><ellipse cx="610" cy="{y}" rx="60" ry="34" fill="{c}"/>'


bubble = '<circle cx="560" cy="300" r="14" fill="#fff"/><circle cx="600" cy="250" r="22" fill="#fff"/><ellipse cx="660" cy="170" rx="110" ry="80" fill="#fff"/>'
dream_bear = ('<g transform="translate(615 128) scale(.3)"><circle cx="70" cy="60" r="34" fill="#D6246E"/>'
              '<circle cx="230" cy="60" r="34" fill="#D6246E"/><circle cx="150" cy="120" r="90" fill="#D6246E"/></g>')
dream_mirror = ('<g transform="translate(660 165)"><ellipse rx="34" ry="44" fill="#FFD3E2" stroke="#D6246E" stroke-width="10"/>'
                '<rect x="-7" y="44" width="14" height="30" rx="7" fill="#D6246E"/>'
                '<path d="M-14 -18 q8 -14 22 -12" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/></g>')
dream_dumbbell = ('<g transform="translate(660 172)" fill="#FF8A3D"><rect x="-50" y="-7" width="100" height="14" rx="7" fill="#3B0A2A"/>'
                  '<rect x="-70" y="-30" width="22" height="60" rx="8"/><rect x="48" y="-30" width="22" height="60" rx="8"/>'
                  '<rect x="-86" y="-20" width="16" height="40" rx="6"/><rect x="70" y="-20" width="16" height="40" rx="6"/></g>')

TBC = '<span class="tbc">[TO COMPLETE]</span>'
WARN = ('<div class="warn"><h3>Warnings</h3><p class="small">Do not exceed the recommended daily dose. Keep out of reach of '
        'young children. Food supplements should not be used as a substitute for a varied and balanced diet and a healthy '
        'lifestyle.</p><p class="small" style="font-weight:500;margin-top:6px">{extra}</p></div>')


def left(use, ingr, extra, weight):
    return (f'<section class="side left"><div class="block"><h3>Recommended use</h3><p>{use}</p></div>'
            f'<div class="block"><h3>Ingredients</h3><p class="small">{ingr}</p></div>{WARN.format(extra=extra)}'
            '<p class="small">Store in a cool, dry, dark place.</p><div class="meta">'
            f'<div class="net">60 gummies <span>{weight}</span><span class="small" style="margin-top:6px">Lot &amp; best before: see bottom of container</span></div>'
            '<div class="barcode">EAN-13 barcode<br>[TO COMPLETE]</div></div></section>')


def right(desc, rows, dose):
    trs = ''
    for n, v, p, hl in rows:
        cls = ' class="hl"' if hl else ''
        trs += f'<tr{cls}><td>{n}</td><td>{v}</td><td>{p}</td></tr>'
    return (f'<section class="side right"><p class="desc">{desc}</p><div class="block"><table><thead><tr>'
            f'<th>Per daily dose<br>({dose})</th><th>Amount</th><th>% NRV*</th></tr></thead><tbody>{trs}</tbody></table></div>'
            '<p class="foot">* NRV: nutrient reference values, Regulation (EU) No 1169/2011.<br>** No NRV established.</p>'
            '<div class="company"><div><b>[TO COMPLETE: company name]</b><br>[TO COMPLETE: street address]<br>[TO COMPLETE: postcode, city], France</div>'
            '<div style="text-align:right;white-space:nowrap"><b>getgumis.com</b><br>Contact: [TO COMPLETE]</div></div></section>')


products = {
    'sleep': dict(name='Sleep', bg='#C9D9F5',
                  face=eyes_closed() + cheeks('#FF9EC4', 510)
                  + '<path d="M370 510 q30 22 60 0" stroke="#3B0A2A" stroke-width="12" fill="none" stroke-linecap="round"/>'
                  + bubble + dream_bear,
                  left=sleep_left, right=sleep_right),
    'glow': dict(name='Glow', bg='#FFD3E2',
                 face=eyes_happy() + cheeks('#FF8FB8', 500)
                 + '<path d="M350 500 q50 50 100 0" stroke="#3B0A2A" stroke-width="12" fill="none" stroke-linecap="round"/>'
                 + sparkle(150, 330, .9) + sparkle(660, 600, .7, '#FF8A3D') + sparkle(120, 620, .5, '#3B0A2A')
                 + bubble + dream_mirror,
                 left=left('Chew 2 gummies a day. ' + TBC,
                           'Biotin, zinc ' + TBC + ' (full list from the manufacturer, in descending order of weight).',
                           TBC, 'Net weight ' + TBC + ' · 30 servings'),
                 right=right('Food supplement with biotin and zinc. ' + TBC,
                             [('Biotin', TBC + ' µg', TBC, True), ('Zinc', TBC + ' mg', TBC, True), (TBC, '', '', False)],
                             '2 gummies')),
    'power': dict(name='Power', bg='#FFE0C7',
                  face=eyes_power() + cheeks('#FFB38A', 505)
                  + '<path d="M340 500 q60 46 120 0 Z" fill="#3B0A2A"/><path d="M360 506 h80" stroke="#fff" stroke-width="8" stroke-linecap="round"/>'
                  + bubble + dream_dumbbell,
                  left=left(TBC + ' gummies a day, providing 3 g of creatine.',
                            'Creatine monohydrate ' + TBC + ' (full list from the manufacturer, in descending order of weight).',
                            'For adults. ' + TBC, 'Net weight ' + TBC + ' · ' + TBC + ' servings'),
                  right=right('Food supplement with creatine. ' + TBC,
                              [('Creatine', '3 g', '**', True), (TBC, '', '', False)], TBC + ' gummies')),
}

css_front = '''
.front{background:var(--bg)!important}.front::before{display:none}
.front .face{position:absolute;inset:0;width:100%;height:100%}
.front .ftop{position:absolute;top:56px;left:70px;display:flex}
.front .ftop .logo{font-size:68px}
.front .fbot{position:absolute;bottom:52px;left:0;right:0;display:flex;flex-direction:column;align-items:center}
.front .fname{font-family:'Fredoka';font-weight:700;font-size:120px;line-height:.85;letter-spacing:-.03em;color:#3B0A2A}
.front .ftag{margin-top:6px;font-weight:800;font-size:16px;letter-spacing:.16em;text-transform:uppercase;color:#3B0A2A}
'''
for k, p in products.items():
    front = (f'<section class="front" style="--bg:{p["bg"]}"><svg class="face" viewBox="0 0 800 830" aria-hidden="true">{p["face"]}</svg>'
             f'<div class="ftop">{logo}</div><div class="fbot"><div class="fname">{p["name"]}</div>'
             '<div class="ftag">Food supplement · 60 gummies</div></div></section>')
    h = t[:L0] + p['left'] + front + p['right'] + t[R1:]
    h = h.replace('</style>', css_front + '</style>').replace('<title>getgumis Sleep label</title>', f'<title>getgumis {p["name"]} label</title>')
    open(f'range-{k}.html', 'w').write(h)
print('ok')
