import re
t = open('premium4.html', encoding='utf8').read()
def rep(a, b):
    global t
    assert a in t, 'MISSING: ' + a[:90]
    t = t.replace(a, b, 1)
def cut(start, end, new):
    global t
    i = t.index(start); j = t.index(end, i)
    t = t[:i] + new + t[j:]

# phone head not sticky (tabs are)
rep('.hw-head{padding:14px 16px 0;position:sticky;top:0;background:var(--iv);z-index:3}', '.hw-head{padding:14px 16px 0}')

# i18n keys
rep('m:"м",km:"км",min:"мин",selectDest:"Мақсат таңдалмады"', 'hide:"Панельді жасыру",list:"Тізім",tShort:"Қысқаша",tMore:"Толығырақ",rec:"Көркем реконструкция",recNote:"шартты бейне, бет-бейнесі әдейі салынбаған",origPhoto:"Түпнұсқа портрет",objPhoto:"Нысанның фотосуреті",noImg:"Расталған сурет әлі жоқ",bioH:"Өмір жолы",bioNo:"Өмірбаяны туралы толық тексерілген деректер әлі қосылмаған.",monH:"Ескерткіш туралы",objH:"Нысан туралы",monNo:"Орнатылған жылы мен авторлары туралы тексерілген дерек табылмады.",nearH:"Маңайында",srcH:"Дереккөздер",namesH:"Атаулары",nowName:"Қазіргі атауы",renamedY:"Атау берілген жыл",renamedNo:"расталған дерек жоқ",valueH:"Көшенің тарихи маңызы",valueNo:"Көшенің өз тарихы туралы құжатталған дерек әлі қосылмаған.",streetOf:"Көшесі",monOf:"Ескерткіші",located:"Нысан мына көше маңында орналасқан:",tribe:"руы",byOsm:"OSM деректері бойынша",touristMap:"«Aqtöbe altyn besigim» туристік картасы",m:"м",km:"км",min:"мин",selectDest:"Мақсат таңдалмады"')
rep('m:"м",km:"км",min:"мин",selectDest:"Цель не выбрана"', 'hide:"Скрыть панель",list:"Список",tShort:"Кратко",tMore:"Подробнее",rec:"Художественная реконструкция",recNote:"условный образ, лицо намеренно не прорисовано",origPhoto:"Подлинный портрет",objPhoto:"Фотография объекта",noImg:"Подтверждённого изображения пока нет",bioH:"Жизненный путь",bioNo:"Проверенная подробная биография пока не добавлена.",monH:"О памятнике",objH:"Об объекте",monNo:"Проверенных сведений о годе установки и авторах не найдено.",nearH:"Рядом",srcH:"Источники",namesH:"Названия",nowName:"Современное название",renamedY:"Год присвоения названия",renamedNo:"подтверждённых данных нет",valueH:"Историческое значение улицы",valueNo:"Документированных сведений об истории самой улицы пока нет.",streetOf:"Улица",monOf:"Памятник",located:"Объект находится рядом с улицей:",tribe:"род",byOsm:"по данным OSM",touristMap:"Туристическая карта «Aqtöbe altyn besigim»",m:"м",km:"км",min:"мин",selectDest:"Цель не выбрана"')

# data hook
rep('const CRED=__CRED__;', 'const CRED=__CRED__;\nconst DET=__DET__;')

# free area
cut('function freeArea(){', 'function centerWorld(', '''function freeArea(){const wr=wrap.getBoundingClientRect();const a={l:0,t:0,r:wr.width,b:wr.height};
  if(isPhone()){a.t=64;if(win.open){a.b=Math.max(a.t+60,innerHeight*.22-wr.top)}else a.b=Math.min(a.b,wr.height-sheetH())}
  else{a.r-=70;if(panelOpen===false)a.t=70;
    if(win.open){const br=hwBox.getBoundingClientRect(),gl=br.left-wr.left,gr=wr.right-br.right;
      if(Math.max(gl,gr)>=90){if(gl>=gr){a.r=gl;a.l=0}else{a.l=br.right-wr.left;a.r=wr.width-70>a.l+60?wr.width-70:wr.width}}}}
  return a}
''')

