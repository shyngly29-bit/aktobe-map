"""premium6.html -> premium7.html: no 2GIS buttons, label shadows, draggable sheet, motion polish."""
t = open('premium6.html', encoding='utf8').read()
def rep(a, b):
    global t
    assert a in t, 'MISSING: ' + a[:90]
    t = t.replace(a, b, 1)

# ---------- 1. remove every 2GIS link (navigation will come later) ----------
rep('''  const pano=`https://yandex.kz/maps/?ll=${p.lon},${p.lat}&z=18&l=stv,sta&panorama%5Bpoint%5D=${p.lon},${p.lat}`,gis=`https://2gis.kz/aktobe/geo/${p.lon},${p.lat}`;
  const ns=nearestStreetName(p.x,p.y),ls=''', '''  const pano=`https://yandex.kz/maps/?ll=${p.lon},${p.lat}&z=18&l=stv,sta&panorama%5Bpoint%5D=${p.lon},${p.lat}`;
  const ns=nearestStreetName(p.x,p.y),ls=''')
rep('''  const acts=`<a class="act act-go" href="${gis}" target="_blank" rel="noopener">${UI.pin}${T("gisRoute")}</a>${t?`<a class="act" href="${t.u}" target="_blank" rel="noopener">${UI.tour}${T("tour3")}</a>`:""}<a class="act" href="${pano}" target="_blank" rel="noopener">${UI.pano}${T("pano")}</a>`;''',
    '''  const acts=`${t?`<a class="act act-go" href="${t.u}" target="_blank" rel="noopener">${UI.tour}${T("tour3")}</a>`:""}<a class="act${t?"":" act-go"}" href="${pano}" target="_blank" rel="noopener">${UI.pano}${T("pano")}</a>`;''')
rep('''  const acts=`<a class="act act-go" href="https://2gis.kz/aktobe/search/${encodeURIComponent(s.ru)}" target="_blank" rel="noopener">${UI.pin}${T("gisRoute")}</a><span class="oc-voice" id="voice"></span>`;''',
    '''  const acts=`<span class="oc-voice" id="voice"></span>`;''')
rep('''      <div class="secs"><a class="primary" style="flex:1" href="https://2gis.kz/aktobe/geo/${np.lon},${np.lat}" target="_blank" rel="noopener">${UI.pin}${T("gisRoute")}</a></div>
''', '')
# the "no turn-by-turn" note pointed users to 2GIS: reword
rep('noNav:"Бұрылыстар бойынша нұсқау жоқ: маршруттау сервисі қосылмаған. Нақты жаяу жолды 2ГИС-те құрыңыз."', 'noNav:"Бұрылыстар бойынша навигация кейін қосылады. Қазір аялдамалар мен оларға дейінгі түзу қашықтық көрсетіледі."')
rep('noNav:"Подсказок о поворотах нет: сервис маршрутизации не подключён. Точный пешеходный путь постройте в 2ГИС."', 'noNav:"Пошаговая навигация появится позже. Сейчас показаны остановки и расстояние до них по прямой."')
# voice listen button is the main action on streets
rep('''<button class="act" type="button" data-v="play">${UI.hp}${T("listen")}</button>''', '''<button class="act act-go" type="button" data-v="play">${UI.hp}${T("listen")}</button>''')
assert '2gis.kz' not in t, '2gis left'

# ---------- 2. street labels: thin white halo + very light shadow, constant on zoom ----------
rep('.slbl text{font-family:var(--f);fill:var(--label);paint-order:stroke;stroke:var(--halo);stroke-linejoin:round;pointer-events:none;font-weight:500}',
    '.slbl text{font-family:var(--f);fill:var(--label);paint-order:stroke fill;stroke:#fff;stroke-linejoin:round;pointer-events:none;font-weight:500}\n#slbl{filter:drop-shadow(0 1px .6px rgba(30,35,40,.16))}')
rep('t.setAttribute("stroke-width",(3.2/s).toFixed(3));', 't.setAttribute("stroke-width",(2.6/s).toFixed(3));')

# ---------- 3. phone sheet: third of the screen, follows the finger ----------
rep('function sheetH(){const vh=innerHeight,s=side.dataset.s;return s==="hidden"?0:s==="peek"?104:s==="half"?vh*.52:vh-70}',
    'function sheetH(){const vh=innerHeight,s=side.dataset.s;return s==="hidden"?0:s==="peek"?104:s==="half"?(win&&win.open?Math.max(vh*.36,300):vh*.46):vh-70}')
