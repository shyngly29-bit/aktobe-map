"""TEDx-inspired promo for «Ақтөбе ескерткіштері» (Kazakh captions, no voice).
python -I make_video.py OUT.mp4
Black stage, big white type, one red accent. No TED logo or slogan.
"""
import sys, os, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = sys.argv[1]
W, H, FPS = 1920, 1080, 30
BG = (10, 10, 10)
WHITE = (245, 245, 242)
GREY = (150, 150, 146)
RED = (226, 39, 35)
FB = 'C:/Windows/Fonts/segoeuib.ttf'
FR = 'C:/Windows/Fonts/segoeui.ttf'
_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]

def ease(x): x = max(0., min(1., x)); return 1 - (1 - x) ** 3
def inout(x): x = max(0., min(1., x)); return x * x * (3 - 2 * x)
def fade(t, a, b, fi=.5, fo=.5):
    """opacity of an element visible on [a,b] with fade in/out"""
    if t < a or t > b: return 0.
    return min(1., (t - a) / fi if fi else 1., (b - t) / fo if fo else 1.)

def shot(name, maxw=None):
    im = Image.open(os.path.join(HERE, 'shots', name + '.png')).convert('RGB')
    return im

def rounded(im, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.size[0] - 1, im.size[1] - 1], r, fill=255)
    out = Image.new('RGBA', im.size); out.paste(im, (0, 0), m); return out

