import math,re,json,sys
LON0,LAT1=57.125,50.325;KX=12800.0;KY=KX/math.cos(math.radians(50.29))
W=(57.25-LON0)*KX;H=(LAT1-50.249)*KY
src=open('template.html',encoding='utf8').read()
tours=re.search(r'const TOURS=\{.*?\n\};',src,re.S).group(0)
pdata=re.search(r'const P=\[.*?\n\];',src,re.S).group(0)
t=open('premium5.html',encoding='utf8').read()
rep={'__SVG__':open('base2_svg.txt',encoding='utf8').read(),'__TOURS__':tours,'__PDATA__':pdata,'__EXTRA__':open('extra.json',encoding='utf8').read(),
 '__STREETS__':open('streets.json',encoding='utf8').read(),'__STORIES__':json.dumps(json.load(open('stories.json',encoding='utf8')),ensure_ascii=False),
 '__DET__':open('details.json',encoding='utf8').read(),'__CRED__':json.dumps(json.load(open('credits.json',encoding='utf8')),ensure_ascii=False),
 '__W__':f'{W:.1f}','__H__':f'{H:.1f}','__LON0__':str(LON0),'__LAT1__':str(LAT1),'__KX__':str(KX),'__KY__':f'{KY:.4f}'}
for a,b in rep.items(): t=t.replace(a,b)
open('../aktobe-pamyatniki-premium.html','w',encoding='utf8').write('<meta charset="utf-8">'+chr(10)+'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'+chr(10)+t)
open('../_preview.html','w',encoding='utf8').write('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'+t)
print(len(t)//1024,'KB',re.findall(r'__[A-Z0-9]+__',t))
