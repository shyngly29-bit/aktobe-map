"""Builds the SVG base map of Aktobe from OSM JSON (Overpass `out geom`).
Usage: python -I build_base.py base.json out_svg.txt
"""
import json, sys, math

LON0, LON1 = 57.125, 57.25
LAT0, LAT1 = 50.249, 50.325
KX = 12800.0
KY = KX / math.cos(math.radians(50.29))
W = (LON1 - LON0) * KX
H = (LAT1 - LAT0) * KY

def P(lat, lon):
    return ((lon - LON0) * KX, (LAT1 - lat) * KY)

def dp(pts, tol):
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    dx, dy = b[0]-a[0], b[1]-a[1]
    L = math.hypot(dx, dy) or 1e-9
    imax, dmax = 0, 0
    for i in range(1, len(pts)-1):
        p = pts[i]
        d = abs(dy*(p[0]-a[0]) - dx*(p[1]-a[1])) / L
        if d > dmax:
            imax, dmax = i, d
    if dmax <= tol:
        return [a, b]
    return dp(pts[:imax+1], tol)[:-1] + dp(pts[imax:], tol)

def path(geom, tol, close=False):
    pts = dp([P(g['lat'], g['lon']) for g in geom], tol)
    s = 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return s + ('Z' if close else '')

def inside(geom, pad=0.01):
    return any(LAT0-pad < g['lat'] < LAT1+pad and LON0-pad < g['lon'] < LON1+pad for g in geom)

data = json.load(open(sys.argv[1], encoding='utf8'))
groups = {k: [] for k in ['water', 'park', 'river', 'stream', 'rail', 'res', 'ter', 'sec', 'pri']}
labels = {}
for e in data['elements']:
    g = e.get('geometry')
    if not g or not inside(g):
        continue
    t = e.get('tags', {})
    hw = t.get('highway')
    if t.get('natural') == 'water':
        groups['water'].append(path(g, 1.0, True))
    elif t.get('leisure') == 'park':
        groups['park'].append(path(g, 1.0, True))
    elif t.get('waterway') == 'river':
        groups['river'].append(path(g, 1.0))
    elif t.get('waterway') == 'stream':
        groups['stream'].append(path(g, 1.0))
    elif t.get('railway') == 'rail':
        groups['rail'].append(path(g, 1.0))
    elif hw in ('residential', 'unclassified', 'pedestrian'):
        groups['res'].append(path(g, 0.8))
    elif hw == 'tertiary':
        groups['ter'].append(path(g, 0.8))
    elif hw == 'secondary':
        groups['sec'].append(path(g, 0.8))
    elif hw in ('primary', 'trunk', 'motorway'):
        groups['pri'].append(path(g, 0.8))
    name = t.get('name:kk') or t.get('name')
    if name and hw in ('primary', 'trunk', 'secondary'):
        pts = [P(p['lat'], p['lon']) for p in g]
        length = sum(math.dist(pts[i], pts[i+1]) for i in range(len(pts)-1))
        if length > labels.get(name, (0,))[0]:
            # keep text upright: run left to right
            if pts[0][0] > pts[-1][0]:
                pts = pts[::-1]
            labels[name] = (length, 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in dp(pts, 3)))

out = []
for k in ['water', 'park', 'river', 'stream', 'rail', 'res', 'ter', 'sec', 'pri']:
    if groups[k]:
        out.append(f'<path class="m-{k}" d="{"".join(groups[k])}"/>')
# rail ties overlay
if groups['rail']:
    out.append(f'<path class="m-rail2" d="{"".join(groups["rail"])}"/>')
lab = sorted(labels.items(), key=lambda kv: -kv[1][0])[:22]
defs = []
texts = []
for i, (name, (length, d)) in enumerate(lab):
    if length < 180:
        continue
    defs.append(f'<path id="st{i}" d="{d}"/>')
    texts.append(f'<text class="m-lbl"><textPath href="#st{i}" startOffset="50%" text-anchor="middle">{name}</textPath></text>')
svg = f'<defs>{"".join(defs)}</defs>' + ''.join(out) + f'<g class="m-lbls">{"".join(texts)}</g>'
open(sys.argv[2], 'w', encoding='utf8').write(svg)
print(f'W={W:.1f} H={H:.1f} bytes={len(svg)} labels={len(texts)}')
