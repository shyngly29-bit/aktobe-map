"""premium4.html -> premium5.html: frosted glass UI, one reusable қошқар мүйіз symbol, generated figures over plates."""
t = open('premium4.html', encoding='utf8').read()
def rep(a, b):
    global t
    assert a in t, 'MISSING: ' + a[:90]
    t = t.replace(a, b, 1)

# ---------- shared ornament symbol (defined once, reused through <use>) ----------
rep('<div class="app">', '''<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs><symbol id="kosh" viewBox="0 0 48 22"><path d="M24 21 C24 13 19 6 13 6 C7 6 4 10 4 13 C4 17 8 18 10 16 C12 14 10 11 8 12 M24 21 C24 13 29 6 35 6 C41 6 44 10 44 13 C44 17 40 18 38 16 C36 14 38 11 40 12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><circle cx="24" cy="21" r="1.8" fill="currentColor"/></symbol></defs></svg>
<div class="app">''')
# small motif on the free edge of the search block and of the catalogue



# ---------- CSS ----------
rep('/* poster hero:', r'''/* ===== frosted glass + ornament (v5) ===== */
:root{--glass:rgba(255,255,255,.78);--glass-strong:rgba(255,255,255,.9);--glass-line:rgba(255,255,255,.85);--glass-edge:rgba(30,45,50,.10);--blur:blur(12px);--orn-gold:rgba(169,132,76,.15);--r-ui:14px}
.orn-mini{position:absolute;width:44px;height:20px;color:var(--orn-gold);pointer-events:none}
.tabs{position:sticky;top:0;z-index:3;background:rgba(255,255,255,.97)!important}

.tabs .sheetx{display:none;margin-left:6px;align-self:center}
.tabs .orn-tabs{position:static;margin-left:auto;align-self:center;width:40px;height:18px;flex:none}
.glass{background:var(--glass);-webkit-backdrop-filter:var(--blur);backdrop-filter:var(--blur);border:1px solid var(--glass-line);box-shadow:0 6px 22px rgba(20,30,35,.12),0 0 0 1px var(--glass-edge)}
.results,.chipst,.toast,.ctrl .grp,.ctrl .solo{background:var(--glass)!important;-webkit-backdrop-filter:var(--blur);backdrop-filter:var(--blur);border:1px solid var(--glass-line);box-shadow:0 6px 22px rgba(20,30,35,.12),0 0 0 1px var(--glass-edge)}
.ctrl button{background:transparent}
.ctrl .grp,.ctrl .solo{border-radius:var(--r-ui)}
.lang{border:1px solid var(--glass-edge)}
.lang button[aria-pressed="true"]{background:#fff}
@media (min-width:901px){
  .app{display:block;position:relative;height:100%}
  .mapwrap{position:absolute;inset:0}
  .top{position:absolute;left:12px;top:12px;width:384px;z-index:20;border-radius:20px 20px 0 0;border:1px solid var(--glass-line);border-bottom:none;background:var(--glass-strong);-webkit-backdrop-filter:var(--blur);backdrop-filter:var(--blur);box-shadow:0 0 0 1px var(--glass-edge);padding-bottom:12px}
  .side{position:absolute;left:12px;top:calc(12px + var(--toph,118px));bottom:12px;width:384px;z-index:19;border-radius:0 0 20px 20px;border:1px solid var(--glass-line);border-top:1px solid var(--glass-edge);background:var(--glass-strong);-webkit-backdrop-filter:var(--blur);backdrop-filter:var(--blur);box-shadow:0 10px 30px rgba(20,30,35,.14),0 0 0 1px var(--glass-edge);overflow:hidden}
  .search{background:rgba(240,242,244,.85)}
  .app.nopanel .top{left:16px;top:16px;width:min(470px,calc(100% - 100px));background:transparent;border:none;box-shadow:none;backdrop-filter:none;-webkit-backdrop-filter:none;padding:0}
}
.app.nopanel .search,.app.nopanel .lang,.app.nopanel .listbtn{background:var(--glass)!important;-webkit-backdrop-filter:var(--blur);backdrop-filter:var(--blur);border:1px solid var(--glass-line);box-shadow:0 6px 22px rgba(20,30,35,.12),0 0 0 1px var(--glass-edge)}
.walkbtn{position:relative;overflow:hidden}
.walkbtn::after{content:"";position:absolute;right:10px;bottom:6px;width:44px;height:20px;background:currentColor;opacity:.18;-webkit-mask:var(--kosh-mask) center/contain no-repeat;mask:var(--kosh-mask) center/contain no-repeat;pointer-events:none}
:root{--kosh-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 22'%3E%3Cpath d='M24 21 C24 13 19 6 13 6 C7 6 4 10 4 13 C4 17 8 18 10 16 C12 14 10 11 8 12 M24 21 C24 13 29 6 35 6 C41 6 44 10 44 13 C44 17 40 18 38 16 C36 14 38 11 40 12' fill='none' stroke='black' stroke-width='2.2' stroke-linecap='round'/%3E%3C/svg%3E")}
/* history window: glass shell, dense milky text surface */
.hw-back{background:rgba(14,60,58,.10)}
.hw-box{background:rgba(255,252,244,.86);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.85);box-shadow:0 24px 70px rgba(10,40,40,.28),0 0 0 1px rgba(14,74,72,.08)}
.hw-box{grid-template-columns:minmax(300px,44%) minmax(0,1fr)}
.hw-left{background:transparent;padding:22px 20px 16px}
.hw-body{background:rgba(255,253,248,.97);border-top:1px solid rgba(169,132,76,.18)}
.hw-tabs{border-bottom:none}
.hw-tab{position:relative}
.hw-tab .tabmark{position:absolute;left:50%;bottom:-2px;width:30px;height:12px;transform:translateX(-50%);color:rgba(169,132,76,.55);pointer-events:none}
.hw-tab[aria-selected="true"]{border-bottom-color:transparent}
.hw-tab[aria-selected="true"]::after{content:"";position:absolute;left:12px;right:12px;bottom:0;height:2px;background:var(--gold);border-radius:2px}
.frame{border:1px solid rgba(169,132,76,.45);background:none;overflow:hidden;align-items:stretch}
.frame .crn{position:absolute;width:56px;height:26px;color:rgba(169,132,76,.15);background:none;z-index:3;pointer-events:none}
.frame .crn.tl{left:8px;top:8px;transform:none}
.frame .crn.br{right:8px;bottom:8px;transform:scale(-1,-1)}
.gen{position:relative;width:100%;height:100%}
.gen .bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.gen::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,252,244,.30) 0%,rgba(255,252,244,.12) 55%,rgba(255,252,244,.55) 100%);pointer-events:none}
.gen .fg{position:absolute;inset:4% 4% 0;width:92%;height:96%;object-fit:contain;object-position:50% 100%;z-index:1}
.frame .ph{border-radius:0}
.frame img.full{padding:10px}
.thumbs button .tgen{position:relative;width:100%;height:100%;display:block}
.thumbs button .tgen img{position:absolute;inset:0;width:100%;height:100%}
.thumbs button .tgen img+img{object-fit:contain;object-position:50% 100%}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){
  :root{--glass:rgba(255,255,255,.98);--glass-strong:#fff}
  .hw-box{background:#FFFCF4}
}
@media (max-width:900px){
  .side{background:var(--glass-strong);-webkit-backdrop-filter:var(--blur);backdrop-filter:var(--blur)}
  .search,.lang,.listbtn{background:var(--glass)!important;-webkit-backdrop-filter:var(--blur);backdrop-filter:var(--blur);border:1px solid var(--glass-line)}
  .orn-tabs,.hw-tab .tabmark,.walkbtn::after{display:none}
  .phead{display:none!important}
  .tabs .sheetx{display:grid}
  .frame .crn.br{display:none}
  .frame{height:340px}
}

/* poster hero:''')

