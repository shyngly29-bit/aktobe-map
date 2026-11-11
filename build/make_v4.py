"""premium3.html -> premium4.html: collapsible panel, separate history window, light-only theme."""
import re
t = open('premium3.html', encoding='utf8').read()

def rep(a, b, count=1):
    global t
    assert a in t, 'MISSING: ' + a[:80]
    t = t.replace(a, b, count)

# 1. light only: drop dark blocks
t = re.sub(r'@media \(prefers-color-scheme: dark\)\{:root:not\(\[data-theme="light"\]\)\{.*?\}\}\n', '', t, flags=re.S)
t = re.sub(r':root\[data-theme="dark"\]\{.*?\}\n', '', t, flags=re.S)
assert 'prefers-color-scheme: dark' not in t

# 2. header markup
rep('''      <div class="lang" role="group" aria-label="Тіл / Язык"><button type="button" data-lang="kk" aria-pressed="true">ҚАЗ</button><button type="button" data-lang="ru" aria-pressed="false">РУС</button></div>
    </div>
    <div class="sbox">''', '''      <div class="tools"><div class="lang" role="group" aria-label="Тіл / Язык"><button type="button" data-lang="kk" aria-pressed="true">ҚАЗ</button><button type="button" data-lang="ru" aria-pressed="false">РУС</button></div>
      <button class="hidep" id="hidep" type="button"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16M15 10l-2 2 2 2"/></svg><span data-i="hide"></span></button></div>
    </div>
    <div class="srow"><div class="sbox">''')
rep('''      <div class="results" id="results" role="listbox" hidden></div>
    </div>
  </header>''', '''      <div class="results" id="results" role="listbox" hidden></div>
    </div><button class="listbtn" id="listbtn" type="button" aria-expanded="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg><span data-i="list"></span></button></div>
  </header>''')

# 3. window + chip markup
rep('''    <div class="pickhint" id="pickhint" hidden></div>
  </div>
</div>''', '''    <div class="pickhint" id="pickhint" hidden></div>
    <div class="chipst" id="chipst" hidden role="status"></div>
  </div>
  <div class="hw" id="hw" hidden>
    <div class="hw-back" id="hwBack"></div>
    <section class="hw-box" id="hwBox" role="dialog" aria-modal="true" aria-labelledby="hwName"></section>
  </div>
</div>''')

