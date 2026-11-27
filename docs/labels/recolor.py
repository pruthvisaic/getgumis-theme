# Recolour the gummies in the bottle photo (outside the label area) to a target colour ramp.
from PIL import Image, ImageFilter
import numpy as np, sys
src, out, name = sys.argv[1], sys.argv[2], sys.argv[3]
RAMPS = {  # (t, rgb) stops, t = normalised gummy luminance
  'red':  [(0, (60, 0, 6)), (0.35, (175, 8, 22)), (0.7, (235, 45, 50)), (1, (255, 165, 160))],
  'blue': [(0, (12, 52, 85)), (0.35, (45, 125, 175)), (0.7, (95, 170, 210)), (1, (195, 232, 246))],
}
b = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
R, G, B = b[..., 0], b[..., 1], b[..., 2]
chroma = (R + B) / 2 - G
w = np.clip((chroma - 4) / 9, 0, 1)
H, W = w.shape
yy, xx = np.mgrid[0:H, 0:W]
region = ((yy > 440) & (yy < 645) | (yy > 1672) & (yy < 1860)) & (xx > 585) & (xx < 1415)
L0 = 0.3 * R + 0.59 * G + 0.11 * B
inner = (xx > 625) & (xx < 1375)
w = np.maximum(w, np.clip((48 - L0) / 18, 0, 1) * inner)   # near-black gummies
w = w * np.clip((215 - L0) / 30, 0, 1)                     # keep pale glass untouched
w = w * region
w = np.asarray(Image.fromarray((w * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))).astype(np.float32) / 255
L = 0.3 * R + 0.59 * G + 0.11 * B
t = np.clip((L - 8) / 150, 0, 1) ** 0.8
stops = RAMPS[name]
ts = np.array([s[0] for s in stops]); cs = np.array([s[1] for s in stops], np.float32)
new = np.stack([np.interp(t, ts, cs[:, k]) for k in range(3)], -1)
res = b * (1 - w[..., None]) + new * w[..., None]
Image.fromarray(np.clip(res, 0, 255).astype(np.uint8)).save(out, quality=95)
print('ok', out)
