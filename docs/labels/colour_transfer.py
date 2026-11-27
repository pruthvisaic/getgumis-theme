"""Colours the gummies in the HD bottle photo from Suplify's own (lower-resolution) render of the
same bottle with red or blue gummies: colour and translucency from Suplify, fine detail from the HD photo.
Usage: python3 colour_transfer.py bottle.jpg suplify.webp out.jpg
"""
import sys
import cv2
import numpy as np

hi_path, lo_path, out_path = sys.argv[1:4]
hi = cv2.imread(hi_path)
lo = cv2.imread(lo_path)
g_hi = cv2.cvtColor(hi, cv2.COLOR_BGR2GRAY)
g_lo = cv2.cvtColor(lo, cv2.COLOR_BGR2GRAY)

# 1. register the Suplify shot onto the HD photo (scale + offset by template matching)
tpl = g_lo[60:780, 230:610]
best = None
for s in np.arange(2.50, 2.60, 0.002):
    t = cv2.resize(tpl, None, fx=s, fy=s, interpolation=cv2.INTER_CUBIC)
    r = cv2.matchTemplate(g_hi, t, cv2.TM_CCOEFF_NORMED)
    _, mv, _, ml = cv2.minMaxLoc(r)
    if best is None or mv > best[0]:
        best = (mv, s, ml)
score, s, (ox, oy) = best
M = np.float32([[s, 0, ox - 230 * s], [0, s, oy - 60 * s]])
up = cv2.warpAffine(lo, M, (hi.shape[1], hi.shape[0]), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
print('match', round(score, 4), 'scale', round(s, 3))

# 2. combine in Lab: chroma from Suplify, lightness from Suplify + HD high-frequency detail
lab_hi = cv2.cvtColor(hi, cv2.COLOR_BGR2LAB).astype(np.float32)
lab_up = cv2.cvtColor(up, cv2.COLOR_BGR2LAB).astype(np.float32)
L_hi = lab_hi[..., 0]
detail = L_hi - cv2.GaussianBlur(L_hi, (0, 0), 3.0)
L = lab_up[..., 0] + detail * 0.9
ab = cv2.GaussianBlur(lab_up[..., 1:], (0, 0), 1.2)
lab = np.dstack([np.clip(L, 0, 255), ab])
rec = cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)

# 3. only inside the gummy areas (above and below the label), soft mask from Suplify's colourfulness
H, W = g_hi.shape
yy, xx = np.mgrid[0:H, 0:W]
region = (((yy > 430) & (yy < 648)) | ((yy > 1670) & (yy < 1865))) & (xx > 580) & (xx < 1420)
chroma = np.hypot(lab_up[..., 1] - 128, lab_up[..., 2] - 128)
w_sup = np.clip((chroma - 8) / 14, 0, 1)
# also every pixel that is a (purple) gummy in the HD photo, so no purple shows through in the shadows
B, G, R = [hi[..., i].astype(np.float32) for i in range(3)]
L0 = 0.3 * R + 0.59 * G + 0.11 * B
w_orig = np.maximum(np.clip(((R + B) / 2 - G - 4) / 9, 0, 1), np.clip((48 - L0) / 18, 0, 1) * ((xx > 625) & (xx < 1375)))
w_orig *= np.clip((215 - L0) / 30, 0, 1)
w = np.maximum(w_sup, w_orig) * region
w = cv2.GaussianBlur(w.astype(np.float32), (0, 0), 1.5)[..., None]
out = hi.astype(np.float32) * (1 - w) + rec * w
cv2.imwrite(out_path, np.clip(out, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 95])
print('ok', out_path)