rep('''(()=>{let y0=null,moved=false;const start=e=>{if(!isPhone())return;if(e.target.closest("a,button:not(.grip)"))return;y0=e.clientY;moved=false};
  const end=e=>{if(y0==null)return;const dy=e.clientY-y0;y0=null;if(Math.abs(dy)<36)return;moved=true;const s=side.dataset.s;
    if(dy<0)setSheet("full");else if(s==="full")setSheet("half");else{if(win.open)closeWin();else setSheet("hidden")}
    if(win.open)setTimeout(renderWinKeep,0)};
  side.addEventListener("pointerdown",e=>{if(e.target.closest(".grip,.oc-head,.tabs"))start(e)});side.addEventListener("pointerup",end);side.addEventListener("pointercancel",()=>{y0=null});
  $("grip").addEventListener("click",e=>{if(moved){e.stopImmediatePropagation();moved=false}},true)})();''',
'''(()=>{let y0=null,h0=0,moved=false,pid=null;
  const start=e=>{if(!isPhone())return;if(e.target.closest("a,button:not(.grip),input"))return;y0=e.clientY;h0=side.getBoundingClientRect().height;moved=false;pid=e.pointerId};
  side.addEventListener("pointerdown",e=>{if(e.target.closest(".grip,.oc-head,.tabs"))start(e)});
  side.addEventListener("pointermove",e=>{if(y0==null||e.pointerId!==pid)return;const dy=e.clientY-y0;if(!moved&&Math.abs(dy)<6)return;
    if(!moved){moved=true;try{side.setPointerCapture(pid)}catch(_){};side.classList.add("dragging")}
    const h=Math.max(0,Math.min(innerHeight-70,h0-dy));side.style.height=h+"px"});
  const end=e=>{if(y0==null)return;const wasMoved=moved;y0=null;side.classList.remove("dragging");if(!wasMoved)return;
    const h=side.getBoundingClientRect().height,vh=innerHeight;side.style.height="";
    const snaps=[["hidden",0],["half",win.open?Math.max(vh*.36,300):vh*.46],["full",vh-70]];
    let best=snaps.reduce((a,b)=>Math.abs(b[1]-h)<Math.abs(a[1]-h)?b:a);
    if(best[0]==="hidden"){if(win.open)closeWin();else setSheet("hidden")}else{setSheet(best[0]);if(win.open)setTimeout(renderWinKeep,0)}};
  side.addEventListener("pointerup",end);side.addEventListener("pointercancel",end);
  $("grip").addEventListener("click",e=>{if(moved){e.stopImmediatePropagation();moved=false}},true)})();''')

# ---------- 4. tabs switch without re-rendering, sliding underline ----------
rep('''  pane.querySelectorAll("[data-tab]").forEach(b=>b.onclick=()=>{win.tab=b.dataset.tab;renderWinKeep();pane.querySelector(`[data-tab="${win.tab}"]`).focus()});''',
    '''  win.w=w;const ind=pane.querySelector(".oc-ind"),moveInd=()=>{const a=pane.querySelector(`.oc-tab[aria-selected="true"]`);if(a&&ind){ind.style.width=a.offsetWidth-20+"px";ind.style.transform=`translateX(${a.offsetLeft+10}px)`}};
  requestAnimationFrame(()=>{ind&&ind.classList.add("noanim");moveInd();requestAnimationFrame(()=>ind&&ind.classList.remove("noanim"))});
  pane.querySelectorAll("[data-tab]").forEach(b=>b.onclick=()=>{win.tab=b.dataset.tab;pane.querySelectorAll("[data-tab]").forEach(x=>x.setAttribute("aria-selected",String(x===b)));
    const tp=$("tp");tp.setAttribute("aria-labelledby","tb-"+win.tab);tp.innerHTML=win.tab==="short"?win.w.short:win.w.more;tp.classList.remove("fadein");void tp.offsetWidth;tp.classList.add("fadein");bindBody();moveInd()});
  bindBody();''')
rep('''  pane.querySelectorAll("[data-go]").forEach(b=>b.onclick=()=>{const g=b.dataset.go,i=+g.slice(1);g[0]==="p"?openPlace(i,{zoom:true}):openStreet(i,{fit:true})});
  pane.querySelectorAll("[data-r]")''', '''  pane.querySelectorAll("[data-r]")''')