# ---------- JS: generated figures, corners via <use>, no top band ----------
rep('const STFIG={', '''const FIGIMG={"Әбілқайыр хан ескерткіші":["abilkaiyr"],"Жалаңтөс баһадүр ескерткіші":["zhalantos"],"Әйтеке би ескерткіші":["aiteke"],"Мөңке би ескерткіші":["monke"],"Тілеу батыр ескерткіші":["tileu"],"Сәңкібай батыр ескерткіші":["sankibai"],"Бөгенбай батыр ескерткіші":["bogenbai"],"Есет Көтібарұлы ескерткіші":["eset"],"Ер Едіге ескерткіші":["edige"],"Ахмет Жұбанов атындағы мемориалдық кешен":["zhubanov"],"Әлия Молдағұлова атындағы мемориалдық кешен":["aliya"],"В. Пацаев ескерткіші":["patsaev"],"Абай Құнанбайұлы ескерткіші":["abai"],"Нұрпейіс Байғанин ескерткіші":["baiganin"],"Аққағаз Досжанова ескерткіші":["doszhanova"],"Т. Ахтанов пен Қ. Шаңғытбаев ескерткіші":["akhtanov","shangytbaev"]};
const FIGNAME={akhtanov:["Тахауи Ахтанов","Тахави Ахтанов"],shangytbaev:["Қуандық Шаңғытбаев","Куандык Шангытбаев"]};
const genItems=kk=>(FIGIMG[kk]||[]).map(n=>({k:"gen",n,fg:`img/fig/${n}.webp`,bg:`img/fig/${n}_bg.webp`}));
const STFIG={''')
rep('const CRN=c=>`<svg class="crn ${c}" viewBox="0 0 48 22" aria-hidden="true">${KOSH}</svg>`;',
    'const CRN=c=>`<svg class="crn ${c}" aria-hidden="true" focusable="false"><use href="#kosh"/></svg>`;')
