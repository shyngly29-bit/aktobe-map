"""premium5.html -> premium6.html: 2GIS-style object card in the left panel / bottom sheet instead of the big window."""
t = open('premium5.html', encoding='utf8').read()
def rep(a, b):
    global t
    assert a in t, 'MISSING: ' + a[:90]
    t = t.replace(a, b, 1)
def cut(start, end, new):
    global t
    i = t.index(start); j = t.index(end, i)
    t = t[:i] + new + t[j:]

# ---------- remove AI wording from the visible UI ----------
rep('recGen:"жасанды интеллект көмегімен жасалған сурет, архив фотосы емес",', '')
rep('recGen:"изображение создано с помощью ИИ, это не архивное фото",', '')
rep('cap=`<b>${T("rec")}</b>${nm?" · "+esc(nm):""} · ${T("recGen")}`', 'cap=`<b>${T("rec")}</b>${nm?" · "+esc(nm):""}`')
assert 'recGen' not in t and 'жасанды интеллект' not in t and 'помощью ИИ' not in t
rep('gisRoute:"2ГИС-те маршрут",', 'gisRoute:"2ГИС-те маршрут",tour3:"3D-тур",enlarge:"Үлкейту",')
rep('gisRoute:"Маршрут в 2ГИС",', 'gisRoute:"Маршрут в 2ГИС",tour3:"3D-тур",enlarge:"Увеличить",')

# ---------- free map area: panel (desktop) or sheet (phone) ----------
rep('''  if(isPhone()){a.t=64;if(win.open){a.b=Math.max(a.t+60,innerHeight*.22-wr.top)}else a.b=Math.min(a.b,wr.height-sheetH())}
  else{a.r-=70;a.l=panelRight();if(panelOpen===false)a.t=70;
    if(win.open){const br=hwBox.getBoundingClientRect(),gl=br.left-wr.left-a.l,gr=wr.right-br.right;
      if(Math.max(gl,gr)>=90){if(gl>=gr){a.r=a.l+gl}else{a.l=br.right-wr.left;a.r=wr.width-70>a.l+60?wr.width-70:wr.width}}}}''',
'''  if(isPhone()){a.t=64;a.b=Math.min(a.b,wr.height-sheetH())}
  else{a.r-=70;a.l=panelRight();if(panelOpen===false)a.t=70}''')

# no "device voice · language" footnote next to the Listen button
rep('''    <small>${how==="sys"?T("voiceSys"):"Claude"} · ${lang==="kk"?"қазақ тілі":"русский язык"}</small>`;''', '''`;''')
rep('''<button class="primary" type="button" data-v="play" style="flex:1">${UI.play}${T("listen")}</button>''', '''<button class="act" type="button" data-v="play">${UI.hp}${T("listen")}</button>''')
rep('''voice.state==="speaking"?`<button class="sec" type="button" data-v="pause">''', '''voice.state==="speaking"?`<button class="act" type="button" data-v="pause">''')
rep('''`<button class="sec" type="button" data-v="resume">''', '''`<button class="act" type="button" data-v="resume">''')
rep('''${mine?`<button class="sec" type="button" data-v="replay">↻ ${T("replay")}</button><button class="sec" type="button" data-v="stop">■ ${T("stop")}</button>`:""}''',
    '''${mine?`<button class="act" type="button" data-v="replay" aria-label="${T("replay")}">↻</button><button class="act" type="button" data-v="stop" aria-label="${T("stop")}">■</button>`:""}''')

