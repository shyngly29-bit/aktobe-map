// Student presentation (Kazakh) for «Ақтөбе ескерткіштері».  node build_deck.js OUT.pptx
const pptxgen = require("pptxgenjs");
const path = require("path");
const { applyTheme } = require(process.env.APPLY_THEME);
const OUT = process.argv[2];
const A = (f) => path.join(__dirname, "deck_assets", f);

const THEME = {
  name: "Aktobe Steppe Night",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1A1F2B", lt1: "FFFFFF", dk2: "14213D", lt2: "F3F5F8",
    accent1: "B0843E", accent2: "1C7C7D", accent3: "C2582D", accent4: "4F6B7A", accent5: "7350B0", accent6: "1C7F8C",
    hlink: "1C7C7D", folHlink: "4F6B7A",
  },
};
const HEX = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.title = "Ақтөбе қаласының тарихи-мәдени ескерткіштері";
pres.author = "Оқушы жобасы";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "DARK",
  background: { color: C.text2 },
  objects: [
    { image: { path: A("kosh_gold.png"), x: 0.6, y: 0.55, w: 1.1, h: 0.5 } },
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 1.5, w: 7.2, h: 2.4, fontFace: THEME.headFontFace, fontSize: 40, bold: true, color: C.background1, valign: "top", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 4.0, w: 7.2, h: 1.0, fontSize: 22, color: C.accent1, italic: true, valign: "top", align: "left", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: C.background1 },
  objects: [
    { image: { path: A("kosh_gold.png"), x: 12.0, y: 0.5, w: 0.8, h: 0.37 } },
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.42, w: 11.2, h: 0.8, fontFace: THEME.headFontFace, fontSize: 34, bold: true, color: C.text2, valign: "middle", align: "left", margin: 0 }, text: "" } },
    { text: { text: "Ақтөбе ескерткіштері", options: { x: 0.6, y: 7.0, w: 5, h: 0.3, fontSize: 10, color: C.accent4, margin: 0 } } },
  ],
  slideNumber: { x: 12.3, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: HEX.accent4, align: "right" },
});

const sh = () => ({ type: "outer", color: "14213D", opacity: 0.16, blur: 10, offset: 3, angle: 90 });

// ---------- 1. title ----------
pres.addSection({ title: "Кіріспе" });
let s = pres.addSlide({ masterName: "DARK", sectionTitle: "Кіріспе" });
s.addText("Ақтөбе қаласының тарихи-мәдени ескерткіштері", { placeholder: "title" });
s.addText("тарихи жадыны сақтаудағы маңызы", { placeholder: "body" });
s.addText([
  { text: "Орындаған: ______________________", options: { breakLine: true } },
  { text: "Жетекшісі: ______________________" },
], { x: 0.6, y: 5.6, w: 6.5, h: 0.9, fontSize: 16, color: C.background2, margin: 0, paraSpaceAfter: 6, isTextBox: true, objectName: "authors" });
[["abilkaiyr", 8.15], ["aiteke", 9.75], ["aliya", 11.35]].forEach(([n, x], i) => {
  const h = i === 1 ? 5.6 : 5.0, w = h * 0.66;
  s.addImage({ path: A(n + ".png"), x: x - w / 2 + 0.6, y: 7.0 - h, w, h, objectName: "figure-" + n, altText: "Көркем реконструкция" });
});
s.addText("Суреттер — көркем реконструкция", { x: 8.6, y: 7.05, w: 4.2, h: 0.3, fontSize: 10, color: C.background2, align: "right", margin: 0, isTextBox: true });
s.addNotes("Сәлеметсіздер ме! Менің жобамның тақырыбы — «Ақтөбе қаласының тарихи-мәдени ескерткіштері: тарихи жадыны сақтаудағы маңызы». Мен қаламыздың ескерткіштері мен көшелерінің тарихын жинап, оны интерактивті картаға айналдырдым.");