rep('  if(kind==="p"){const f=FIG[o.kk];if(f)items.push({k:"fig",t:f.t});', '  if(kind==="p"){items.push(...genItems(o.kk));')
rep('  else{const st=o.story,lp=placeForStreet(o),ft=(lp&&FIG[lp.kk]&&FIG[lp.kk].t)||STFIG[o.kk];if(ft&&ft!=="doctor0"&&!st.event)items.push({k:"fig",t:ft});',
    '  else{const st=o.story,lp=placeForStreet(o);if(lp&&!st.event)items.push(...genItems(lp.kk));')
rep('''  else if(it.k==="fig"){body=figSVG(it.t);cap=`<b>${T("rec")}</b> · ${T("recNote")}`}''',
    '''  else if(it.k==="gen"){const nm=FIGNAME[it.n]?FIGNAME[it.n][li()]:"";body=`<div class="gen"><img class="bg" src="${it.bg}" alt=""><img class="fg" src="${it.fg}" alt="${esc(T("rec"))}${nm?": "+esc(nm):""}"></div>`;cap=`<b>${T("rec")}</b>${nm?" · "+esc(nm):""} · ${T("recGen")}`}
  else if(it.k==="fig"){body=figSVG(it.t);cap=`<b>${T("rec")}</b> · ${T("recNote")}`}''')
rep('''x.k==="fig"?figSVG(x.t):`<img src="${x.src}" alt="">`''', '''x.k==="gen"?`<span class="tgen"><img src="${x.bg}" alt=""><img src="${x.fg}" alt=""></span>`:x.k==="fig"?figSVG(x.t):`<img src="${x.src}" alt="">`''')
rep('''aria-label="${x.k==="fig"?T("rec"):''', '''aria-label="${x.k==="fig"||x.k==="gen"?T("rec")+(FIGNAME[x.n]?": "+FIGNAME[x.n][li()]:""):''')
rep('return `<div class="frame">${CRN("tl")}${CRN("tr")}${CRN("bl")}${CRN("br")}${body}</div>', 'return `<div class="frame">${CRN("tl")}${CRN("br")}${body}</div>')
rep('hwBox.innerHTML=`${ORN2}<div class="hw-left">', 'hwBox.innerHTML=`<div class="hw-left">')
rep('''data-tab="short">${T("tShort")}</button>''', '''data-tab="short">${T("tShort")}${win.tab==="short"?'<svg class="tabmark" aria-hidden="true" focusable="false"><use href="#kosh"/></svg>':""}</button>''')
rep('''data-tab="more">${T("tMore")}</button>''', '''data-tab="more">${T("tMore")}${win.tab==="more"?'<svg class="tabmark" aria-hidden="true" focusable="false"><use href="#kosh"/></svg>':""}</button>''')
# i18n
rep('rec:"Көркем реконструкция",', 'rec:"Көркем реконструкция",recGen:"жасанды интеллект көмегімен жасалған сурет, архив фотосы емес",')
rep('rec:"Художественная реконструкция",', 'rec:"Художественная реконструкция",recGen:"изображение создано с помощью ИИ, это не архивное фото",')
# hover preview uses the generated figure when there is one
rep('''if(withPreview&&!isPhone()){const im=p.por||p.ph;
    pv.innerHTML=(im?`<img src="${im.src}" alt="">`:"")''', '''if(withPreview&&!isPhone()){const im=p.por||p.ph,g=genItems(p.kk)[0];
    pv.innerHTML=(g?`<div class="pvgen"><img src="${g.bg}" alt=""><img src="${g.fg}" alt=""></div>`:im?`<img src="${im.src}" alt="">`:"")''')