# sheet states
cut('function setSheet(s){', '/* ---------- panel views ---------- */', '''function setSheet(s){side.dataset.s=s;$("grip").setAttribute("aria-expanded",s==="full");updListBtn();requestAnimationFrame(()=>{sheetPx();setTimeout(()=>{sheetPx();scheduleLabels(0)},240)})}
function sheetH(){const vh=innerHeight,s=side.dataset.s;return s==="hidden"?0:s==="peek"?104:s==="half"?vh*.46:vh-70}
function sheetPx(){const h=isPhone()?sheetH():0;wrap.style.setProperty("--sh-px",h+"px");document.documentElement.style.setProperty("--sh-px",h+"px")}
$("grip").onclick=()=>setSheet(side.dataset.s==="full"?"half":"full");

/* ---------- panel show / hide (desktop) and list button ---------- */
let panelOpen=true;try{panelOpen=localStorage.getItem("panel")!=="0"}catch(e){}
const app=document.querySelector(".app");
function keepCenter(change){const c=toWorld(...centerPx());change();requestAnimationFrame(()=>{const [rx,ry]=wrapToRoot(...centerPx());tx=rx-c[0]*k;ty=ry-c[1]*k;clamp();apply(true)})}
function setPanel(open,quiet){const f=()=>{panelOpen=open;app.classList.toggle("nopanel",!open);try{localStorage.setItem("panel",open?"1":"0")}catch(e){}};quiet?f():keepCenter(f);updListBtn();if(!open&&document.activeElement&&side.contains(document.activeElement))$("listbtn").focus()}
function updListBtn(){$("listbtn").setAttribute("aria-expanded",String(isPhone()?side.dataset.s!=="hidden":panelOpen))}
$("hidep").onclick=()=>setPanel(false);
$("listbtn").onclick=()=>{if(isPhone())setSheet(side.dataset.s==="hidden"?"half":"hidden");else setPanel(!panelOpen)};

''')

# home: phone close header
rep('''  pane.innerHTML=`<div class="tabs" role="tablist">''', '''  pane.innerHTML=`<div class="phead"><button class="x" type="button" id="sheetx" aria-label="${T("close")}">×</button></div><div class="tabs" role="tablist">''')
rep('''  $("walkbtn").onclick=openWalk;
  bindRows();''', '''  $("walkbtn").onclick=openWalk;const sx=$("sheetx");if(sx)sx.onclick=()=>setSheet("hidden");
  bindRows();''')

# walk pane bar: back/close leave the walk screen (a running walk keeps going)
rep('''function bindBar(){pane.querySelector("[data-back]").onclick=()=>{if(walk.on&&view!=="walk"){renderWalk()}else closeCard()};pane.querySelector("[data-close]").onclick=closeCard}''',
    '''function bindBar(){const leave=()=>{if(!walk.started)walk.on=false;renderHome()};pane.querySelector("[data-back]").onclick=leave;pane.querySelector("[data-close]").onclick=()=>{leave();if(isPhone())setSheet("hidden")}}''')

# drop the old poster function
cut('function heroHTML(p,f){', 'function onPlaceTap(i,from){', '')

