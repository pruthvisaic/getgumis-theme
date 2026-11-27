"""Recolours the white ribbed cap of a bottle photo (2000 x 2000 frame of bottle.jpg), keeping its shading.
Usage: python3 cap_colour.py in.jpg out.jpg '#RRGGBB' [gamma]  (gamma 1.0 for light colours, 2.2 for strong ones)
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, out, hexcol = sys.argv[1:4]
gamma = float(sys.argv[4]) if len(sys.argv) > 4 else 2.2
c = np.array([int(hexcol[i:i + 2], 16) for i in (1, 3, 5)], np.float32)
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
H, W, _ = im.shape
L = im @ np.array([0.299, 0.587, 0.114], np.float32)
d = (255 - im).max(axis=2)
mask = np.zeros((H, W), np.float32)
for y in range(150, 394):
    xs = np.where(d[y] > 12)[0]
    if len(xs) > 40:
        mask[y, xs.min():xs.max() + 1] = 1
# keep the soft shadow line under the cap rim as it is (y > 366 dark band)
mask[367:394, :] *= np.clip((L[367:394, :] - 150) / 60, 0, 1)
m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32)[..., None] / 255
s = np.clip(L / 246.0, 0, 1.08)[..., None]
shade = s ** gamma                                  # ribs and edges stay visible
spec = np.clip((s - 0.985) / 0.1, 0, 1) * 0.35       # a little gloss on the brightest ridges
rec = c * shade * 1.04 + 255 * spec
res = im * (1 - m) + np.clip(rec, 0, 255) * m
Image.fromarray(res.astype(np.uint8)).save(out, quality=95)
print('ok', out)