rep('function renderWinKeep(){', 'function bindBody(){pane.querySelectorAll("#tp [data-go]").forEach(b=>b.onclick=()=>{const g=b.dataset.go,i=+g.slice(1);g[0]==="p"?openPlace(i,{zoom:true}):openStreet(i,{fit:true})})}\nfunction renderWinKeep(){')
rep('''<button class="oc-tab" role="tab" id="tb-more" aria-controls="tp" aria-selected="${win.tab==="more"}" data-tab="more">${T("tMore")}</button></div>''',
    '''<button class="oc-tab" role="tab" id="tb-more" aria-controls="tp" aria-selected="${win.tab==="more"}" data-tab="more">${T("tMore")}</button><span class="oc-ind" aria-hidden="true"></span></div>''')
# the short subtitle under the image is not needed (category line already says it)
rep('''   ${w.sub?`<p class="oc-sub">${esc(w.sub)}</p>`:""}
''', '')

# ---------- 5. image fallback: keep name, story and actions if a picture fails ----------
rep('''function imgBody(it){if(it.k==="gen")return `<div class="gen"><img class="bg" src="${it.bg}" alt=""><img class="fg" src="${it.fg}" alt=''',
    '''const IMGERR=`onerror="const f=this.closest('.oc-img');if(f)f.remove();else{const l=this.closest('.lb-in');if(l)l.innerHTML=''}"`;
function imgBody(it){if(it.k==="gen")return `<div class="gen"><img class="bg" src="${it.bg}" alt="" onerror="this.remove()"><img class="fg" ${IMGERR} src="${it.fg}" alt=''')
rep('''  if(it.k==="por")return `<img class="full" src="${it.src}" alt="${T("origPhoto")}">`;return `<img class="ph" src="${it.src}" alt="${T("objPhoto")}">`}''',
    '''  if(it.k==="por")return `<img class="full" ${IMGERR} src="${it.src}" alt="${T("origPhoto")}">`;return `<img class="ph" ${IMGERR} src="${it.src}" alt="${T("objPhoto")}">`}''')

# ---------- 6. motion: card in/out, fast switching, lightbox, search, ring pulse, hover delay ----------
rep('''function openWin(tk,i,opt={}){if(!win.open)lastFocus=opt.from||document.activeElement;''',
    '''let closeTok=0;
function openWin(tk,i,opt={}){closeTok++;pane.classList.remove("closing");const wasOpen=win.open&&view==="card";if(!win.open)lastFocus=opt.from||document.activeElement;''')
rep('''  renderWin();pane.scrollTop=0;''', '''  renderWin();pane.scrollTop=0;const oc=pane.querySelector(".oc");if(oc)oc.classList.add(wasOpen?"swap":"enter");''')
rep('''function closeWin(){if(!win.open)return;win.open=false;''', '''function closeWin(){if(!win.open)return;
  if(!isPhone()&&!reduce()&&!pane.classList.contains("closing")){const tok=++closeTok;pane.classList.add("closing");setTimeout(()=>{if(tok!==closeTok)return;pane.classList.remove("closing");closeWinNow()},170);return}
  closeWinNow()}
function closeWinNow(){if(!win.open)return;win.open=false;''')
rep('''function openLightbox(it){if(!it)return;lb.querySelector(".lb-in").innerHTML=imgBody(it);lb.querySelector(".lb-cap").innerHTML=imgCap(it);lb.hidden=false;lb.querySelector(".lb-x").focus()}
function closeLightbox(){lb.hidden=true;const z=pane.querySelector("[data-zoom]");if(z)z.focus()}''',
'''let lbScroll=0;
function openLightbox(it){if(!it)return;lbScroll=pane.scrollTop;lb.querySelector(".lb-in").innerHTML=imgBody(it);lb.querySelector(".lb-cap").innerHTML=imgCap(it);lb.hidden=false;lb.classList.remove("show");void lb.offsetWidth;lb.classList.add("show");lb.querySelector(".lb-x").focus()}
function closeLightbox(){lb.classList.remove("show");lb.hidden=true;pane.scrollTop=lbScroll;const z=pane.querySelector("[data-zoom]");if(z)z.focus({preventScroll:true})}''')
# ring pulse once on the selected marker
rep('''  P.forEach(o=>o.el.classList.toggle("on",o.i===i));mg.appendChild(p.el);p.el.classList.remove("gone");
  const ol=$("olSel");if(p.out){ol.setAttribute("d",p.out);ol.classList.add("show")}else ol.classList.remove("show");
  $("stSel").style.display="none";openWin("p",i,opt)}''',
'''  P.forEach(o=>o.el.classList.toggle("on",o.i===i));mg.appendChild(p.el);p.el.classList.remove("gone");
  p.el.classList.remove("pulse");void p.el.getBBox();p.el.classList.add("pulse");
  const ol=$("olSel");if(p.out){ol.setAttribute("d",p.out);ol.classList.add("show")}else ol.classList.remove("show");
  $("stSel").style.display="none";openWin("p",i,opt)}''')