rep('.pv img{display:block;width:100%;height:140px;object-fit:cover;object-position:50% 22%}', '.pv img{display:block;width:100%;height:140px;object-fit:cover;object-position:50% 22%}\n.pv .pvgen{position:relative;height:190px}.pv .pvgen img{position:absolute;inset:0;width:100%;height:100%}.pv .pvgen img+img{object-fit:contain;object-position:50% 100%;padding-top:6px}')
rep('.pv{position:absolute;left:0;top:0;width:220px;background:var(--panel);', '.pv{position:absolute;left:0;top:0;width:220px;background:rgba(255,252,244,.92);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.85);')

# ---------- desktop: floating panel geometry ----------
rep('function freeArea(){const wr=wrap.getBoundingClientRect();const a={l:0,t:0,r:wr.width,b:wr.height};',
    'function panelRight(){if(isPhone()||!panelOpen)return 0;const r=side.getBoundingClientRect(),w=wrap.getBoundingClientRect();return r.right-w.left+12}\nfunction freeArea(){const wr=wrap.getBoundingClientRect();const a={l:0,t:0,r:wr.width,b:wr.height};')
rep('  else{a.r-=70;if(panelOpen===false)a.t=70;', '  else{a.r-=70;a.l=panelRight();if(panelOpen===false)a.t=70;')
rep('function placeWinBox(){if(isPhone()){hwBox.style.left="";hwBox.style.width="";return}const wr=wrap.getBoundingClientRect();const bw=Math.min(Math.max(680,Math.min(980,wr.width-300)),wr.width-24);hwBox.style.width=bw+"px";hwBox.style.left=(wr.left+(wr.width-bw)/2)+"px"}',
    'function placeWinBox(){if(isPhone()){hwBox.style.left="";hwBox.style.width="";return}const wr=wrap.getBoundingClientRect(),L0=panelRight(),avail=wr.width-L0;const bw=Math.min(Math.max(680,Math.min(1000,avail-200)),avail-24);hwBox.style.width=bw+"px";hwBox.style.left=(wr.left+L0+(avail-bw)/2)+"px"}')
rep('block(chipst);if(win.open)block(hwBox);if(!panelOpen&&!isPhone())block(document.querySelector(".top"));',
    'block(chipst);if(win.open)block(hwBox);if(!isPhone()){block(document.querySelector(".top"));if(panelOpen)block(side)}')
rep('function updListBtn(){', 'function measureTop(){document.documentElement.style.setProperty("--toph",document.querySelector(".top").offsetHeight+"px")}\nfunction updListBtn(){')
rep('addEventListener("resize",()=>{sheetPx();', 'addEventListener("resize",()=>{measureTop();sheetPx();')
rep('if(isPhone())side.dataset.s="hidden";setPanel(panelOpen||isPhone(),true);setLang(L);', 'if(isPhone())side.dataset.s="hidden";setPanel(panelOpen||isPhone(),true);setLang(L);measureTop();')
rep('  if(!results.hidden)runSearch();scheduleLabels(0)}', '  if(!results.hidden)runSearch();measureTop();scheduleLabels(0)}')

