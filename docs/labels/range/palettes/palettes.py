import re
from range_lib import *
PALETTES = {
 'P1': dict(name='Pastel (current)', sleep=('#C9D9F5','#3B0A2A','#FF9EC4'), glow=('#FFD3E2','#3B0A2A','#FF8FB8'), power=('#FFE0C7','#3B0A2A','#FFB38A')),
 'P2': dict(name='Bold brand', sleep=('#3B0A2A','#FFF4EC','#D6246E'), glow=('#D6246E','#FFF4EC','#FF8FB8'), power=('#FF8A3D','#3B0A2A','#FFC7A0')),
 'P3': dict(name='Candy brights', sleep=('#B8A6F0','#2A0A1F','#FF8FB8'), glow=('#FF6FA5','#2A0A1F','#FFC2DA'), power=('#FFD23F','#2A0A1F','#FF9E5E')),
 'P4': dict(name='Night jewels', sleep=('#1E2A5A','#FFF4EC','#6F7FD6'), glow=('#5B1A4A','#FFF4EC','#D6246E'), power=('#0F4C47','#FFF4EC','#3FA89C')),
 'P5': dict(name='Soft earth', sleep=('#C8D5E3','#2E3A4A','#E9B7C2'), glow=('#F1D3C9','#4A2A2A','#E59A9A'), power=('#D9DDB8','#2F3A22','#E5B07A')),
 'P6': dict(name='Cream + colour', sleep=('#FFF4EC','#3A5BD9','#C9D9F5'), glow=('#FFF4EC','#D6246E','#FFD3E2'), power=('#FFF4EC','#E8641A','#FFE0C7')),
 'P7': dict(name='Lavender family', sleep=('#E4DAF7','#3B0A2A','#C9B2F0'), glow=('#C9B2F0','#3B0A2A','#F2A7CC'), power=('#8E6BD1','#FFF4EC','#B79BF0')),
 'P8': dict(name='Sunset', sleep=('#FF8C7A','#3B0A2A','#FFC1B3'), glow=('#E8467C','#FFF4EC','#FF9EC0'), power=('#FFB238','#3B0A2A','#FF7A3D')),
 'P9': dict(name='Fresh mint', sleep=('#BFE9E3','#16413C','#8FD3C9'), glow=('#FFC9DD','#4A1530','#FF9EC0'), power=('#D8F28A','#26330C','#B6DB4F')),
 'P10': dict(name='Neon night', sleep=('#17131C','#5FE3FF','#2A6E86'), glow=('#17131C','#FF5FB8','#7A2A58'), power=('#17131C','#C6FF4A','#5A7A1E')),
 'P11': dict(name='Retro 70s', sleep=('#6E7B4E','#FFF1D6','#A9B57F'), glow=('#C8553D','#FFF1D6','#E89A7F'), power=('#E9A93B','#3B2410','#F4C977')),
 'P12': dict(name='Ice cream', sleep=('#FFF1C9','#4A2E14','#FFD6A0'), glow=('#FFC7D6','#5A1730','#FF9EB8'), power=('#CDEBC4','#24401E','#9ED19A')),
}
faces = {k: products[k]['face'] for k in products}
names = {'sleep': 'Sleep', 'glow': 'Glow', 'power': 'Power'}
def lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return 0.2126*r+0.7152*g+0.0722*b
for pid, pal in PALETTES.items():
    for k in ('sleep','glow','power'):
        bg, ink, cheek = pal[k]
        face = faces[k].replace('#3B0A2A', ink)
        face = re.sub(r'fill="#(FF9EC4|FF8FB8|FFB38A)"', f'fill="{cheek}"', face)
        dark = lum(bg) < 0.35 or lum(ink) > 0.7
        lg = f'<div class="sticker">{logo}</div>' if dark else logo
        front = (f'<section class="front" style="--bg:{bg}"><svg class="face" viewBox="0 0 800 830" aria-hidden="true">{face}</svg>'
                 f'<div class="ftop">{lg}</div><div class="fbot"><div class="fname" style="color:{ink}">{names[k]}</div>'
                 f'<div class="ftag" style="color:{ink}">Food supplement · 60 gummies</div></div></section>')
        h = t[:L0] + products[k]['left'] + front + products[k]['right'] + t[R1:]
        h = h.replace('</style>', css_front + '.front .ftop .sticker{display:inline-flex;align-items:center;background:#fff;border-radius:999px;padding:10px 26px 14px}.front .ftop .sticker .logo{font-size:56px}</style>')
        open(f'pal-{pid}-{k}.html', 'w').write(h)
import json; json.dump({p: v['name'] for p, v in PALETTES.items()}, open('palettes.json', 'w'))
print('ok')