// ---------- 2. relevance ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Кіріспе" });
s.addText("Неге бұл тақырып маңызды", { placeholder: "title" });
s.addText("Біз күн сайын ескерткіштер мен көшелердің жанынан өтеміз. Бірақ олардың кімнің құрметіне аталғанын, бұрын қалай аталғанын көбіміз білмейміз. Тарихи жады осылай біртіндеп ұмытылады.", {
  x: 0.6, y: 1.6, w: 5.2, h: 3.2, fontSize: 20, color: C.text1, margin: 0, valign: "top", lineSpacingMultiple: 1.15, isTextBox: true, objectName: "relevance-text" });
[["38", "тарихи-мәдени нысан картада"], ["350", "көше атауы қала орталығында"], ["116", "көшенің бұрынғы атауы бар"]].forEach(([n, l], i) => {
  const y = 1.45 + i * 1.75;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.6, y, w: 6.1, h: 1.5, rectRadius: 0.12, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: "stat-card-" + i });
  s.addText(n, { x: 6.9, y: y + 0.15, w: 2.2, h: 1.2, fontFace: THEME.headFontFace, fontSize: 54, bold: true, color: C.accent1, margin: 0, valign: "middle", isTextBox: true });
  s.addText(l, { x: 9.2, y: y + 0.15, w: 3.3, h: 1.2, fontSize: 18, color: C.text2, margin: 0, valign: "middle", isTextBox: true });
});
s.addText("Дереккөз: OpenStreetMap, «Aqtöbe altyn besigim» туристік картасы", { x: 0.6, y: 6.5, w: 7, h: 0.3, fontSize: 11, color: C.accent4, margin: 0, isTextBox: true });
s.addNotes("Біз күнде көретін ескерткіштер мен көшелердің тарихын көпшілік біле бермейді. Менің картамда 38 тарихи-мәдени нысан бар, қала орталығында 350 көше атауы көрсетілген, олардың 116-сының бұрынғы атауы бар. Әр атаудың артында бір тарих тұр.");

// ---------- 3. goal & tasks ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Кіріспе" });
s.addText("Жобаның мақсаты мен міндеттері", { placeholder: "title" });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 1.5, w: 4.8, h: 4.9, rectRadius: 0.15, fill: { color: C.text2 }, line: { color: C.text2 }, objectName: "goal-card" });
s.addImage({ path: A("kosh_gold.png"), x: 0.95, y: 1.85, w: 0.9, h: 0.41 });
s.addText("Мақсаты", { x: 0.95, y: 2.45, w: 4.1, h: 0.5, fontFace: THEME.headFontFace, fontSize: 24, bold: true, color: C.accent1, margin: 0, isTextBox: true });
s.addText("Ақтөбенің тарихи-мәдени ескерткіштері мен көшелерінің тарихын жинап, оны бәріне қолжетімді интерактивті картаға айналдыру.", {
  x: 0.95, y: 3.05, w: 4.1, h: 3.0, fontSize: 19, color: C.background1, margin: 0, valign: "top", lineSpacingMultiple: 1.12, isTextBox: true });