# ---------- card renderer replaces the window ----------
cut('function placeWin(p){', 'function showChip(s){', r'''function imgBody(it){if(it.k==="gen")return `<div class="gen"><img class="bg" src="${it.bg}" alt=""><img class="fg" src="${it.fg}" alt="${esc(T("rec"))}${FIGNAME[it.n]?": "+esc(FIGNAME[it.n][li()]):""}"></div>`;
  if(it.k==="por")return `<img class="full" src="${it.src}" alt="${T("origPhoto")}">`;return `<img class="ph" src="${it.src}" alt="${T("objPhoto")}">`}
function imgCap(it){if(it.k==="gen")return `<b>${T("rec")}</b>${FIGNAME[it.n]?" · "+esc(FIGNAME[it.n][li()]):""}`;if(it.k==="por")return `<b>${T("origPhoto")}</b> · ${it.cap}`;return `<b>${T("objPhoto")}</b> · ${it.cap}`}
function imageBlock(items){if(!items.length)return "";const it=items[win.stage]||items[0];
  return `<figure class="oc-img"><button class="oc-zoom" type="button" data-zoom aria-label="${T("enlarge")}">${imgBody(it)}<svg class="crn" aria-hidden="true" focusable="false"><use href="#kosh"/></svg></button><figcaption>${imgCap(it)}</figcaption>
   ${items.length>1?`<div class="thumbs">${items.map((x,n)=>`<button type="button" data-st="${n}" aria-pressed="${n===win.stage}" aria-label="${x.k==="gen"?T("rec")+(FIGNAME[x.n]?": "+FIGNAME[x.n][li()]:""):x.k==="por"?T("origPhoto"):T("objPhoto")}">${x.k==="gen"?`<span class="tgen"><img src="${x.bg}" alt=""><img src="${x.fg}" alt=""></span>`:`<img src="${x.src}" alt="">`}</button>`).join("")}</div>`:""}</figure>`}
function cardPlace(p){const d=DET[p.kk]||{},f=FIG[p.kk],t=p.tour&&TOURS[p.tour];
  const pano=`https://yandex.kz/maps/?ll=${p.lon},${p.lat}&z=18&l=stv,sta&panorama%5Bpoint%5D=${p.lon},${p.lat}`,gis=`https://2gis.kz/aktobe/geo/${p.lon},${p.lat}`;
  const ns=nearestStreetName(p.x,p.y),ls=d.street&&streetByKk(d.street);
  const short=d.short?d.short[li()]:`${DESC(p)}${ns?" "+T("located")+" "+SN(ns)+".":""}`;
  const lead=CAP(p)||(DESC(p).split(/(?<=[.!?])\s/)[0]);
  const acts=`<a class="act act-go" href="${gis}" target="_blank" rel="noopener">${UI.pin}${T("gisRoute")}</a>${t?`<a class="act" href="${t.u}" target="_blank" rel="noopener">${UI.tour}${T("tour3")}</a>`:""}<a class="act" href="${pano}" target="_blank" rel="noopener">${UI.pano}${T("pano")}</a>`;
  const rn=rIdx>=0&&route[rIdx]===p.i?`<div class="rnav oc-rnav"><span>${T("stopN")} ${rIdx+1} / ${route.length}</span><div><button type="button" data-r="-1" ${rIdx===0?"disabled":""} aria-label="${T("prev")}">←</button><button type="button" data-r="1" ${rIdx===route.length-1?"disabled":""}>${T("next")} →</button></div></div>`:"";
  const nb=nearby(p.x,p.y,p.i);
  const more=`${f?`<h3>${T("bioH")}</h3>${d.bio?`<ol class="bio">${d.bio.map(b=>`<li>${esc(b[li()])}</li>`).join("")}</ol>`:`<p class="muted">${T("bioNo")}</p>`}`:`<h3>${T("objH")}</h3><p>${esc(DESC(p))}</p>`}
    <h3>${p.c==="rel"||p.c==="mus"?T("objH"):T("monH")}</h3><dl>${p.code?`<dt>${T("touristMap")}</dt><dd>${p.code}</dd>`:""}<dt>${L==="kk"?"Орны":"Место"}</dt><dd>${ns?esc(SN(ns)):"—"}</dd>${f&&f.tribe?`<dt>${L==="kk"?"Руы":"Род"}</dt><dd>${esc(f.tribe[li()])}</dd>`:""}</dl><p class="muted">${T("monNo")}</p>
    ${nb.length?`<h3>${T("nearH")}</h3><div class="near">${nb.map(n=>`<button type="button" data-go="p${n.i}">${esc(n.n)} · ${fmtDist(n.d)}</button>`).join("")}</div>`:""}
    ${srcList([d.wiki&&["Wikipedia",d.wiki],[p.out?"OpenStreetMap: контур":"OpenStreetMap",p.outSrc||`https://www.openstreetmap.org/?mlat=${p.lat}&mlon=${p.lon}#map=18/${p.lat}/${p.lon}`],p.por&&["Wikimedia Commons: "+(p.por.by||"портрет"),p.por.page],p.ph&&["Wikimedia Commons: "+(p.ph.by||"фото"),p.ph.page],p.code&&[T("touristMap")+" — "+p.code,null],t&&["visitaktobe.kz — 3D",t.u]])}`;
  return {cat:p.c,catName:CAT1[p.c][li()],name:f?(f.name?f.name[li()]:SHORT(p)):NAME(p),sub:f?NAME(p):"",addr:ns?SN(ns):"",lead,acts,rn,items:stageFor("p",p),
    short:`<p>${esc(short)}</p>${ls?`<button class="linkbtn" type="button" data-go="s${ls.i}">${svgI("st")}${T("streetOf")}: ${esc(SN(ls))}</button>`:""}`,more}}
function cardStreet(s){const st=s.story,lp=placeForStreet(s);
  const per=x=>x.p?x.p.replace(/^-/,"–").replace(/-/,"–"):"";
  const olds=s.olds.filter(o=>o.p||!s.olds.some(q=>q.p&&fold(q.ru||q.kk||"").includes(fold((o.ru||o.kk||"").replace(/^ул\.?\s*/,"")))));
  const named=st.event?"":(L==="kk"?`Көше ${st.who[0]} құрметіне аталған. `:`Улица названа в честь: ${st.who[1]}. `);
  const y=renewYear(s),last=olds.length?olds[olds.length-1]:null;
  const acts=`<a class="act act-go" href="https://2gis.kz/aktobe/search/${encodeURIComponent(s.ru)}" target="_blank" rel="noopener">${UI.pin}${T("gisRoute")}</a><span class="oc-voice" id="voice"></span>`;
  const d=lp&&DET[lp.kk];
  const more=`<h3>${T("namesH")}</h3><dl><dt>${T("nowName")}</dt><dd>${esc(s.kk)}<br>${esc(s.ru)}</dd>${olds.map(o=>`<dt>${esc(per(o))||"—"}</dt><dd>${esc((L==="kk"?(o.kk||o.ru):(o.ru||o.kk))||"")}</dd>`).join("")}<dt>${T("renamedY")}</dt><dd>${y?esc(y)+(st.renamed?"":" ("+T("byOsm")+")"):T("renamedNo")}</dd></dl>
    <h3>${T("valueH")}</h3>${st.note?`<p>${esc(st.note[li()])}</p>`:`<p class="muted">${T("valueNo")}</p>`}
    <h3>${T("bioH")}: ${esc(st.who[li()])}</h3>${d&&d.bio?`<ol class="bio">${d.bio.map(b=>`<li>${esc(b[li()])}</li>`).join("")}</ol>`:`<p>${esc(st.bio[li()])}</p>`}
    ${srcList([[T("osmWay"),`https://www.openstreetmap.org/way/${s.id}`],...st.src,st.por&&["Wikimedia Commons: портрет",CRED[st.por]&&CRED[st.por].page],st.ph&&["Wikimedia Commons: фото",CRED[st.ph]&&CRED[st.ph].page]])}`;
  return {cat:"st",catName:T("street"),name:SN(s),sub:SA(s),addr:last?(L==="kk"?"бұрын: ":"ранее: ")+((L==="kk"?(last.kk||last.ru):(last.ru||last.kk))||""):"",lead:[st.who[li()],st.dates].filter(Boolean).join(" · "),acts,rn:"",items:stageFor("s",s),
    short:`<p>${esc(named+st.bio[li()]+(st.note?" "+st.note[li()]:""))}</p>${lp?`<button class="linkbtn" type="button" data-go="p${lp.i}">${svgI(lp.c)}${T("monOf")}: ${esc(SHORT(lp))}</button>`:""}`,more}}
function renderWin(){const o=win.t==="p"?P[win.i]:STREETS[win.i];const w=win.t==="p"?cardPlace(o):cardStreet(o);view="card";const full=side.dataset.s==="full";
  pane.innerHTML=`<article class="oc" aria-labelledby="hwName">
   <header class="oc-head" id="ocHead">
    <div class="oc-bar">${isPhone()?`<span class="oc-cat"><i class="bg-${w.cat}">${svgI(w.cat==="st"?"st":w.cat,"#fff")}</i>${esc(w.catName)}</span>`:`<button class="back" type="button" data-back>${UI.back}${T("back")}</button>`}<button class="oc-x" id="hwClose" type="button" aria-label="${T("close")}">×</button></div>
    <h2 class="oc-name" id="hwName" tabindex="-1">${esc(w.name)}</h2>
    <p class="oc-meta">${isPhone()?"":`<span class="oc-cat"><i class="bg-${w.cat}">${svgI(w.cat==="st"?"st":w.cat,"#fff")}</i>${esc(w.catName)}</span>`}${w.addr?`<span>${UI.pin}${esc(w.addr)}</span>`:""}</p>
    ${w.lead&&w.lead!==w.catName?`<p class="oc-lead">${esc(w.lead)}</p>`:""}
    <div class="oc-acts">${w.acts}</div>
    ${isPhone()?`<button class="oc-more" id="ocMore" type="button" aria-expanded="${full}">${full?(L==="kk"?"Жинау":"Свернуть"):T("tMore")}</button>`:""}
   </header>
   ${w.rn}
   ${imageBlock(w.items)}
   ${w.sub?`<p class="oc-sub">${esc(w.sub)}</p>`:""}
   <div class="oc-tabs" role="tablist"><button class="oc-tab" role="tab" id="tb-short" aria-controls="tp" aria-selected="${win.tab==="short"}" data-tab="short">${T("tShort")}</button><button class="oc-tab" role="tab" id="tb-more" aria-controls="tp" aria-selected="${win.tab==="more"}" data-tab="more">${T("tMore")}</button></div>
   <div class="oc-body" id="tp" role="tabpanel" aria-labelledby="tb-${win.tab}">${win.tab==="short"?w.short:w.more}</div>
  </article>`;
  $("hwClose").onclick=closeWin;const bk=pane.querySelector("[data-back]");if(bk)bk.onclick=closeWin;
  const mo=$("ocMore");if(mo)mo.onclick=()=>{setSheet(side.dataset.s==="full"?"half":"full");setTimeout(renderWinKeep,0)};
  pane.querySelectorAll("[data-tab]").forEach(b=>b.onclick=()=>{win.tab=b.dataset.tab;renderWinKeep();pane.querySelector(`[data-tab="${win.tab}"]`).focus()});
  pane.querySelectorAll("[data-st]").forEach(b=>b.onclick=()=>{win.stage=+b.dataset.st;renderWinKeep()});
  pane.querySelectorAll("[data-zoom]").forEach(b=>b.onclick=()=>openLightbox(w.items[win.stage]||w.items[0]));
  pane.querySelectorAll("[data-go]").forEach(b=>b.onclick=()=>{const g=b.dataset.go,i=+g.slice(1);g[0]==="p"?openPlace(i,{zoom:true}):openStreet(i,{fit:true})});
  pane.querySelectorAll("[data-r]").forEach(b=>b.onclick=()=>{rIdx+=+b.dataset.r;openPlace(route[rIdx],{zoom:true,keepRoute:true})});
  if(win.t==="s")renderVoice(win.i);
}
function renderWinKeep(){const y=pane.scrollTop;renderWin();pane.scrollTop=y}
function placeWinBox(){}
function openWin(tk,i,opt={}){if(!win.open)lastFocus=opt.from||document.activeElement;
  win.open=true;win.t=tk;win.i=i;win.tab="short";win.stage=0;hideChip();pv.hidden=true;hover(null);
  if(isPhone()){if(side.dataset.s==="hidden"||side.dataset.s==="peek")setSheet("half")}else if(!panelOpen)setPanel(true);
  renderWin();pane.scrollTop=0;
  requestAnimationFrame(()=>{if(!isPhone())$("hwName").focus({preventScroll:true});
    if(tk==="p"){const p=P[i];centerWorld(p.x,p.y,Math.max(k,opt.zoom?(p.out?6:3.6):k))}else{const s=STREETS[i];fitBox(...s.bb,6)}});
  scheduleLabels(0)}
function closeWin(){if(!win.open)return;win.open=false;if(voice.state!=="idle"&&win.t==="s")stopVoice();
  sel=null;rIdx=-1;P.forEach(o=>o.el.classList.remove("on","hl"));$("olSel").classList.remove("show");$("stSel").style.display="none";$("stHov").style.display="none";
  if(walk.on)renderWalk();else renderHome();if(isPhone())setSheet("hidden");
  scheduleLabels(0);const back=lastFocus;if(back&&document.contains(back)&&back!==document.body)back.focus({preventScroll:true})}
/* enlarged image */
const lb=$("lb");
function openLightbox(it){if(!it)return;lb.querySelector(".lb-in").innerHTML=imgBody(it);lb.querySelector(".lb-cap").innerHTML=imgCap(it);lb.hidden=false;lb.querySelector(".lb-x").focus()}
function closeLightbox(){lb.hidden=true;const z=pane.querySelector("[data-zoom]");if(z)z.focus()}
lb.querySelector(".lb-x").onclick=closeLightbox;lb.addEventListener("click",e=>{if(e.target===lb)closeLightbox()});
/* swipe the sheet on phones */
(()=>{let y0=null,moved=false;const start=e=>{if(!isPhone())return;if(e.target.closest("a,button:not(.grip)"))return;y0=e.clientY;moved=false};
  const end=e=>{if(y0==null)return;const dy=e.clientY-y0;y0=null;if(Math.abs(dy)<36)return;moved=true;const s=side.dataset.s;
    if(dy<0)setSheet("full");else if(s==="full")setSheet("half");else{if(win.open)closeWin();else setSheet("hidden")}
    if(win.open)setTimeout(renderWinKeep,0)};
  side.addEventListener("pointerdown",e=>{if(e.target.closest(".grip,.oc-head,.tabs"))start(e)});side.addEventListener("pointerup",end);side.addEventListener("pointercancel",()=>{y0=null});
  $("grip").addEventListener("click",e=>{if(moved){e.stopImmediatePropagation();moved=false}},true)})();
''')
rep('document.addEventListener("keydown",e=>{if(e.key==="Escape"){if(!$("results").hidden){hideResults();return}if(win.open){closeWin();return}',
    'document.addEventListener("keydown",e=>{if(e.key==="Escape"){if(!lb.hidden){closeLightbox();return}if(!$("results").hidden){hideResults();return}if(win.open){closeWin();return}')
