import sys,math
LON0,LAT1=57.125,50.325;KX=12800.0;KY=KX/math.cos(math.radians(50.29))
W=(57.25-LON0)*KX;H=(LAT1-50.249)*KY
t=open('template.html',encoding='utf8').read()
svg=open('base_svg.txt',encoding='utf8').read()
for a,b in {'__SVG__':svg,'__W__':f'{W:.1f}','__H__':f'{H:.1f}','__LON0__':str(LON0),'__LAT1__':str(LAT1),'__KX__':str(KX),'__KY__':f'{KY:.4f}'}.items():t=t.replace(a,b)
open('../aktobe-pamyatniki.html','w',encoding='utf8').write(t)
print(len(t), '__' in t.replace('__proto__',''))