# 4. CSS additions
rep('/* poster hero:', r'''/* collapsible panel */
.tools{display:flex;align-items:center;gap:8px}
.brand b{min-width:0}.brand b span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hidep{white-space:nowrap;display:inline-flex;align-items:center;gap:6px;border:none;background:var(--panel-2);border-radius:999px;padding:6px 11px;font-size:12.5px;font-weight:600;color:var(--ink-2);cursor:pointer;min-height:36px}
.hidep svg{width:16px;height:16px}
.hidep:hover{color:var(--ink)}
.srow{display:flex;gap:8px;align-items:center}
.listbtn{display:none;align-items:center;gap:7px;border:none;background:var(--panel);box-shadow:var(--shadow);border-radius:12px;padding:0 14px;min-height:44px;font-weight:600;font-size:14px;cursor:pointer;flex:none}
.listbtn svg{width:18px;height:18px}
.app.nopanel{grid-template-columns:0 minmax(0,1fr)}
.app.nopanel .side{display:none}
.app.nopanel .top{grid-column:2;grid-row:1;position:absolute;left:16px;top:16px;width:min(470px,calc(100% - 100px));background:transparent;border:none;padding:0;flex-direction:row;align-items:center;gap:8px;pointer-events:none}
.app.nopanel .top>*{pointer-events:auto}
.app.nopanel .brand{order:2}
.app.nopanel .brand b,.app.nopanel .hidep{display:none}
.app.nopanel .srow{order:1;flex:1;min-width:0}
.app.nopanel .search,.app.nopanel .lang{background:var(--panel);box-shadow:var(--shadow)}
.app.nopanel .listbtn{display:inline-flex}
.app{position:relative}
.phead{display:none}
/* ordinary street chip */
.chipst{position:absolute;left:50%;transform:translateX(-50%);bottom:calc(22px + env(safe-area-inset-bottom,0px));background:var(--panel);border-radius:14px;box-shadow:var(--shadow);padding:8px 8px 8px 14px;display:flex;align-items:center;gap:10px;z-index:7;max-width:calc(100% - 120px)}
.chipst[hidden]{display:none}
.chipst b{display:block;font-size:14px}
.chipst span{display:block;font-size:12px;color:var(--ink-2)}
/* history window */
.hw{position:fixed;inset:0;z-index:50}
.hw[hidden]{display:none}
.hw-back{position:absolute;inset:0;background:rgba(14,60,58,.16)}
.hw-box{--iv:#FBF7EE;--teal:#0E4A48;--teal-2:#3D6B68;--gold:#A9844C;--gold-soft:rgba(169,132,76,.16);
  position:fixed;top:5vh;height:90vh;background:var(--iv);color:var(--teal);border-radius:22px;box-shadow:0 24px 70px rgba(10,40,40,.35);display:grid;grid-template-columns:minmax(260px,40%) minmax(0,1fr);overflow:hidden}
.hw-box :focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.hw-orn{position:absolute;left:0;right:0;top:0;height:22px;color:var(--gold);pointer-events:none;z-index:2}
.hw-left{position:relative;display:flex;flex-direction:column;gap:10px;padding:34px 22px 18px;background:var(--iv);border-right:1px solid var(--gold-soft);min-height:0}
.frame{position:relative;flex:1;min-height:0;border:1.5px solid var(--gold);border-radius:16px;margin:6px;display:flex;align-items:flex-end;justify-content:center;overflow:visible;background:radial-gradient(60% 50% at 50% 45%,rgba(233,185,73,.20),transparent 72%)}
.frame .crn{position:absolute;width:34px;height:20px;color:var(--gold);background:var(--iv)}
.frame .crn.tl{left:-10px;top:-11px}.frame .crn.tr{right:-10px;top:-11px;transform:scaleX(-1)}
.frame .crn.bl{left:-10px;bottom:-11px;transform:scaleY(-1)}.frame .crn.br{right:-10px;bottom:-11px;transform:scale(-1,-1)}
.frame svg.fig{height:96%;width:auto;max-width:100%;filter:drop-shadow(0 10px 14px rgba(40,25,10,.2))}
.frame img.full{max-width:100%;max-height:100%;object-fit:contain;display:block;margin:auto;border-radius:6px}
.frame .ph{width:100%;height:100%;object-fit:cover;border-radius:14px}
.frame .noimg{margin:auto;display:flex;flex-direction:column;align-items:center;gap:10px;color:var(--teal-2);font-size:13px;text-align:center;padding:20px}
.frame .noimg i{width:84px;height:84px;border-radius:50%;display:grid;place-items:center;color:#fff}
.frame .noimg i svg{width:44px;height:44px}
.scap{margin:0;font-size:12px;line-height:1.4;color:var(--teal-2);text-align:center}
.scap a{color:inherit}
.scap b{color:var(--gold);font-weight:600}
.thumbs{display:flex;gap:8px;justify-content:center}
.thumbs button{width:56px;height:56px;border-radius:12px;border:1.5px solid var(--gold-soft);background:#fff;padding:0;overflow:hidden;cursor:pointer;display:grid;place-items:center}
.thumbs button[aria-pressed="true"]{border-color:var(--gold);box-shadow:0 0 0 2px var(--gold-soft)}
.thumbs button img{width:100%;height:100%;object-fit:cover;object-position:50% 20%}
.thumbs button svg{height:48px;width:auto}
.hw-right{display:flex;flex-direction:column;min-height:0;min-width:0;padding-top:22px}
.hw-head{padding:18px 26px 0;display:flex;justify-content:space-between;gap:14px;align-items:flex-start}
.hw-cat{font-size:11.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}
.hw-name{font-size:28px;font-weight:700;line-height:1.15;margin:6px 0 4px;letter-spacing:-.01em;text-wrap:balance;color:var(--teal)}
.hw-alt{margin:0;color:var(--teal-2);font-size:14px}
.pills{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.pills span{font-size:12.5px;font-weight:600;padding:4px 10px;border-radius:999px;background:var(--gold-soft);color:#6E5428}
.hw-x{flex:none;width:46px;height:46px;border-radius:50%;border:1.5px solid var(--gold);background:var(--iv);color:var(--teal);font-size:26px;line-height:1;cursor:pointer;display:grid;place-items:center}
.hw-x:hover{background:var(--gold-soft)}
.hw-tabs{display:flex;gap:4px;padding:14px 26px 0;border-bottom:1px solid var(--gold-soft)}
.hw-tab{border:none;background:transparent;color:var(--teal-2);font-weight:600;font-size:14.5px;padding:10px 12px 11px;border-bottom:2.5px solid transparent;cursor:pointer;min-height:44px}
.hw-tab[aria-selected="true"]{color:var(--teal);border-bottom-color:var(--gold)}
.hw-body{overflow:auto;flex:1;min-height:0;padding:18px 26px 26px;background:var(--iv);overscroll-behavior:contain}
.hw-body p{margin:0 0 12px;font-size:15.5px;line-height:1.65;max-width:62ch;color:#173E3C}
.hw-body h3{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin:20px 0 8px}
.hw-body ol.bio{list-style:none;margin:0;padding:0;border-left:2px solid var(--gold-soft)}
.hw-body ol.bio li{position:relative;padding:0 0 10px 16px;font-size:14.5px;line-height:1.5;color:#173E3C}
.hw-body ol.bio li::before{content:"";position:absolute;left:-6px;top:6px;width:10px;height:10px;border-radius:50%;background:var(--iv);border:2px solid var(--gold)}
.hw-body dl{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:0;font-size:14px}
.hw-body dt{color:var(--teal-2);font-variant-numeric:tabular-nums}
.hw-body dd{margin:0;color:#173E3C}
.hw-body .muted{color:var(--teal-2);font-size:13.5px}
.hw-acts{display:flex;flex-wrap:wrap;gap:8px;margin:4px 0 6px}
.hw-acts .primary{background:var(--teal);color:#FBF7EE}
.hw-acts .primary:hover{filter:brightness(1.12)}
.hw-acts .sec{background:#fff;border:1px solid var(--gold-soft);color:var(--teal)}
.hw-acts .sec:hover{border-color:var(--gold);color:var(--teal)}
.hw .voice{background:#fff;border:1px solid var(--gold-soft);margin:6px 0 14px}
.hw .voice .primary{background:var(--teal);color:#FBF7EE}
.hw .voice small{color:var(--teal-2)}
.near{display:flex;flex-wrap:wrap;gap:6px}
.near button{border:1px solid var(--gold-soft);background:#fff;border-radius:999px;padding:6px 12px;font-size:13px;color:var(--teal);cursor:pointer;min-height:36px}
.near button:hover{border-color:var(--gold)}
.srcs{display:flex;flex-direction:column;gap:5px;border-top:1px solid var(--gold-soft);margin-top:18px;padding-top:12px;font-size:12.5px}
.srcs a{color:var(--teal-2)}
.hw .rnav{background:var(--gold-soft);color:#6E5428;margin:0 0 12px}
.hw .rnav button{border-color:var(--gold);color:#6E5428}

/* poster hero:''')

