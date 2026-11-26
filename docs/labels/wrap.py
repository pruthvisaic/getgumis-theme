from PIL import Image, ImageFilter
import numpy as np, sys
bottle=np.asarray(Image.open('bottle.jpg').convert('RGB')).astype(np.float32)
label=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(np.float32)
LH,LW=label.shape[:2]                     # 1660 x 4000 (2x)
x0,x1,y0,y1=598,1403,642,1675
cx=(x0+x1)/2; r=(x1-x0)/2
scale=(y1-y0+1)/(LH/2)                    # photo px per label px (1x)
out=bottle.copy()
ys=np.arange(y0,y1+1); xs=np.arange(x0,x1+1)
X,Y=np.meshgrid(xs,ys)
dx=np.clip((X-cx)/r,-0.9999,0.9999)
arc=r*np.arcsin(dx)                        # arc length on the cylinder (photo px)
u=(LW/2)+arc/scale*2
v=(Y-y0)/scale*2
ui=np.clip(u,0,LW-1); vi=np.clip(v,0,LH-1)
# bilinear sampling
u0=np.floor(ui).astype(int); v0=np.floor(vi).astype(int)
u1=np.clip(u0+1,0,LW-1); v1=np.clip(v0+1,0,LH-1)
fu=(ui-u0)[...,None]; fv=(vi-v0)[...,None]
s=(label[v0,u0]*(1-fu)*(1-fv)+label[v0,u1]*fu*(1-fv)+label[v1,u0]*(1-fu)*fv+label[v1,u1]*fu*fv)
# shading from the blank label in the photo
g=bottle[y0:y1+1,x0:x1+1].mean(axis=2)
ref=np.percentile(g,92)
S=np.clip(g/ref,0.72,1.06)[...,None]
# subtle extra edge darkening for the cylinder
edge=(1-0.10*np.abs(dx)**3)[...,None]
res=np.clip(s*S*edge,0,255)
# soften the left/right silhouette edges (1px blend)
alpha=np.clip((r-np.abs(X-cx))/1.5,0,1)[...,None]
out[y0:y1+1,x0:x1+1]=res*alpha+bottle[y0:y1+1,x0:x1+1]*(1-alpha)
img=Image.fromarray(out.astype(np.uint8))
img.save(sys.argv[2],quality=95)
print('ok',scale)