def framed(im, w, r=18):
    """screenshot -> rounded card with soft shadow, width w"""
    h = int(im.size[1] * w / im.size[0])
    card = rounded(im.resize((w, h), Image.LANCZOS), r)
    pad = 60
    sh = Image.new('RGBA', (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([pad, pad + 14, pad + w, pad + h + 14], r, fill=(0, 0, 0, 170))
    sh = sh.filter(ImageFilter.GaussianBlur(26))
    sh.alpha_composite(card, (pad, pad))
    return sh

def text_layer(lines, size, color=WHITE, bold=True, align='center', spacing=1.12):
    """returns RGBA image of text; lines may contain (text,color) segments"""
    f = font(FB if bold else FR, size)
    rows = []
    for ln in lines:
        segs = ln if isinstance(ln, list) else [(ln, color)]
        wsum = sum(f.getlength(s) for s, _ in segs)
        rows.append((segs, wsum))
    lh = int(size * spacing)
    tw = int(max(w for _, w in rows)) + 8
    img = Image.new('RGBA', (tw, lh * len(rows) + int(size * .3)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, (segs, wsum) in enumerate(rows):
        x = (tw - wsum) / 2 if align == 'center' else 0
        for s, c in segs:
            d.text((x, i * lh), s, font=f, fill=c)
            x += f.getlength(s)
    return img

def put(frame, layer, cx, cy, alpha=1., dy=0., anchor='center'):
    if alpha <= 0: return
    l = layer
    if alpha < 1:
        l = layer.copy(); a = l.getchannel('A').point(lambda v: int(v * alpha)); l.putalpha(a)
    x = int(cx - l.size[0] / 2) if anchor == 'center' else int(cx)
    y = int(cy - l.size[1] / 2 + dy)
    frame.alpha_composite(l, (x, y))

def red_dot(frame, cx, cy, r, alpha=1.):
    if alpha <= 0: return
    lay = Image.new('RGBA', (int(r * 2 + 4), int(r * 2 + 4)), (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse([2, 2, 2 + r * 2, 2 + r * 2], fill=RED + (int(255 * alpha),))
    frame.alpha_composite(lay, (int(cx - r - 2), int(cy - r - 2)))

def red_bar(frame, x, y, w, h=8, alpha=1.):
    if alpha <= 0 or w <= 0: return
    lay = Image.new('RGBA', (int(w), h), RED + (int(255 * alpha),)); frame.alpha_composite(lay, (int(x), int(y)))

def caption(frame, t, a, b, title, sub=None, y=930):
    al = fade(t, a, b, .4, .4)
    if al <= 0: return
    put(frame, text_layer([title], 54), W / 2, y, al, dy=(1 - ease((t - a) / .5)) * 18)
    if sub: put(frame, text_layer([sub], 32, GREY, bold=False), W / 2, y + 62, al)

# ---------- assets ----------
S = {n: shot(n) for n in ['d_home', 'd_place', 'd_street', 'd_search', 'd_walk', 'd_nopanel', 'd_nurgasyr', 'p_home', 'p_card']}
FR_CARD = {}
def card(name, w):
    k = (name, w)
    if k not in FR_CARD: FR_CARD[k] = framed(S[name], w, 16 if w > 600 else 26)
    return FR_CARD[k]
figs = []
for n in ['abai', 'aliya', 'eset']:
    fg = Image.open(os.path.join(ROOT, 'img', 'fig', n + '.webp')).convert('RGBA')
    fg.thumbnail((480, 720), Image.LANCZOS); figs.append(fg)
qr = Image.open(os.path.join(HERE, 'qr.png')).convert('RGBA').resize((260, 260), Image.NEAREST)
TL = {}
def T(key, lines, size, color=WHITE, bold=True, align='center'):
    if key not in TL: TL[key] = text_layer(lines, size, color, bold, align)
    return TL[key]

# ---------- timeline (seconds) ----------
DUR = 84.0
def render(t):
    fr = Image.new('RGBA', (W, H), BG + (255,))
    # 1. opening question
    if t < 13:
        red_dot(fr, W / 2, 300, 10 + 8 * ease(t / 1.2), fade(t, 0, 12.6, .6, .6))
        put(fr, T('o1', ['Біз күн сайын'], 112), W / 2, 470, fade(t, .8, 7.6, .6, .5), dy=(1 - ease((t - .8) / .7)) * 24)
        put(fr, T('o2', ['тарихтың жанынан өтеміз.'], 112), W / 2, 600, fade(t, 2.2, 7.6, .6, .5), dy=(1 - ease((t - 2.2) / .7)) * 24)
        put(fr, T('o3', ['Бірақ олардың', [('есімін', RED), (' білеміз бе?', WHITE)]], 128), W / 2, 540, fade(t, 8.1, 12.7, .6, .5), dy=(1 - ease((t - 8.1) / .7)) * 24)
    # 2. numbers
    if 12.8 < t < 23.2:
        a = fade(t, 13, 18, .5, .5)
        if a > 0:
            n = int(round(38 * ease((t - 13.2) / 1.6)))
            put(fr, text_layer([str(n)], 300, RED), W / 2, 440, a)
            put(fr, T('n1', ['тарихи-мәдени нысан'], 64), W / 2, 680, a)
            put(fr, T('n1s', ['ескерткіштер · мемориалдар · ғибадатханалар · мұражайлар'], 34, GREY, False), W / 2, 760, a)
        b = fade(t, 18.2, 23, .5, .5)
        if b > 0:
            n = int(round(350 * ease((t - 18.4) / 1.6)))
            put(fr, text_layer([str(n)], 300, RED), W / 2, 440, b)
            put(fr, T('n2', ['көше атауы картада'], 64), W / 2, 680, b)
            put(fr, T('n2s', ['әр атаудың артында — тағдыр, тарих, есім'], 34, GREY, False), W / 2, 760, b)
    # 3. app reveal
    if 23 < t < 31.2:
        put(fr, T('r1', ['Сондықтан біз жасадық'], 60, GREY, False), W / 2, 150, fade(t, 23.2, 31, .5, .4))
        put(fr, T('r2', [[('Ақтөбе ', WHITE), ('ескерткіштері', RED)]], 96), W / 2, 250, fade(t, 23.8, 31, .5, .4))
        a = fade(t, 24.6, 31, .7, .4)
        if a > 0:
            z = 1 + .04 * (t - 24.6) / 6.4
            c = card('d_home', int(1180 * z))
            put(fr, c, W / 2, 680, a, dy=(1 - ease((t - 24.6) / .9)) * 60)
    # 4-6. app features: screenshot left, statement right
    feats = [(31, 38, 'd_place', ['Ескерткішті бас —', [('тарихын', RED), (' оқы.', WHITE)]], ['Әр нысан туралы қысқаша', 'және толық мәлімет']),
             (38, 45, 'd_street', ['Әр көшенің —', [('өз тарихы', RED), ('.', WHITE)]], ['Инженерная → Орджоникидзе →', 'Көкжар → Шоқан Уәлиханов']),
             (45, 51.5, 'd_search', ['Бұрынғы атауымен', [('де ', WHITE), ('табылады', RED), ('.', WHITE)]], ['«Ленин» деп жазсаңыз —', 'Әйтеке би көшесі шығады'])]
    for a0, b0, nm, lines, sub in feats:
        if a0 - .2 < t < b0 + .2:
            al = fade(t, a0, b0, .5, .45)
            z = 1 + .035 * (t - a0) / (b0 - a0)
            put(fr, card(nm, int(1000 * z)), 600, 540, al, dy=(1 - ease((t - a0) / .8)) * 40)
            tl = T('f' + nm, lines, 66, align='left')
            put(fr, tl, 1190, 470, al, dy=(1 - ease((t - a0 - .2) / .8)) * 24, anchor='left')
            put(fr, T('fs' + nm, sub, 34, GREY, False, 'left'), 1190, 620, al, anchor='left')
            red_bar(fr, 1192, 380, 120 * ease((t - a0 - .3) / .6), 8, al)
    # 7. historical figures
    if 51.3 < t < 58.4:
        al = fade(t, 51.5, 58.2, .5, .45)
        put(fr, T('h1', [[('16 ', RED), ('тарихи тұлға', WHITE)]], 88), W / 2, 150, al)
        for i, fg in enumerate(figs):
            ai = fade(t, 52 + i * .35, 58.2, .6, .45)
            # soft red floor glow
            put(fr, glow, 520 + i * 440, 930, ai * .9)
            put(fr, fg, 520 + i * 440, 600, ai, dy=(1 - ease((t - 52 - i * .35) / .8)) * 40)
        put(fr, T('h2', ['Көркем реконструкция'], 28, GREY, False), W / 2, 1020, al)
    # 8. phone + languages
    if 58.2 < t < 64.6:
        al = fade(t, 58.4, 64.4, .5, .45)
        put(fr, card('p_home', 330), 420, 545, al, dy=(1 - ease((t - 58.4) / .8)) * 40)
        put(fr, card('p_card', 330), 800, 545, fade(t, 58.8, 64.4, .5, .45), dy=(1 - ease((t - 58.8) / .8)) * 40)
        put(fr, T('m1', ['Телефонда да,', 'компьютерде де.'], 70, align='left'), 1120, 470, al, anchor='left')
        put(fr, T('m2', [[('Қазақша ', RED), ('және орысша.', WHITE)]], 56, align='left'), 1120, 640, al, anchor='left')
    # 9. walk mode
    if 64.4 < t < 70.8:
        al = fade(t, 64.6, 70.6, .5, .45)
        z = 1 + .035 * (t - 64.6) / 6
        put(fr, card('d_walk', int(1000 * z)), 600, 540, al, dy=(1 - ease((t - 64.6) / .8)) * 40)
        put(fr, T('w1', ['Серуенге шық.'], 66, align='left'), 1190, 460, al, anchor='left')
        put(fr, T('w2', ['«Ақтөбенің тарихи тұлғалары»', 'маршруты — 8 аялдама'], 34, GREY, False, 'left'), 1190, 570, al, anchor='left')
        red_bar(fr, 1192, 380, 120 * ease((t - 64.9) / .6), 8, al)
    # 10. closing thought
    if 70.6 < t < 77.4:
        al = fade(t, 70.8, 77.2, .6, .5)
        put(fr, T('c1', ['Тарихи жадыны сақтау —'], 104), W / 2, 470, al, dy=(1 - ease((t - 70.8) / .8)) * 24)
        put(fr, T('c2', [[('әрқайсымыздың ', RED), ('қолымызда.', WHITE)]], 104), W / 2, 610, fade(t, 71.6, 77.2, .6, .5), dy=(1 - ease((t - 71.6) / .8)) * 24)
    # 11. end card
    if t > 77.2:
        al = fade(t, 77.4, DUR + 1, .6, 0)
        red_dot(fr, 300, 330, 14, al)
        put(fr, T('e1', [[('Ақтөбе ', WHITE), ('ескерткіштері', RED)]], 96), 330, 330, al, anchor='left')
        put(fr, T('e2', ['Интерактивті тарихи карта'], 44, GREY, False), 300, 440, al, anchor='left')
        put(fr, T('e3', ['shyngly29-bit.github.io/aktobe-map'], 46), 300, 600, al, anchor='left')
        put(fr, qr, 1560, 470, al)
        put(fr, T('e4', ['Деректер: OpenStreetMap · Wikimedia Commons · visitaktobe.kz'], 26, GREY, False), W / 2, 980, al)
    # final fade to black
    if t > DUR - .8:
        k = (t - (DUR - .8)) / .8
        fr.alpha_composite(Image.new('RGBA', (W, H), BG + (int(255 * min(1, k)),)))
    return fr.convert('RGB')

glow = Image.new('RGBA', (420, 90), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([20, 20, 400, 70], fill=(226, 39, 35, 120))
glow = glow.filter(ImageFilter.GaussianBlur(18))

if __name__ == '__main__':
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    if len(sys.argv) > 2 and sys.argv[2] == 'stills':
        for s in [5, 10, 15, 20, 27, 34, 41, 48, 55, 61, 67, 74, 81]:
            render(s).save(OUT.replace('.mp4', f'_{s:02d}.jpg'), quality=82)
        sys.exit()
    p = subprocess.Popen([ff, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        p.stdin.write(render(i / FPS).tobytes())
        if i % 300 == 0: print(f'{i}/{n}', flush=True)
    p.stdin.close(); p.wait()
    print('done', OUT, os.path.getsize(OUT) // 1024, 'KB')