# phone layout: hidden sheet, list button, phone window
rep('''  .side[data-s="peek"]{--sh:104px}''', '''  .side[data-s="hidden"]{--sh:0px;box-shadow:none;visibility:hidden}
  .side[data-s="peek"]{--sh:104px}''')
rep('''  .brand b{display:none}''', '''  .brand b,.hidep{display:none}
  .srow{order:1;flex:1;min-width:0}
  .listbtn{display:inline-flex;padding:0 12px}
  .listbtn span{display:none}
  .phead{display:flex;justify-content:flex-end;padding:0 10px;position:sticky;top:0;z-index:3;background:var(--panel)}
  .chipst{bottom:auto;top:calc(66px + env(safe-area-inset-top,0px));max-width:calc(100% - 24px)}
  .hw-box{left:0!important;right:0;width:auto!important;top:22vh;height:auto;bottom:0;border-radius:22px 22px 0 0;display:block;overflow:auto;padding-bottom:env(safe-area-inset-bottom,0px)}
  .hw-left{border-right:none;border-bottom:1px solid var(--gold-soft);padding:30px 16px 12px;min-height:auto}
  .frame{height:300px;flex:none}
  .hw-right{padding-top:0}
  .hw-head{padding:14px 16px 0;position:sticky;top:0;background:var(--iv);z-index:3}
  .hw-x{position:fixed;right:12px;top:calc(22vh + 10px);z-index:4;width:48px;height:48px;box-shadow:0 2px 10px rgba(0,0,0,.18)}
  .hw-name{font-size:23px;padding-right:56px}
  .hw-tabs{padding:10px 16px 0;position:sticky;top:0;background:var(--iv);z-index:2}
  .hw-body{overflow:visible;padding:16px 16px 28px}
  .hw-left .hw-orn{display:none}''')

open('premium4.html', 'w', encoding='utf8').write(t)
print('css/html ok', len(t))