# new window code replaces in-panel cards
cut('function onPlaceTap(i,from){', '/* ---------- search ---------- */', r'''const STFIG={"Шоқан Уәлиханов көшесі":"writer","Мәншүк Мәметова көшесі":"sniper","Махамбет Өтемісов көшесі":"batyr","Аманкелді Иманов көшесі":"batyr","Дінмұхамед Қонаев көшесі":"writer","Есет Батыр көшесі":"batyr","Ғазиза Жұбанова көшесі":"doctor0"};
const placeForStreet=s=>P.find(p=>DET[p.kk]&&DET[p.kk].street===s.kk&&!(s.kk==="Есет Батыр көшесі"));
const streetByKk=kk=>STREETS.find(s=>s.kk===kk);
const orig=src=>src.replace("-portrait.jpg","-orig.jpg");
const KOSH='<path d="M24 21 C24 13 19 6 13 6 C7 6 4 10 4 13 C4 17 8 18 10 16 C12 14 10 11 8 12 M24 21 C24 13 29 6 35 6 C41 6 44 10 44 13 C44 17 40 18 38 16 C36 14 38 11 40 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="24" cy="21" r="1.6" fill="currentColor"/>';
const ORN2=`<svg class="hw-orn" viewBox="0 0 480 22" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs><pattern id="kosh" width="48" height="22" patternUnits="userSpaceOnUse">${KOSH}</pattern></defs><rect width="480" height="22" fill="url(#kosh)"/></svg>`;
const CRN=c=>`<svg class="crn ${c}" viewBox="0 0 48 22" aria-hidden="true">${KOSH}</svg>`;
const win={open:false,t:null,i:-1,saved:null,tab:"short",stage:0};
const hw=$("hw"),hwBox=$("hwBox"),chipst=$("chipst");
function nearestStreetName(x,y){let best=null,bd=80*UPM;for(const s of STREETS){const b=s.bb;if(x<b[0]-bd||x>b[2]+bd||y<b[1]-bd||y>b[3]+bd)continue;for(const c of s.pts)for(let j=1;j<c.length;j++){const d=segDist(x,y,c[j-1],c[j]);if(d<bd){bd=d;best=s}}}return best}
function nearby(x,y,skip){const out=[];P.forEach(p=>{if(p.i===skip)return;const d=distM(x,y,p.x,p.y);if(d<450)out.push({t:"p",i:p.i,d,n:SHORT(p)})});return out.sort((a,b)=>a.d-b.d).slice(0,6)}
function stageFor(kind,o){const items=[];
  if(kind==="p"){const f=FIG[o.kk];if(f)items.push({k:"fig",t:f.t});if(o.por)items.push({k:"por",src:orig(o.por.src),cap:`${esc(o.por.note[li()])}. ${esc(o.por.by)}, <a href="${o.por.page}" target="_blank" rel="noopener">${esc(o.por.lic)}</a> · Wikimedia Commons`});
    if(o.ph)items.push({k:"ph",src:o.ph.src,cap:`${esc(o.ph.by)}, <a href="${o.ph.page}" target="_blank" rel="noopener">${esc(o.ph.lic)}</a> · Wikimedia Commons`})}
  else{const st=o.story,lp=placeForStreet(o),ft=(lp&&FIG[lp.kk]&&FIG[lp.kk].t)||STFIG[o.kk];if(ft&&ft!=="doctor0"&&!st.event)items.push({k:"fig",t:ft});
    if(st.por)items.push({k:"por",src:imgUrl(st.por).replace("-portrait.jpg","-orig.jpg"),cap:credit(st.por)});
    if(st.ph)items.push({k:"ph",src:imgUrl(st.ph),cap:credit(st.ph)})}
  return items}
function stageHTML(items,cat){const it=items[win.stage]||items[0];let body,cap;
  if(!it){body=`<div class="noimg"><i class="bg-${cat}">${svgI(cat==="st"?"st":cat,"#fff")}</i>${T("noImg")}</div>`;cap=""}
  else if(it.k==="fig"){body=figSVG(it.t);cap=`<b>${T("rec")}</b> · ${T("recNote")}`}
  else if(it.k==="por"){body=`<img class="full" src="${it.src}" alt="${T("origPhoto")}">`;cap=`<b>${T("origPhoto")}</b> · ${it.cap}`}
  else{body=`<img class="ph" src="${it.src}" alt="${T("objPhoto")}">`;cap=`<b>${T("objPhoto")}</b> · ${it.cap}`}
  const thumbs=items.length>1?`<div class="thumbs">${items.map((x,n)=>`<button type="button" data-st="${n}" aria-pressed="${n===win.stage}" aria-label="${x.k==="fig"?T("rec"):x.k==="por"?T("origPhoto"):T("objPhoto")}">${x.k==="fig"?figSVG(x.t):`<img src="${x.src}" alt="">`}</button>`).join("")}</div>`:"";
  return `<div class="frame">${CRN("tl")}${CRN("tr")}${CRN("bl")}${CRN("br")}${body}</div><p class="scap">${cap}</p>${thumbs}`}
function srcList(arr){return `<div class="srcs"><b style="color:var(--gold);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase">${T("srcH")}</b>${arr.filter(Boolean).map(([n,u])=>u?`<a href="${u}" target="_blank" rel="noopener">${esc(n)}</a>`:`<span>${esc(n)}</span>`).join("")}</div>`}
function renewYear(s){const st=s.story;if(st&&st.renamed)return st.renamed;let y=null;(s.olds||[]).forEach(o=>{const m=(o.p||"").match(/(\d{4})\s*$/);if(m&&(!y||+m[1]>+y))y=m[1]});return y}
function placeWin(p){const d=DET[p.kk]||{},f=FIG[p.kk],t=p.tour&&TOURS[p.tour];
  const pano=`https://yandex.kz/maps/?ll=${p.lon},${p.lat}&z=18&l=stv,sta&panorama%5Bpoint%5D=${p.lon},${p.lat}`,gis=`https://2gis.kz/aktobe/geo/${p.lon},${p.lat}`;
  const ns=nearestStreetName(p.x,p.y);
  const short=d.short?d.short[li()]:`${DESC(p)}${ns?" "+T("located")+" "+SN(ns)+".":""}`;
  const ls=d.street&&streetByKk(d.street);
  const inRoute=rIdx>=0&&route[rIdx]===p.i;
  const acts=`<div class="hw-acts">${t?`<a class="primary" href="${t.u}" target="_blank" rel="noopener">${UI.tour}${T("tour")}</a><a class="sec" href="${pano}" target="_blank" rel="noopener">${UI.pano}${T("pano")}</a>`:`<a class="primary" href="${pano}" target="_blank" rel="noopener">${UI.pano}${T("pano")}</a>`}<a class="sec" href="${gis}" target="_blank" rel="noopener">${UI.pin}${T("gis")}</a>${ls?`<button class="sec" type="button" data-go="s${ls.i}">${svgI("st")}${T("streetOf")}: ${esc(SN(ls))}</button>`:""}</div>`;
  const rn=inRoute?`<div class="rnav"><span>${T("stopN")} ${rIdx+1} / ${route.length}</span><div><button type="button" data-r="-1" ${rIdx===0?"disabled":""} aria-label="${T("prev")}">←</button><button type="button" data-r="1" ${rIdx===route.length-1?"disabled":""}>${T("next")} →</button></div></div>`:"";
  const nb=nearby(p.x,p.y,p.i);
  const isPerson=!!f;
  const more=`${isPerson?`<h3>${T("bioH")}</h3>${d.bio?`<ol class="bio">${d.bio.map(b=>`<li>${esc(b[li()])}</li>`).join("")}</ol>`:`<p class="muted">${T("bioNo")}</p>`}`:`<h3>${T("objH")}</h3><p>${esc(DESC(p))}</p>`}
    <h3>${p.c==="rel"||p.c==="mus"?T("objH"):T("monH")}</h3><dl>${p.code?`<dt>${T("touristMap")}</dt><dd>${p.code}</dd>`:""}<dt>${L==="kk"?"Орны":"Место"}</dt><dd>${ns?esc(SN(ns)):"—"}</dd></dl><p class="muted" style="margin-top:8px">${T("monNo")}</p>
    ${nb.length?`<h3>${T("nearH")}</h3><div class="near">${nb.map(n=>`<button type="button" data-go="p${n.i}">${esc(n.n)} · ${fmtDist(n.d)}</button>`).join("")}</div>`:""}
    ${srcList([d.wiki&&["Wikipedia",d.wiki],[p.out?"OpenStreetMap: контур":"OpenStreetMap",p.outSrc||`https://www.openstreetmap.org/?mlat=${p.lat}&mlon=${p.lon}#map=18/${p.lat}/${p.lon}`],p.por&&["Wikimedia Commons: "+(L==="kk"?"портрет":"портрет"),p.por.page],p.ph&&["Wikimedia Commons: "+(L==="kk"?"фото":"фото"),p.ph.page],p.code&&[T("touristMap")+" — "+p.code,null],t&&["visitaktobe.kz — 3D",t.u]])}`;
  const pills=[f&&CAP(p)?CAP(p):null,f&&f.tribe?f.tribe[li()]+" "+T("tribe"):null].filter(Boolean);
  return {cat:p.c,catName:CATS[p.c][li()],name:f&&f.name?f.name[li()]:NAME(p),alt:f&&f.name?NAME(p):ALT(p),pills,items:stageFor("p",p),short:`${rn}<p>${esc(short)}</p>${acts}`,more}}
function streetWin(s){const st=s.story,lp=placeForStreet(s);
  const per=x=>x.p?x.p.replace(/^-/,"–").replace(/-/,"–"):"";
  const olds=s.olds.filter(o=>o.p||!s.olds.some(q=>q.p&&fold(q.ru||q.kk||"").includes(fold((o.ru||o.kk||"").replace(/^ул\.?\s*/,"")))));
  const named=st.event?"":(L==="kk"?`Көше ${st.who[0]} құрметіне аталған. `:`Улица названа в честь: ${st.who[1]}. `);
  const short=`${named}${st.bio[li()]}${st.note?" "+st.note[li()]:""}`;
  const y=renewYear(s);
  const acts=`<div class="hw-acts"><a class="sec" href="https://2gis.kz/aktobe/search/${encodeURIComponent(s.ru)}" target="_blank" rel="noopener">${UI.pin}${T("gis")}</a>${lp?`<button class="sec" type="button" data-go="p${lp.i}">${svgI(lp.c)}${T("monOf")}: ${esc(SHORT(lp))}</button>`:""}</div>`;
  const d=lp&&DET[lp.kk];
  const more=`<h3>${T("namesH")}</h3><dl><dt>${T("nowName")}</dt><dd>${esc(s.kk)}<br>${esc(s.ru)}</dd>${olds.map(o=>`<dt>${esc(per(o))||"—"}</dt><dd>${esc((L==="kk"?(o.kk||o.ru):(o.ru||o.kk))||"")}</dd>`).join("")}<dt>${T("renamedY")}</dt><dd>${y?esc(y)+(st.renamed?"":" ("+T("byOsm")+")"):T("renamedNo")}</dd></dl>
    <h3>${T("valueH")}</h3>${st.note?`<p>${esc(st.note[li()])}</p>`:`<p class="muted">${T("valueNo")}</p>`}
    <h3>${T("bioH")}: ${esc(st.who[li()])}</h3>${d&&d.bio?`<ol class="bio">${d.bio.map(b=>`<li>${esc(b[li()])}</li>`).join("")}</ol>`:`<p>${esc(st.bio[li()])}</p>`}
    ${srcList([[T("osmWay"),`https://www.openstreetmap.org/way/${s.id}`],...st.src,st.por&&["Wikimedia Commons: портрет",CRED[st.por]&&CRED[st.por].page],st.ph&&["Wikimedia Commons: фото",CRED[st.ph]&&CRED[st.ph].page]])}`;
  return {cat:"st",catName:T("street"),name:SN(s),alt:SA(s),pills:[st.who[li()],st.dates].filter(Boolean),items:stageFor("s",s),short:`<p>${esc(short)}</p><div class="voice" id="voice"></div>${acts}`,more}}
function renderWin(){const o=win.t==="p"?P[win.i]:STREETS[win.i];const w=win.t==="p"?placeWin(o):streetWin(o);
  hwBox.innerHTML=`${ORN2}<div class="hw-left">${stageHTML(w.items,w.cat)}</div>
   <div class="hw-right"><div class="hw-head"><div><div class="hw-cat">${esc(w.catName)}</div><h2 class="hw-name" id="hwName">${esc(w.name)}</h2><p class="hw-alt">${esc(w.alt)}</p>${w.pills.length?`<div class="pills">${w.pills.map(x=>`<span>${esc(x)}</span>`).join("")}</div>`:""}</div>
     <button class="hw-x" id="hwClose" type="button" aria-label="${T("close")}">×</button></div>
    <div class="hw-tabs" role="tablist"><button class="hw-tab" role="tab" id="tb-short" aria-controls="tp" aria-selected="${win.tab==="short"}" data-tab="short">${T("tShort")}</button><button class="hw-tab" role="tab" id="tb-more" aria-controls="tp" aria-selected="${win.tab==="more"}" data-tab="more">${T("tMore")}</button></div>
    <div class="hw-body" id="tp" role="tabpanel" aria-labelledby="tb-${win.tab}">${win.tab==="short"?w.short:w.more}</div></div>`;
  $("hwClose").onclick=closeWin;
  hwBox.querySelectorAll("[data-tab]").forEach(b=>b.onclick=()=>{win.tab=b.dataset.tab;renderWin();hwBox.querySelector(`[data-tab="${win.tab}"]`).focus()});
  hwBox.querySelectorAll("[data-st]").forEach(b=>b.onclick=()=>{win.stage=+b.dataset.st;renderWin()});
  hwBox.querySelectorAll("[data-go]").forEach(b=>b.onclick=()=>{const g=b.dataset.go,i=+g.slice(1);g[0]==="p"?openPlace(i,{zoom:true}):openStreet(i,{fit:true})});
  hwBox.querySelectorAll("[data-r]").forEach(b=>b.onclick=()=>{rIdx+=+b.dataset.r;openPlace(route[rIdx],{zoom:true,keepRoute:true})});
  if(win.t==="s")renderVoice(win.i);
}
function placeWinBox(){if(isPhone()){hwBox.style.left="";hwBox.style.width="";return}const wr=wrap.getBoundingClientRect();const bw=Math.min(Math.max(680,Math.min(980,wr.width-300)),wr.width-24);hwBox.style.width=bw+"px";hwBox.style.left=(wr.left+(wr.width-bw)/2)+"px"}
function openWin(tk,i,opt={}){if(!win.open){win.saved={k,tx,ty};lastFocus=opt.from||document.activeElement}
  win.open=true;win.t=tk;win.i=i;win.tab="short";win.stage=0;hideChip();pv.hidden=true;hover(null);
  renderWin();hw.hidden=false;placeWinBox();hwBox.scrollTop=0;
  requestAnimationFrame(()=>{$("hwClose").focus({preventScroll:true});
    if(tk==="p"){const p=P[i];centerWorld(p.x,p.y,Math.max(k,opt.zoom?(p.out?6:3.6):k))}else{const s=STREETS[i];fitBox(...s.bb,6)}});
  scheduleLabels(0)}
function closeWin(){if(!win.open)return;win.open=false;hw.hidden=true;if(voice.state!=="idle"&&win.t==="s")stopVoice();
  sel=null;rIdx=-1;P.forEach(o=>o.el.classList.remove("on","hl"));$("olSel").classList.remove("show");$("stSel").style.display="none";$("stHov").style.display="none";
  const s=win.saved;win.saved=null;if(s)animateTo(s.k,s.tx,s.ty);
  if(view==="home")renderHome();
  scheduleLabels(0);const back=lastFocus;if(back&&document.contains(back)&&back!==document.body)back.focus({preventScroll:true})}
$("hwBack").onclick=closeWin;
hw.addEventListener("keydown",e=>{if(e.key==="Tab"){const f=[...hwBox.querySelectorAll('button,a[href],[tabindex="0"]')].filter(x=>x.offsetParent!==null);if(!f.length)return;const a=f[0],z=f[f.length-1];if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}}});
function showChip(s){chipst.innerHTML=`<div><b>${esc(SN(s))}</b><span>${esc(SA(s))}</span></div><button class="x" type="button" aria-label="${T("close")}">×</button>`;chipst.hidden=false;chipst.querySelector(".x").onclick=()=>{hideChip();sel=null;$("stSel").style.display="none";scheduleLabels(0)}}
function hideChip(){chipst.hidden=true}
function onPlaceTap(i,from){if(walk.on&&walk.mode==="dest"&&!walk.started){walk.dest=i;renderWalk();return}openPlace(i,{from})}
function openPlace(i,opt={}){const p=P[i];if(!opt.keepRoute)rIdx=-1;sel={t:"p",i};
  P.forEach(o=>o.el.classList.toggle("on",o.i===i));mg.appendChild(p.el);p.el.classList.remove("gone");
  const ol=$("olSel");if(p.out){ol.setAttribute("d",p.out);ol.classList.add("show")}else ol.classList.remove("show");
  $("stSel").style.display="none";openWin("p",i,opt);if(view==="home")renderHome()}
function openStreet(i,opt={}){const s=STREETS[i];sel={t:"s",i};
  P.forEach(o=>o.el.classList.remove("on"));$("olSel").classList.remove("show");
  const hi=$("stSel");hi.setAttribute("d",s.d);hi.style.display="";$("stHov").style.display="none";pv.hidden=true;
  if(s.story){openWin("s",i,opt);return}
  if(win.open){win.open=false;hw.hidden=true;win.saved=null}
  showChip(s);if(opt.fit)fitBox(...s.bb,6);scheduleLabels(0)}
function closeCard(){if(win.open)closeWin();else{hideChip();sel=null;$("stSel").style.display="none";scheduleLabels(0)}}
document.addEventListener("keydown",e=>{if(e.key==="Escape"){if(!$("results").hidden){hideResults();return}if(win.open){closeWin();return}if(!chipst.hidden){closeCard();return}hover(null)}});

''')

