"""Collect candidate images from Wikimedia (free licenses only).
python -I fetch_images.py  -> writes candidates.json and img_raw/*.jpg
"""
import json, time, urllib.request, urllib.parse, os, re, sys

UA = {"User-Agent": "aktobe-map-builder/1.0 (educational school project)"}
def api(host, **p):
    p.update(format="json")
    url = f"https://{host}/w/api.php?" + urllib.parse.urlencode(p)
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            time.sleep(3 * (i + 1))
    return {}

PERSONS = {  # key -> list of (wiki host, title)
    "abai": [("ru.wikipedia.org", "Абай Кунанбаев")],
    "aliya": [("ru.wikipedia.org", "Молдагулова, Алия Нурмухамбетовна")],
    "zhubanov": [("kk.wikipedia.org", "Ахмет Жұбанов"), ("ru.wikipedia.org", "Жубанов, Ахмет Куанович")],
    "doszhanova": [("ru.wikipedia.org", "Досжанова, Аккагаз")],
    "baiganin": [("ru.wikipedia.org", "Байганин, Нурпеис")],
    "patsaev": [("en.wikipedia.org", "Viktor Patsayev"), ("kk.wikipedia.org", "Виктор Пацаев")],
    "akhtanov": [("kk.wikipedia.org", "Тахауи Ахтанов"), ("ru.wikipedia.org", "Ахтанов, Тахави")],
    "shangytbaev": [("kk.wikipedia.org", "Қастек Шаңғытбаев")],
}
out = {"persons": {}, "places": {}}
for key, tries in PERSONS.items():
    for host, title in tries:
        d = api(host, action="query", redirects=1, prop="pageimages", piprop="name", titles=title)
        pages = d.get("query", {}).get("pages", {})
        name = next((p.get("pageimage") for p in pages.values() if p.get("pageimage")), None)
        if name:
            out["persons"][key] = name
            break
        time.sleep(1)
    print("person", key, out["persons"].get(key))

# places: Commons files geotagged near the point
t = open("template.html", encoding="utf8").read()
pts = [(m.group(1), float(m.group(2)), float(m.group(3))) for m in re.finditer(r'kk:"([^"]+)",ru:"[^"]+",lat:([\d.]+),lon:([\d.]+)', t)]
for kk, lat, lon in pts:
    d = api("commons.wikimedia.org", action="query", list="geosearch", gsnamespace=6, gscoord=f"{lat}|{lon}", gsradius=120, gslimit=12)
    files = [g["title"][5:] for g in d.get("query", {}).get("geosearch", [])]
    out["places"][kk] = files
    print("place", kk, len(files))
    time.sleep(0.5)
json.dump(out, open("candidates.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