# hover preview after a short delay
rep('''  g.addEventListener("pointerenter",e=>{if(e.pointerType==="mouse"&&!dragging)hover({t:"p",i:p.i},true)});''',
    '''  g.addEventListener("pointerenter",e=>{if(e.pointerType!=="mouse"||dragging)return;clearTimeout(g._hv);g._hv=setTimeout(()=>hover({t:"p",i:p.i},true),140)});
  g.addEventListener("pointerleave",()=>clearTimeout(g._hv));''')

# ---------- CSS ----------
rep('/* poster hero:', r'''/* ===== v7: elevation + motion ===== */
.oc{border-radius:0}
@media (min-width:901px){
  .side{border-radius:0 0 18px 18px;box-shadow:0 12px 34px rgba(20,30,35,.16),0 0 0 1px rgba(30,45,50,.08)}
  .top{border-radius:18px 18px 0 0}
  .pv{box-shadow:0 6px 18px rgba(20,30,35,.12)}
  .ctrl .grp,.ctrl .solo,.pgrip{box-shadow:0 3px 10px rgba(20,30,35,.10),0 0 0 1px rgba(30,45,50,.06)}
}
.oc-zoom{border-radius:16px;box-shadow:0 2px 8px rgba(20,30,35,.06)}
.act{transition:background .15s,transform .1s}
.act:active,.oc-x:active,.linkbtn:active,.ctrl button:active,.res:active,.row:active{transform:scale(.97)}
.oc-x:focus-visible,.act:focus-visible,.oc-tab:focus-visible,.row:focus-visible,.oc-zoom:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.oc-tabs{position:relative}
.oc-tab{border-bottom-color:transparent!important}
.oc-ind{position:absolute;left:0;bottom:-1px;height:2.5px;border-radius:2px;background:var(--accent);width:0;transition:transform .24s cubic-bezier(.2,.7,.2,1),width .24s cubic-bezier(.2,.7,.2,1)}
.oc-ind.noanim{transition:none}
@media (max-width:900px){.side.dragging{transition:none!important}.side{transition:height .28s cubic-bezier(.2,.7,.2,1)}}
@media (prefers-reduced-motion:no-preference){
  .oc.enter{animation:ocIn .24s cubic-bezier(.2,.7,.2,1) both}
  .oc.swap{animation:ocSwap .2s ease both}
  .pane.closing .oc{animation:ocOut .17s ease both}
  @media (max-width:900px){.oc.enter{animation:none}}
  .fadein{animation:ocSwap .18s ease both}
  .results:not([hidden]){animation:resIn .15s ease-out both}
  .lb.show{animation:lbFade .2s ease both}.lb.show .lb-in{animation:lbIn .22s cubic-bezier(.2,.7,.2,1) both}
  .mk.pulse .ring{animation:ring .6s ease-out 1}
  .pv:not([hidden]){animation:resIn .14s ease-out both}
}
@keyframes ocIn{from{opacity:0;transform:translateX(-14px)}to{opacity:1;transform:none}}
@keyframes ocOut{from{opacity:1;transform:none}to{opacity:0;transform:translateX(-12px)}}
@keyframes ocSwap{from{opacity:.35}to{opacity:1}}
@keyframes resIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:none}}
@keyframes lbFade{from{opacity:0}to{opacity:1}}
@keyframes lbIn{from{opacity:0;transform:scale(.98)}to{opacity:1;transform:none}}
@keyframes ring{0%{stroke-width:7;opacity:.25}100%{stroke-width:3;opacity:1}}

/* poster hero:''')

rep('@media (max-width:900px){.side.dragging{transition:none!important}', '@media (max-width:900px){.side[data-s="half"]{--sh:46%}.side.card[data-s="half"]{--sh:max(36%,300px)}.side.dragging{transition:none!important}')
rep("  win.open=true;win.t=tk;win.i=i;win.tab=\"short\";win.stage=0;", "  win.open=true;side.classList.add(\"card\");win.t=tk;win.i=i;win.tab=\"short\";win.stage=0;")
rep("function closeWinNow(){if(!win.open)return;win.open=false;", "function closeWinNow(){if(!win.open)return;win.open=false;side.classList.remove(\"card\");")
open('premium7.html', 'w', encoding='utf8').write(t)
print('v7 ok', len(t))
