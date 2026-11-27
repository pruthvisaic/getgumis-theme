# Builds the gumis Magnesium label (India): full face version + blank-face version for the website overlay.
import re
t = open('get-B-sleep.html').read()
TEAL, CHEEK = '#12898A', '#BFEDE6'
LEAF = 'M0 -30 C 22 -22, 22 22, 0 30 C -22 22, -22 -22, 0 -30 Z'
def leaf(x, y, s, c, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><path d="{LEAF}" fill="{c}"/>'
            f'<path d="M0 -24 L0 24" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".7"/></g>')
bubble = ('<circle cx="560" cy="300" r="14" fill="#fff"/><circle cx="600" cy="250" r="22" fill="#fff"/>'
          '<ellipse cx="660" cy="170" rx="110" ry="80" fill="#fff"/>'
          + leaf(640, 175, 1.25, TEAL, -30) + leaf(690, 160, 1.0, '#5BC8B8', 25))
features = (f'<path d="M215 410 q65 45 130 0" stroke="{TEAL}" stroke-width="22" fill="none" stroke-linecap="round"/>'
            f'<path d="M455 410 q65 45 130 0" stroke="{TEAL}" stroke-width="22" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="190" cy="485" rx="60" ry="34" fill="{CHEEK}"/><ellipse cx="610" cy="485" rx="60" ry="34" fill="{CHEEK}"/>'
            f'<path d="M350 492 q50 42 100 0" stroke="{TEAL}" stroke-width="12" fill="none" stroke-linecap="round"/>'
            + leaf(150, 330, .8, '#5BC8B8', -20) + leaf(660, 600, .65, TEAL, 30) + leaf(120, 620, .5, '#5BC8B8', 10))
TBC = '<span class="tbc">[TBC]</span>'
left = ('<section class="side left"><div class="block"><h3>Directions for use</h3><p>Chew ' + TBC + ' gummies a day, or as directed by a healthcare professional.</p></div>'
        '<div class="block"><h3>Ingredients</h3><p class="small">' + TBC + ' Full ingredient list from the manufacturer, in descending order of weight. Allergens in bold.</p></div>'
        '<div class="warn"><h3>Caution</h3><p class="small">Not to exceed the recommended daily usage. Keep out of reach of children. '
        'Not for medicinal use. Not to be used as a substitute for a varied diet. Pregnant or lactating women, children, and people on medication should consult a doctor before use.</p></div>'
        '<p class="small">Store in a cool, dry place, away from direct sunlight.</p><div class="meta">'
        '<div class="net">Net qty: ' + TBC + ' g <span>' + TBC + ' gummies · ' + TBC + ' servings</span>'
        '<span class="small" style="margin-top:6px">Batch No., Mfg. date &amp; Best before: see bottom of container</span>'
        '<span style="margin-top:8px;font-weight:800;color:#3B0A2A">MRP ₹' + TBC + ' (incl. of all taxes)</span></div>'
        '<div class="barcode">Barcode<br>[TO COMPLETE]</div></div></section>')
right = ('<section class="side right"><div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px">'
         '<p class="desc">Health supplement with magnesium. NOT FOR MEDICINAL USE.</p>'
         '<span class="vegmark" title="Veg mark: confirm with manufacturer"><i></i></span></div>'
         '<div class="block"><table><thead><tr><th>Per serving<br>(' + TBC + ' gummies)</th><th>Amount</th><th>% RDA*</th></tr></thead><tbody>'
         '<tr class="hl"><td>Magnesium (as ' + TBC + ')</td><td>' + TBC + ' mg</td><td>' + TBC + '</td></tr>'
         '<tr><td>Energy</td><td>' + TBC + ' kcal</td><td></td></tr><tr><td>Carbohydrate</td><td>' + TBC + ' g</td><td></td></tr>'
         '<tr><td>of which total sugars</td><td>' + TBC + ' g</td><td></td></tr><tr><td>Protein / Fat</td><td>' + TBC + ' g</td><td></td></tr></tbody></table></div>'
         '<p class="foot">* % RDA as per ICMR-NIN guidelines. [TBC: confirm with manufacturer]</p>'
         '<div class="company" style="display:block;font-size:15px;line-height:1.35"><b>Marketed by:</b> [TO COMPLETE: company name, address] · FSSAI Lic. No. [TO COMPLETE]<br>'
         '<b>Manufactured by:</b> [TO COMPLETE] · FSSAI Lic. No. [TO COMPLETE]<br>'
         '<b>Customer care:</b> [TO COMPLETE: phone / email] · <b>gumis.in</b></div></section>')
def front(face_inner):
    return ('<section class="front" style="--bg:#FFF4EC"><svg class="face" viewBox="0 0 800 830" aria-hidden="true">' + face_inner + '</svg>'
            '<div class="ftop"><div class="logo"><span class="gumis">gum<span class="i">ı</span>s</span></div></div>'
            f'<div class="fbot"><div class="fname" style="color:{TEAL}">Magnesium</div><div class="ftag" style="color:{TEAL}">Health supplement · Gummies</div></div></section>')
css = ('.net .tbc,.net span .tbc{display:inline!important;font-size:inherit}.front .fbot .fname{font-size:96px!important;line-height:1!important}.right .company{font-size:13.5px!important}.right .foot{font-size:14px}.vegmark{flex:none;width:34px;height:34px;border:3px solid #1E8E3E;display:flex;align-items:center;justify-content:center}'
       '.vegmark i{width:16px;height:16px;border-radius:50%;background:#1E8E3E}')
L0 = t.index('<section class="side left">'); R1 = t.index('</section>', t.index('<section class="side right">')) + 10
for name, inner in [('magnesium', features + bubble), ('blank-magnesium', bubble)]:
    h = t[:L0] + left + front(inner) + right + t[R1:]
    h = h.replace('</style>', css + '</style>', 1).replace('<title>getgumis Sleep label</title>', '<title>gumis Magnesium label</title>')
    open(f'{name}.html', 'w').write(h)
print('ok')