# grip toggles: keep card content in sync
rep('$("grip").onclick=()=>setSheet(side.dataset.s==="full"?"half":"full");', '$("grip").onclick=()=>{setSheet(side.dataset.s==="full"?"half":"full");if(win.open)setTimeout(renderWinKeep,0)};')
# language switch re-renders the card on top of the home view
rep('if(view==="walk")renderWalk();else renderHome();if(win.open)renderWin();', 'if(win.open)renderWin();else if(view==="walk")renderWalk();else renderHome();')
# selecting a row while a card is open: do not re-render the catalogue under the card
rep('''  $("stSel").style.display="none";openWin("p",i,opt);if(view==="home")renderHome()}''', '''  $("stSel").style.display="none";openWin("p",i,opt)}''')

# ---------- markup: lightbox ----------
rep('  <div class="hw" id="hw" hidden>', '''  <div class="lb" id="lb" hidden role="dialog" aria-modal="true"><div class="lb-in"></div><p class="lb-cap"></p><button class="lb-x" type="button" aria-label="×">×</button></div>
  <div class="hw" id="hw" hidden>''')

# ---------- CSS ----------
rep('/* poster hero:', r'''/* ===== object card (v6) ===== */
.oc{display:flex;flex-direction:column;background:#fff;min-height:100%;--gold:#A9844C;--gold-soft:rgba(169,132,76,.18)}
.oc-head{position:sticky;top:0;z-index:4;background:#fff;padding:6px 16px 14px;border-bottom:1px solid var(--line);display:flex;flex-direction:column;gap:6px}
.oc-bar{display:flex;justify-content:space-between;align-items:center;gap:8px;margin:0 -6px;min-height:44px}
.oc-x{flex:none;width:44px;height:44px;border-radius:50%;border:none;background:var(--panel-2);font-size:24px;line-height:1;cursor:pointer;display:grid;place-items:center;color:var(--ink-2)}
.oc-x:hover{color:var(--ink);background:#E9EBEE}
.oc-name{font-size:22px;font-weight:700;line-height:1.22;margin:0;letter-spacing:-.01em;text-wrap:balance}
.oc-name:focus{outline:none}.oc-name:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px}
.oc-meta{margin:0;font-size:13.5px;color:var(--ink-2);display:flex;align-items:center;gap:6px 12px;flex-wrap:wrap}
.oc-meta span{display:inline-flex;align-items:center;gap:5px}
.oc-meta svg{width:14px;height:14px;color:var(--ink-3)}
.oc-cat{display:inline-flex;align-items:center;gap:6px;font-size:13px;color:var(--ink-2);font-weight:500}
.oc-cat i{width:20px;height:20px;border-radius:50%;display:grid;place-items:center}
.oc-cat i svg{width:12px;height:12px}
.oc-lead{margin:0;font-size:14px;line-height:1.45;color:var(--ink)}
.oc-acts{display:flex;gap:8px;flex-wrap:wrap;margin-top:6px}
.act{display:inline-flex;align-items:center;gap:7px;min-height:42px;padding:8px 14px;border-radius:999px;background:var(--panel-2);color:var(--ink);text-decoration:none;font-weight:600;font-size:13.5px;border:none;cursor:pointer;white-space:nowrap}
.act:hover{background:#E9EBEE}
.act svg{width:17px;height:17px;flex:none}
.act-go{background:var(--accent);color:#fff}.act-go:hover{background:#178E2F}
.oc-voice{display:contents}
.oc-voice .vrow{display:flex;gap:8px}
.oc-voice small{flex-basis:100%;font-size:12px;color:var(--ink-3);display:flex;align-items:center;gap:6px}
.oc-voice small svg{width:14px;height:14px}
.oc-more{align-self:flex-start;border:none;background:none;color:var(--accent);font-weight:600;padding:4px 0;min-height:40px;cursor:pointer}
.oc-rnav{margin:12px 16px 0}
.oc-img{margin:14px 16px 0}
.oc-zoom{position:relative;display:block;width:100%;height:300px;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#F3F4F2;padding:0;cursor:zoom-in}
.oc-zoom .gen{position:absolute;inset:0}
.oc-zoom img.full{width:100%;height:100%;object-fit:contain;padding:8px}
.oc-zoom img.ph{width:100%;height:100%;object-fit:cover;display:block}
.oc-zoom .crn{position:absolute;left:8px;top:8px;width:46px;height:22px;color:rgba(169,132,76,.6);z-index:3;pointer-events:none}
.oc-img figcaption{font-size:12px;color:var(--ink-3);margin:6px 2px 0;line-height:1.4}
.oc-img figcaption b{color:var(--ink-2);font-weight:600}
.oc-img figcaption a{color:inherit}
.oc-img .thumbs{justify-content:flex-start;margin-top:8px}
.oc-img .thumbs button{width:48px;height:48px;border:1.5px solid var(--line);border-radius:10px}
.oc-img .thumbs button[aria-pressed="true"]{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent-soft)}
.oc-sub{margin:10px 16px 0;font-size:12.5px;color:var(--ink-3)}
.oc-tabs{display:flex;gap:4px;padding:6px 16px 0;border-bottom:1px solid var(--line);margin-top:10px}
.oc-tab{border:none;background:none;padding:10px 10px 11px;font-weight:600;font-size:14px;color:var(--ink-2);border-bottom:2px solid transparent;cursor:pointer;min-height:44px}
.oc-tab[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--accent)}
.oc-body{padding:14px 16px 28px;background:#fff}
.oc-body p{margin:0 0 12px;font-size:14.5px;line-height:1.62;color:var(--ink)}
.oc-body h3{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);margin:18px 0 8px}
.oc-body ol.bio{list-style:none;margin:0;padding:0;border-left:2px solid var(--line)}
.oc-body ol.bio li{position:relative;padding:0 0 10px 16px;font-size:14px;line-height:1.5}
.oc-body ol.bio li::before{content:"";position:absolute;left:-6px;top:6px;width:10px;height:10px;border-radius:50%;background:#fff;border:2px solid var(--accent)}
.oc-body dl{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:0 0 8px;font-size:14px}
.oc-body dt{color:var(--ink-3);font-variant-numeric:tabular-nums}.oc-body dd{margin:0}
.oc-body .muted{color:var(--ink-3);font-size:13px}
.oc-body .near{display:flex;flex-wrap:wrap;gap:6px}
.oc-body .near button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 12px;font-size:13px;cursor:pointer;min-height:36px}
.oc-body .srcs{display:flex;flex-direction:column;gap:5px;border-top:1px solid var(--line);margin-top:16px;padding-top:12px;font-size:12.5px}
.oc-body .srcs b{color:var(--ink-3)!important}
.oc-body .srcs a{color:var(--ink-2)}
.linkbtn{display:inline-flex;align-items:center;gap:7px;border:1px solid var(--line);background:#fff;border-radius:12px;padding:8px 12px;font-size:13.5px;cursor:pointer;min-height:40px;color:var(--ink)}
.linkbtn svg{width:16px;height:16px;color:var(--ink-2)}
.linkbtn:hover{border-color:var(--accent)}
/* enlarged image */
.lb{position:fixed;inset:0;z-index:90;background:rgba(18,22,26,.78);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:16px}
.lb[hidden]{display:none}
.lb-in{position:relative;width:min(92vw,600px);height:min(80vh,900px);border-radius:16px;overflow:hidden;background:#F3F4F2}
.lb-in .gen{position:absolute;inset:0}
.lb-in img.full{width:100%;height:100%;object-fit:contain}
.lb-in img.ph{width:100%;height:100%;object-fit:contain;background:#111}
.lb-cap{margin:0;color:#fff;font-size:13px;max-width:600px;text-align:center}
.lb-cap a{color:#fff}
.lb-x{position:fixed;right:max(14px,env(safe-area-inset-right,0px));top:calc(14px + env(safe-area-inset-top,0px));width:48px;height:48px;border-radius:50%;border:none;background:#fff;font-size:26px;cursor:pointer;display:grid;place-items:center}
@media (max-width:900px){
  .side[data-s="half"]{--sh:52%}
  .oc-head{padding:0 16px 12px}
  .oc-bar{margin:0;min-height:44px}
  .oc-name{font-size:20px}
  .oc-zoom{height:280px}
}

/* poster hero:''')
rep('function sheetH(){const vh=innerHeight,s=side.dataset.s;return s==="hidden"?0:s==="peek"?104:s==="half"?vh*.46:vh-70}',
    'function sheetH(){const vh=innerHeight,s=side.dataset.s;return s==="hidden"?0:s==="peek"?104:s==="half"?vh*.52:vh-70}')

open('premium6.html', 'w', encoding='utf8').write(t)
print('v6 ok', len(t))
