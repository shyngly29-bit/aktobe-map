"""OSM streets -> streets.json (names kk/ru, old names, chains in SVG units) and base2_svg.txt (2GIS-like road casing).
python -I build_streets.py
"""
import json, math, re, collections
LON0, LON1, LAT0, LAT1 = 57.125, 57.25, 50.249, 50.325
KX = 12800.0
KY = KX / math.cos(math.radians(50.29))
W, H = (LON1 - LON0) * KX, (LAT1 - LAT0) * KY
def P(lat, lon): return ((lon - LON0) * KX, (LAT1 - lat) * KY)

def dp(pts, tol):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy) or 1e-9
    imax, dmax = 0, 0
    for i in range(1, len(pts)-1):
        d = abs(dy*(pts[i][0]-a[0]) - dx*(pts[i][1]-a[1])) / L
        if d > dmax: imax, dmax = i, d
    if dmax <= tol: return [a, b]
    return dp(pts[:imax+1], tol)[:-1] + dp(pts[imax:], tol)
def inside(g, pad=0.01): return any(LAT0-pad < p['lat'] < LAT1+pad and LON0-pad < p['lon'] < LON1+pad for p in g)
RANK = {'trunk': 4, 'primary': 4, 'motorway': 4, 'secondary': 3, 'tertiary': 2, 'residential': 1, 'unclassified': 1, 'pedestrian': 1}

data = json.load(open('base.json', encoding='utf8'))['elements']
groups = collections.defaultdict(lambda: {'ways': [], 'rank': 0, 'ids': [], 'tags': collections.defaultdict(set)})
cls = collections.defaultdict(list)
for e in data:
    g = e.get('geometry'); t = e.get('tags', {})
    if not g or not inside(g): continue
    hw = t.get('highway')
    if t.get('natural') == 'water': cls['water'].append((g, True)); continue
    if t.get('leisure') == 'park': cls['park'].append((g, True)); continue
    if t.get('waterway') == 'river': cls['river'].append((g, False)); continue
    if t.get('waterway') == 'stream': cls['stream'].append((g, False)); continue
    if t.get('railway') == 'rail': cls['rail'].append((g, False)); continue
    if hw not in RANK: continue
    r = RANK[hw]; cls[{4: 'pri', 3: 'sec', 2: 'ter', 1: 'res'}[r]].append((g, False))
    n = t.get('name')
    if not n: continue
    G = groups[n]; G['ways'].append(g); G['ids'].append(e['id']); G['rank'] = max(G['rank'], r)
    for k, v in t.items():
        if k.startswith(('name', 'old_name', 'wikipedia', 'wikidata')): G['tags'][k].add(v)

def chains(ways):
    segs = [[(round(p['lat'], 6), round(p['lon'], 6)) for p in w] for w in ways]
    out = []
    while segs:
        c = segs.pop(0); changed = True
        while changed:
            changed = False
            for i, s in enumerate(segs):
                if s[0] == c[-1]: c = c + s[1:]
                elif s[-1] == c[-1]: c = c + s[::-1][1:]
                elif s[-1] == c[0]: c = s + c[1:]
                elif s[0] == c[0]: c = s[::-1] + c[1:]
                else: continue
                segs.pop(i); changed = True; break
        out.append(c)
    return out

def one(tags, k):
    v = tags.get(k); return sorted(v)[0] if v else None

streets = []
for n, G in groups.items():
    tg = G['tags']
    kk = one(tg, 'name:kk') or n
    ru = one(tg, 'name:ru') or n
    olds = {}
    for k, vals in tg.items():
        m = re.match(r'old_name(?::(kk|ru|en))?(?::(.+))?$', k)
        if not m: continue
        lang, period = m.group(1) or 'kk', m.group(2) or ''
        if lang == 'en': continue
        olds.setdefault(period, {})[lang] = ' / '.join(sorted(vals))
    ch = []
    for c in chains(G['ways']):
        pts = dp([P(a, b) for a, b in c], 0.6)
        if len(pts) >= 2: ch.append(' '.join(f'{x:.1f},{y:.1f}' for x, y in pts))
    s = {'kk': kk, 'ru': ru, 'r': G['rank'], 'c': ch, 'id': G['ids'][0]}
    if olds: s['old'] = [{'p': p, **v} for p, v in sorted(olds.items())]
    wp = one(tg, 'wikipedia:ru') or one(tg, 'wikipedia')
    if wp: s['wp'] = wp
    streets.append(s)
streets.sort(key=lambda s: -s['r'])
json.dump(streets, open('streets.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))

def path(g, tol, close):
    pts = dp([P(p['lat'], p['lon']) for p in g], tol)
    return 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ('Z' if close else '')
svg = []
def grp(cl, key):
    d = ''.join(path(g, 0.8 if key in ('res', 'ter', 'sec', 'pri') else 1.0, c) for g, c in cls[key])
    return f'<path class="{cl}" d="{d}"/>' if d else ''
D = {k: grp('x', k) for k in cls}
for k in ['water', 'park', 'river', 'stream']: svg.append(D[k].replace('class="x"', f'class="m-{k}"'))
for k in ['res', 'ter', 'sec', 'pri']: svg.append(D[k].replace('class="x"', f'class="m-{k}-c"'))
for k in ['res', 'ter', 'sec', 'pri']: svg.append(D[k].replace('class="x"', f'class="m-{k}"'))
svg.append(D['rail'].replace('class="x"', 'class="m-rail"')); svg.append(D['rail'].replace('class="x"', 'class="m-rail2"'))
open('base2_svg.txt', 'w', encoding='utf8').write(''.join(svg))
print('streets', len(streets), 'json KB', len(json.dumps(streets, ensure_ascii=False)) // 1024, 'svg KB', len(''.join(svg)) // 1024,
      'with old', sum('old' in s for s in streets), 'kk!=name', sum(s['kk'] != s['ru'] for s in streets))
