import json,re,math,sys
t=open('template.html',encoding='utf8').read()
pts=[(m.group(1),m.group(2),float(m.group(3)),float(m.group(4))) for m in re.finditer(r'kk:"([^"]+)",ru:"([^"]+)",lat:([\d.]+),lon:([\d.]+)',t)]
A=json.load(open('areas.json',encoding='utf8'))['elements']
def pip(lat,lon,g):
  c=False;n=len(g)
  for i in range(n):
    a,b=g[i],g[i-1]
    if (a['lat']>lat)!=(b['lat']>lat) and lon<(b['lon']-a['lon'])*(lat-a['lat'])/(b['lat']-a['lat'])+a['lon']: c=not c
  return c
def area(g):
  s=0
  for i in range(len(g)):
    a,b=g[i],g[i-1]; s+=(b['lon']-a['lon'])*(b['lat']+a['lat'])
  return abs(s)/2*111000*111000*0.639
def dist(lat,lon,g):
  return min(math.hypot((p['lat']-lat)*111000,(p['lon']-lon)*71000) for p in g)
for kk,ru,lat,lon in pts:
  c=[]
  for e in A:
    g=e.get('geometry');
    if not g or len(g)<4: continue
    tg=e['tags'];inside=pip(lat,lon,g);d=0 if inside else dist(lat,lon,g)
    if d<40: c.append((round(d),int(area(g)),e['id'],tg.get('name',''),tg.get('amenity') or tg.get('tourism') or tg.get('historic') or tg.get('leisure') or tg.get('building')))
  c.sort(key=lambda x:(x[0],x[1]))
  print(kk,'|',c[:4])