rep("const br=hwBox.getBoundingClientRect(),gl=br.left-wr.left,gr=wr.right-br.right;","const br=hwBox.getBoundingClientRect(),gl=br.left-wr.left-a.l,gr=wr.right-br.right;")
rep("if(gl>=gr){a.r=gl;a.l=0}","if(gl>=gr){a.r=a.l+gl}")
rep('<section class="hw-box" id="hwBox" role="dialog" aria-modal="true" aria-labelledby="hwName"></section>','<section class="hw-box" id="hwBox" role="dialog" aria-modal="true" aria-labelledby="hwName"></section>\n    <button class="hw-x hw-x2" id="hwClose2" type="button">×</button>')
rep('.hw-x:hover{background:var(--gold-soft)}','.hw-x:hover{background:var(--gold-soft)}\n.hw-x2{display:none}')
rep("  .hw-x{position:fixed;right:12px;top:calc(22vh + 10px);z-index:4;width:48px;height:48px;box-shadow:0 2px 10px rgba(0,0,0,.18)}","  .hw-box .hw-x{display:none}\n  .hw-x2{display:grid;position:fixed;right:12px;top:calc(22vh + 12px);z-index:60;width:50px;height:50px;box-shadow:0 2px 12px rgba(0,0,0,.2);--iv:#FBF7EE;--teal:#0E4A48;--gold:#A9844C}")
rep('$("hwBack").onclick=closeWin;','$("hwBack").onclick=closeWin;$("hwClose2").onclick=closeWin;')
rep('requestAnimationFrame(()=>{$("hwClose").focus({preventScroll:true});','requestAnimationFrame(()=>{(isPhone()?$("hwClose2"):$("hwClose")).focus({preventScroll:true});$("hwClose2").setAttribute("aria-label",T("close"));')
rep("""hw.addEventListener("keydown",e=>{if(e.key==="Tab"){const f=[...hwBox.querySelectorAll('button,a[href],[tabindex="0"]')]""","""hw.addEventListener("keydown",e=>{if(e.key==="Tab"){const f=[...hw.querySelectorAll('button,a[href],[tabindex="0"]')]""")
rep('  <div class="mapwrap" id="wrap">','  <button class="pgrip" id="pgrip" type="button" aria-controls="side"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg><span></span></button>\n  <div class="mapwrap" id="wrap">')
rep('/* poster hero:', """.pgrip{display:none}
@media (min-width:901px){
  .pgrip{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;position:absolute;left:396px;top:50%;transform:translateY(-50%);z-index:21;width:26px;min-height:76px;padding:8px 0;border:1px solid var(--glass-line);border-left:none;border-radius:0 12px 12px 0;background:var(--glass-strong);-webkit-backdrop-filter:var(--blur);backdrop-filter:var(--blur);box-shadow:4px 4px 14px rgba(20,30,35,.12);cursor:pointer;color:var(--ink-2)}
  .pgrip:hover{color:var(--ink)}
  .pgrip svg{width:18px;height:18px}
  .pgrip span{display:none;writing-mode:vertical-rl;font-size:12px;font-weight:600;letter-spacing:.04em}
  .app.nopanel .pgrip{left:0;border-left:none;min-height:110px}
  .app.nopanel .pgrip svg{transform:scaleX(-1)}
  .app.nopanel .pgrip span{display:block}
  .app.nopanel .side,.app.nopanel .pgrip+.x{display:none!important}
}
/* poster hero:""")
rep('$("hidep").onclick=()=>setPanel(false);','$("hidep").onclick=()=>setPanel(false);\n$("pgrip").onclick=()=>setPanel(!panelOpen);')
rep('function updListBtn(){','function updGrip(){const g=$("pgrip");if(!g)return;g.setAttribute("aria-expanded",String(panelOpen));g.setAttribute("aria-label",panelOpen?T("hide"):T("list"));g.title=panelOpen?T("hide"):T("list");g.querySelector("span").textContent=T("list")}\nfunction updListBtn(){updGrip();')
rep('<button class="tab" role="tab" data-tab="streets" aria-selected="${tab==="streets"}">${T("streets")} · ${storyStreets.length}</button></div>','<button class="tab" role="tab" data-tab="streets" aria-selected="${tab==="streets"}">${T("streets")} · ${storyStreets.length}</button><svg class="orn-mini orn-tabs" aria-hidden="true" focusable="false"><use href="#kosh"/></svg></div>')
rep('<svg class="orn-mini orn-tabs" aria-hidden="true" focusable="false"><use href="#kosh"/></svg></div>','<svg class="orn-mini orn-tabs" aria-hidden="true" focusable="false"><use href="#kosh"/></svg><button class="x sheetx" type="button" id="sheetx2" aria-label="${T("close")}">×</button></div>')
rep('const sx=$("sheetx");if(sx)sx.onclick=()=>setSheet("hidden");','const sx=$("sheetx2");if(sx)sx.onclick=()=>setSheet("hidden");')
open('premium5.html', 'w', encoding='utf8').write(t)
print('v5 ok', len(t))