# voice refresh hooks
rep('if("speechSynthesis"in window){loadVoices();speechSynthesis.onvoiceschanged=()=>{loadVoices();if(view==="street"&&sel)renderVoice(sel.i)}}',
    'if("speechSynthesis"in window){loadVoices();speechSynthesis.onvoiceschanged=()=>{loadVoices();if(win.open&&win.t==="s")renderVoice(win.i)}}')
rep('function refreshVoice(){if(view==="street"&&sel&&sel.t==="s")renderVoice(sel.i)}', 'function refreshVoice(){if(win.open&&win.t==="s")renderVoice(win.i)}')

# walk opens the panel / sheet
rep('function openWalk(){walk.on=true;hideResults();', 'function openWalk(){walk.on=true;hideResults();if(win.open)closeWin();if(!isPhone()&&!panelOpen)setPanel(true);')

# map click: plain area hides the street chip
rep('  if(s)openStreet(s.i,{from:null});else if(sel){closeCard()}', '  if(s)openStreet(s.i,{from:null});else if(!chipst.hidden)closeCard()')

# labels avoid the chip / window
rep('  block(document.querySelector(".ctrl"));', '  block(document.querySelector(".ctrl"));block(chipst);if(win.open)block(hwBox);if(!panelOpen&&!isPhone())block(document.querySelector(".top"));')

# language refresh
rep('if(view==="place"&&sel)openPlace(sel.i,{keepRoute:true,from:lastFocus});else if(view==="street"&&sel)openStreet(sel.i,{from:lastFocus});else if(view==="walk")renderWalk();else renderHome();',
    'if(view==="walk")renderWalk();else renderHome();if(win.open)renderWin();if(!chipst.hidden&&sel&&sel.t==="s")showChip(STREETS[sel.i]);')

# resize keeps window centred over the map
rep('addEventListener("resize",()=>{sheetPx();apply(true)});', 'addEventListener("resize",()=>{sheetPx();if(win.open)placeWinBox();updListBtn();apply(true)});')

# start
rep('setLang(L);sheetPx();startView();apply(true);', 'if(isPhone())side.dataset.s="hidden";setPanel(panelOpen||isPhone(),true);setLang(L);sheetPx();startView();apply(true);')

# arrival toast etc. used openPlace({zoom}) - still fine. walk opened from sheet on phone
open('premium4.html', 'w', encoding='utf8').write(t)
print('js ok', len(t))
