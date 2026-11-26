from PIL import Image, ImageFilter
import numpy as np, sys
src=Image.open(sys.argv[1]).convert('RGB'); a=np.asarray(src).astype(int)
d=(255-a).max(axis=2)
obj=d>10
H,W=obj.shape
mask=np.zeros((H,W),bool)
rows=[]
for y in range(H):
  xs=np.where(obj[y])[0]
  if len(xs)>40:            # ignore specks / faint shadow
    mask[y,xs.min():xs.max()+1]=True; rows.append(y)
# drop the soft floor shadow: keep rows down to the last row where the object is wide (bottle base)
widths=mask.sum(axis=1)
base=max(y for y in rows if widths[y]>500)
mask[base+1:,:]=False
m=Image.fromarray((mask*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
out=src.copy(); out.putalpha(m)
bbox=out.getbbox(); out=out.crop(bbox)
out.save(sys.argv[2]); print('bbox',bbox,'base',base,out.size)