["Ескерткіштер мен көшелер туралы деректерді жинау", "Деректерді тексеріп, дереккөздерін көрсету", "Қазақ және орыс тілдеріндегі интерактивті карта жасау", "Картаны оқушылар мен қала тұрғындарына ұсыну"].forEach((t, i) => {
  const y = 1.55 + i * 1.22;
  s.addShape(pres.shapes.OVAL, { x: 6.0, y: y + 0.1, w: 0.75, h: 0.75, fill: { color: C.accent2 }, line: { color: C.accent2 }, objectName: "task-num-" + (i + 1) });
  s.addText(String(i + 1), { x: 6.0, y: y + 0.1, w: 0.75, h: 0.75, fontSize: 22, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText(t, { x: 7.0, y, w: 5.7, h: 0.95, fontSize: 19, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
});
s.addNotes("Жобамның мақсаты — қаламыздың ескерткіштері мен көшелерінің тарихын жинап, оны бәріне қолжетімді интерактивті картаға айналдыру. Ол үшін төрт міндет қойдым: деректерді жинау, оларды тексеру, екі тілде карта жасау және картаны көпшілікке ұсыну.");

// ---------- 4. sources & methods ----------
pres.addSection({ title: "Зерттеу" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Зерттеу" });
s.addText("Дереккөздер мен әдістер", { placeholder: "title" });
[["Т", "Туристік карта", "«Aqtöbe altyn besigim»: 38 нысанның тізімі, QR-кодтар арқылы 3D-турлар", "accent3"],
 ["O", "OpenStreetMap", "Көшелердің сызықтары, координаттар, бұрынғы атаулары мен жылдары", "accent2"],
 ["W", "Википедия", "Тарихи тұлғалардың өмірбаяны, көшелердің қайта аталуы", "accent4"],
 ["C", "Wikimedia Commons", "Еркін лицензиялы портреттер мен фотосуреттер, авторлары көрсетілген", "accent5"]].forEach(([ic, h, b, col], i) => {
  const x = 0.6 + (i % 2) * 6.15, y = 1.5 + Math.floor(i / 2) * 2.55;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 5.95, h: 2.3, rectRadius: 0.12, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: "source-card-" + i });
  s.addShape(pres.shapes.OVAL, { x: x + 0.35, y: y + 0.4, w: 0.85, h: 0.85, fill: { color: C[col] }, line: { color: C[col] } });
  s.addText(ic, { x: x + 0.35, y: y + 0.4, w: 0.85, h: 0.85, fontSize: 24, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText(h, { x: x + 1.45, y: y + 0.35, w: 4.2, h: 0.5, fontSize: 21, bold: true, color: C.text2, margin: 0, isTextBox: true });
  s.addText(b, { x: x + 1.45, y: y + 0.9, w: 4.2, h: 1.2, fontSize: 16, color: C.text1, margin: 0, valign: "top", isTextBox: true });
});
s.addNotes("Деректерді төрт дереккөзден алдым. Туристік картадан ескерткіштер тізімін және 3D-турлардың сілтемелерін алдым. OpenStreetMap — көшелер мен координаттар үшін. Википедиядан тұлғалардың өмірбаяны мен көшелердің қайта аталуын тексердім. Суреттер Wikimedia Commons-тан алынды, авторлары көрсетілген.");

// ---------- 5. monuments on the map ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Зерттеу" });
s.addText("Картадағы 38 нысан", { placeholder: "title" });
s.addChart(pres.charts.BAR, [{ name: "Нысандар", labels: ["Ескерткіштер", "Мемориалдар", "Мұражайлар", "Діни ғимараттар"], values: [19, 8, 6, 5] }], {
  x: 0.5, y: 1.4, w: 5.0, h: 5.0, barDir: "bar", chartColors: [HEX.accent3, HEX.accent4, HEX.accent6, HEX.accent5],
  showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 16, dataLabelColor: HEX.dk2, dataLabelFontFace: "+mn-lt",
  catAxisLabelFontSize: 15, catAxisLabelColor: HEX.dk2, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
  catAxisOrientation: "maxMin", showLegend: false, showTitle: false, barGapWidthPct: 45, objectName: "category-chart" });
s.addImage({ path: A("d_home.png"), x: 5.9, y: 1.45, w: 6.85, h: 6.85 * 900 / 1600, objectName: "map-screenshot", altText: "Интерактивті картаның жалпы көрінісі" });
s.addText("Картаның жалпы көрінісі: ескерткіштер, мемориалдар, мұражайлар және ғибадатханалар", { x: 5.9, y: 5.45, w: 6.85, h: 0.6, fontSize: 13, color: C.accent4, margin: 0, isTextBox: true });
s.addNotes("Картада 38 нысан бар: 19 ескерткіш, 8 мемориал, 6 мұражай және 5 діни ғимарат. Әр санаттың өз белгісі мен түсі бар, сондықтан картадан оларды бірден ажыратуға болады.");

// ---------- 6. historical figures ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Зерттеу" });
s.addText("Ақтөбенің тарихи тұлғалары", { placeholder: "title" });
[["abilkaiyr", "Әбілқайыр хан", "1693–1748 · Кіші жүз ханы"], ["aiteke", "Әйтеке би", "Үш ұлы бидің бірі"], ["aliya", "Әлия Молдағұлова", "1925–1944 · мерген, Кеңес Одағының Батыры"], ["patsaev", "Виктор Пацаев", "1933–1971 · Ақтөбеде туған ғарышкер"]].forEach(([n, nm, cap], i) => {
  const x = 0.6 + i * 3.08;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.4, w: 2.88, h: 5.25, rectRadius: 0.14, fill: { color: C.background2 }, line: { color: C.background2 }, shadow: sh(), objectName: "person-card-" + i });
  const h = 3.4, w = h * 0.64;
  s.addImage({ path: A(n + ".png"), x: x + (2.88 - w) / 2, y: 1.55, w, h, altText: "Көркем реконструкция: " + nm });
  s.addText(nm, { x: x + 0.2, y: 5.05, w: 2.5, h: 0.5, fontSize: 18, bold: true, color: C.text2, margin: 0, isTextBox: true });
  s.addText(cap, { x: x + 0.2, y: 5.55, w: 2.5, h: 0.9, fontSize: 14, color: C.text1, margin: 0, valign: "top", isTextBox: true });
});
s.addText("Суреттер — көркем реконструкция, архив фотосы емес. Картада барлығы 16 тарихи тұлға бар.", { x: 0.6, y: 6.68, w: 11, h: 0.3, fontSize: 11, color: C.accent4, margin: 0, isTextBox: true });
s.addNotes("Картада 16 тарихи тұлға бар. Олардың арасында Кіші жүздің ханы Әбілқайыр, үш ұлы бидің бірі Әйтеке би, Кеңес Одағының Батыры мерген Әлия Молдағұлова және Ақтөбеде туған ғарышкер Виктор Пацаев бар. Әр тұлға толық бойлы көркем бейнемен көрсетілген. Бұл — көркем реконструкция, архив фотосы емес.");

// ---------- 7. street history ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Зерттеу" });
s.addText("Көшелердің бұрынғы атаулары", { placeholder: "title" });
s.addText("Шоқан Уәлиханов көшесі", { x: 0.6, y: 1.45, w: 8, h: 0.5, fontSize: 22, bold: true, color: C.text2, margin: 0, isTextBox: true });
const tl = [["1878–1920", "Инженерная"], ["1920–1992", "Орджоникидзе"], ["1992–2000", "Көкжар"], ["2000 жылдан", "Шоқан Уәлиханов"]];
s.addShape(pres.shapes.LINE, { x: 1.2, y: 2.75, w: 11.0, h: 0, line: { color: HEX.accent1, width: 2 }, objectName: "timeline-1" });
tl.forEach(([y, nm], i) => {
  const x = 1.2 + i * 3.67, last = i === tl.length - 1;
  s.addShape(pres.shapes.OVAL, { x: x - 0.18, y: 2.57, w: 0.36, h: 0.36, fill: { color: last ? C.accent2 : C.background1 }, line: { color: last ? C.accent2 : C.accent1, width: 2 } });
  s.addText(y, { x: x - 1.2, y: 2.05, w: 2.4, h: 0.4, fontSize: 15, color: C.accent4, align: "center", margin: 0, isTextBox: true });
  s.addText(nm, { x: x - 1.5, y: 3.05, w: 3.0, h: 0.5, fontSize: 18, bold: last, color: last ? C.accent2 : C.text1, align: "center", margin: 0, isTextBox: true });
});
s.addText("Әбілқайыр хан даңғылы", { x: 0.6, y: 4.1, w: 8, h: 0.5, fontSize: 22, bold: true, color: C.text2, margin: 0, isTextBox: true });
const tl2 = [["1967 жылға дейін", "Жеңіс даңғылы"], ["16 маусым 1967", "Ленин даңғылы"], ["23 қазан 1997", "Әбілқайыр хан даңғылы"]];
s.addShape(pres.shapes.LINE, { x: 1.2, y: 5.4, w: 7.4, h: 0, line: { color: HEX.accent1, width: 2 }, objectName: "timeline-2" });
tl2.forEach(([y, nm], i) => {
  const x = 1.2 + i * 3.7, last = i === tl2.length - 1;
  s.addShape(pres.shapes.OVAL, { x: x - 0.18, y: 5.22, w: 0.36, h: 0.36, fill: { color: last ? C.accent2 : C.background1 }, line: { color: last ? C.accent2 : C.accent1, width: 2 } });
  s.addText(y, { x: x - 1.3, y: 4.7, w: 2.6, h: 0.4, fontSize: 15, color: C.accent4, align: "center", margin: 0, isTextBox: true });
  s.addText(nm, { x: x - 1.5, y: 5.7, w: 3.0, h: 0.5, fontSize: 18, bold: last, color: last ? C.accent2 : C.text1, align: "center", margin: 0, isTextBox: true });
});
s.addText("Дереккөз: OpenStreetMap; Википедия, «Проспект Абилкайыр-хана», «Переименованные улицы Актобе»", { x: 0.6, y: 6.55, w: 11, h: 0.3, fontSize: 11, color: C.accent4, margin: 0, isTextBox: true });
s.addNotes("Көшелердің де өз тарихы бар. Мысалы, Шоқан Уәлиханов көшесі бұрын Инженерная, кейін Орджоникидзе, одан соң Көкжар деп аталған, ал 2000 жылдан бастап Шоқан Уәлиханов есімін алған. Қаланың орталық даңғылы 1967 жылға дейін Жеңіс даңғылы, кейін Ленин даңғылы болған, ал 1997 жылдың 23 қазанында Әбілқайыр хан есімі берілген.");

// ---------- 8. the app ----------
pres.addSection({ title: "Нәтиже" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Нәтиже" });
s.addText("Интерактивті карта", { placeholder: "title" });
s.addImage({ path: A("d_place.png"), x: 0.6, y: 1.45, w: 6.6, h: 6.6 * 1080 / 1500, objectName: "card-screenshot", altText: "Абай ескерткішінің карточкасы" });
[["Ескерткішті бас", "қысқаша және толық тарих, сурет, 3D-тур"], ["Көшені бас", "бұрынғы атаулары мен жылдары"], ["Іздеу", "қазіргі және бұрынғы атау бойынша"], ["Тыңдау", "көше тарихын дауыстап оқу"]].forEach(([h, b], i) => {
  const y = 1.55 + i * 1.18;
  s.addShape(pres.shapes.OVAL, { x: 7.65, y: y + 0.05, w: 0.6, h: 0.6, fill: { color: C.accent2 }, line: { color: C.accent2 } });
  s.addImage({ path: A("kosh_white.png"), x: 7.7, y: y + 0.24, w: 0.5, h: 0.23 });
  s.addText(h, { x: 8.45, y, w: 4.3, h: 0.45, fontSize: 20, bold: true, color: C.text2, margin: 0, isTextBox: true });
  s.addText(b, { x: 8.45, y: y + 0.45, w: 4.3, h: 0.5, fontSize: 16, color: C.text1, margin: 0, isTextBox: true });
});
s.addNotes("Нәтижесінде интерактивті карта жасадым. Ескерткішті басқанда оның қысқаша және толық тарихы, суреті және бар болса 3D-туры ашылады. Көшені басқанда оның бұрынғы атаулары шығады. Іздеуде қазіргі атаумен де, бұрынғы атаумен де табуға болады, ал кейбір көшелердің тарихын тыңдауға да болады.");

// ---------- 9. phone & walk ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Нәтиже" });
s.addText("Телефонда және серуенде", { placeholder: "title" });
s.addImage({ path: A("p_home.png"), x: 0.7, y: 1.4, w: 2.45, h: 2.45 * 1688 / 780, objectName: "phone-map", altText: "Телефондағы карта" });
s.addImage({ path: A("p_card.png"), x: 3.45, y: 1.4, w: 2.45, h: 2.45 * 1688 / 780, objectName: "phone-card", altText: "Телефондағы карточка" });
[["Серуен режимі", "«Ақтөбенің тарихи тұлғалары» маршруты — 8 аялдама"], ["Екі тіл", "интерфейс пен мәтіндер қазақша және орысша"], ["3D-турлар", "Нұр Ғасыр мешіті, Николай соборы және басқалар — visitaktobe.kz"]].forEach(([h, b], i) => {
  const y = 1.6 + i * 1.6;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.5, y, w: 6.2, h: 1.35, rectRadius: 0.12, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: "feature-card-" + i });
  s.addText(h, { x: 6.85, y: y + 0.15, w: 5.6, h: 0.45, fontSize: 20, bold: true, color: C.accent2, margin: 0, isTextBox: true });
  s.addText(b, { x: 6.85, y: y + 0.62, w: 5.6, h: 0.6, fontSize: 16, color: C.text1, margin: 0, isTextBox: true });
});
s.addNotes("Карта телефонда да, компьютерде де жұмыс істейді. Серуен режимінде «Ақтөбенің тарихи тұлғалары» маршруты бойынша сегіз аялдаманы аралауға болады. Интерфейс қазақша және орысша, ал кейбір нысандардың 3D-турлары бар.");

// ---------- 10. conclusion ----------
pres.addSection({ title: "Қорытынды" });
s = pres.addSlide({ masterName: "DARK", sectionTitle: "Қорытынды" });
s.addText("Қорытынды", { placeholder: "title" });
s.addText("тарихи жады — қаланың көшелері мен ескерткіштерінде", { placeholder: "body" });
["Ескерткіштер мен көше атаулары — қаланың тірі тарихы", "Ашық деректер мен технология тарихты бәріне қолжетімді етеді", "Картаны жаңа нысандармен, суреттермен және естеліктермен толықтыруға болады"].forEach((t, i) => {
  const y = 1.55 + i * 1.6;
  s.addShape(pres.shapes.OVAL, { x: 8.3, y: y + 0.1, w: 0.7, h: 0.7, fill: { color: C.accent1 }, line: { color: C.accent1 } });
  s.addText(String(i + 1), { x: 8.3, y: y + 0.1, w: 0.7, h: 0.7, fontSize: 20, bold: true, color: C.text2, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText(t, { x: 9.2, y, w: 3.6, h: 1.0, fontSize: 18, color: C.background1, valign: "middle", margin: 0, isTextBox: true });
});
s.addNotes("Қорытындылай келе, ескерткіштер мен көше атаулары — қаламыздың тірі тарихы. Ашық деректер мен технология бұл тарихты бәріне қолжетімді етеді. Картаны әрі қарай жаңа нысандармен, суреттермен және естеліктермен толықтыруға болады.");

// ---------- 11. link & thanks ----------
s = pres.addSlide({ masterName: "DARK", sectionTitle: "Қорытынды" });
s.addText("Картаны ашыңыз", { placeholder: "title" });
s.addText("shyngly29-bit.github.io/aktobe-map", { placeholder: "body", fontSize: 26, italic: false, bold: true });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 9.0, y: 1.4, w: 3.7, h: 3.7, rectRadius: 0.15, fill: { color: C.background1 }, line: { color: C.background1 }, objectName: "qr-frame" });
s.addImage({ path: A("qr.png"), x: 9.25, y: 1.65, w: 3.2, h: 3.2, objectName: "qr", altText: "Картаның QR-коды" });
s.addText("Назарларыңызға рақмет!", { x: 0.6, y: 5.3, w: 8, h: 0.7, fontFace: THEME.headFontFace, fontSize: 30, bold: true, color: C.background1, margin: 0, isTextBox: true });
s.addText("Деректер: OpenStreetMap (ODbL) · Wikimedia Commons · Википедия · visitaktobe.kz", { x: 0.6, y: 6.6, w: 12, h: 0.3, fontSize: 11, color: C.background2, margin: 0, isTextBox: true });
s.addNotes("Картаны телефоныңызбен QR-код арқылы немесе осы сілтеме бойынша ашуға болады. Назарларыңызға рақмет! Сұрақтарыңызға жауап беруге дайынмын.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
