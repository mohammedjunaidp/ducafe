import io, os, re, sys

P = "src/index.template.html"
s = io.open(P, encoding="utf8").read()
orig = s
fixes = []

def sub(old, new, label, count=1):
    global s
    if old not in s:
        print("  !! NOT FOUND:", label); sys.exit(1)
    s = s.replace(old, new, count)
    fixes.append(label)

# ---- 1. scroll tracking: offsetTop is relative to offsetParent, and .leader /
#         .award live inside position:relative sections -> wrong numbers.
sub(
"""  const probe = scrollY + innerHeight * 0.34;
  let idx = 0;
  for (let i = 0; i < stops.length; i++) if (stops[i].offsetTop <= probe) idx = i;""",
"""  const probe = scrollY + innerHeight * 0.34;
  let idx = 0;
  for (let i = 0; i < stops.length; i++) if (tops[i] <= probe) idx = i;""",
"onScroll uses measured document tops")

sub(
"""let cur = 0;
const prog = document.getElementById('progress');""",
"""let cur = 0, tops = [];
const measure = () => { tops = stops.map(s => s.getBoundingClientRect().top + scrollY); };
const prog = document.getElementById('progress');""",
"added measure() for absolute stop offsets")

sub(
"""}, { passive:true });
onScroll();""",
"""}, { passive:true });
addEventListener('resize', () => { measure(); onScroll(); }, { passive:true });
addEventListener('load', () => { measure(); onScroll(); });
measure();
onScroll();""",
"re-measure on resize/load")

# ---- 2. rail highlight: simplify, and guard the -1 findIndex case
sub(
"""    const id = '#' + stops[idx].id;
    let best = 0;
    CHAPTERS.forEach(([h], i) => { if (stops.findIndex(s => '#' + s.id === h) <= idx) best = i; });
    if (CHAPTERS.some(([h]) => h === id)) best = CHAPTERS.findIndex(([h]) => h === id);
    railBtns.forEach((b, i) => b.setAttribute('aria-current', String(i === best)));""",
"""    let best = 0;
    CHAPTERS.forEach(([h], i) => { const k = chapterStop[i]; if (k >= 0 && k <= idx) best = i; });
    railBtns.forEach((b, i) => b.setAttribute('aria-current', String(i === best)));""",
"rail highlight guarded against missing stops")

sub(
"""const railBtns = [...rail.querySelectorAll('button')];""",
"""const railBtns = [...rail.querySelectorAll('button')];
const chapterStop = CHAPTERS.map(([h]) => stops.findIndex(s => '#' + s.id === h));""",
"precomputed chapter->stop index")

# ---- 3. invalid HTML: <figcaption> was nested inside <button> inside <figure>
sub(
"""  <figure style="margin:0">
    <button class="polaroid rv" data-d="${i%4}" data-lb="${k}" data-cap="${esc(cap)}"
            style="--tilt:${[-2.4,1.8,-1.2,2.6,-2,1.4][i]}deg" type="button"
            aria-label="Enlarge photo: ${esc(cap)}">
      <span class="pin" aria-hidden="true"></span>
      <span class="shot"><img data-src="${k}" alt="Candid team photo — ${esc(cap)}" width="600" height="750" decoding="async"></span>
      <figcaption><span>${esc(cap)}</span><span class="tnum">no. ${String(i+1).padStart(2,'0')}</span></figcaption>
    </button>
  </figure>`).join('');""",
"""  <button class="polaroid rv" data-d="${i%4}" data-lb="${k}" data-cap="${esc(cap)}"
          style="--tilt:${[-2.4,1.8,-1.2,2.6,-2,1.4][i]}deg" type="button"
          aria-label="Enlarge photo: ${esc(cap)}">
    <span class="pin" aria-hidden="true"></span>
    <span class="shot"><img data-src="${k}" alt="Candid team photo — ${esc(cap)}" width="600" height="750" decoding="async"></span>
    <span class="cap"><span>${esc(cap)}</span><span class="tnum">no. ${String(i+1).padStart(2,'0')}</span></span>
  </button>`).join('');""",
"polaroid markup is now valid HTML")

sub(".polaroid figcaption{", ".polaroid .cap{", "polaroid caption selector")

# ---- 4. focus containment for the two overlays
sub(
"""const map = document.getElementById('map');
let lastFocus = null;""",
"""const map = document.getElementById('map');
const pageMain = document.querySelector('main');
const setInert = on => { pageMain.inert = on; rail.inert = on; };
let lastFocus = null;""",
"added setInert helper")

sub(
"""const openMap = () => {
  lastFocus = document.activeElement;
  map.setAttribute('open','');
  map.querySelector('button')?.focus();
};
const closeMap = () => { map.removeAttribute('open'); lastFocus?.focus(); };""",
"""const openMap = () => {
  lastFocus = document.activeElement;
  map.setAttribute('open','');
  setInert(true);
  map.querySelector('button')?.focus();
};
const closeMap = () => { map.removeAttribute('open'); setInert(false); lastFocus?.focus(); };""",
"map traps focus")

sub(
"""  lb.setAttribute('open','');
  lbClose.focus();
});
const closeLb = () => { lb.removeAttribute('open'); lbImg.src = ''; lbLast?.focus(); };""",
"""  lb.setAttribute('open','');
  setInert(true);
  lbClose.focus();
});
const closeLb = () => {
  lb.removeAttribute('open'); lbImg.src = '';
  setInert(false); lbLast?.focus();
};""",
"lightbox traps focus")

# ---- 5. don't yank the page around on the first keystroke
sub(
"""  if (v && first) first.scrollIntoView({ behavior: reduce.matches ? 'auto' : 'smooth', block:'center' });""",
"""  measure();
  if (v.length >= 2 && first) first.scrollIntoView({ behavior: reduce.matches ? 'auto' : 'smooth', block:'center' });""",
"search scrolls only from 2 chars, and re-measures stops")

# ---- 6. marquee halves must be identical for a seamless -50% loop
sub(
"""document.getElementById('credits').innerHTML =
  [0,1].map(() => uniqNames.map(n => `<span>${esc(n)}</span>`).join('<span>·</span>')).join('<span>·</span>');""",
"""const creditSeg = uniqNames.map(n => `<span>${esc(n)}</span><span aria-hidden="true">·</span>`).join('');
document.getElementById('credits').innerHTML = creditSeg + creditSeg;""",
"credits marquee loops seamlessly")

# ---- 7. real fallback if a photo key is ever missing (instead of a dead class)
sub(
""".frame .pic img{width:100%;height:100%;object-fit:cover}""",
""".frame .pic img{width:100%;height:100%;object-fit:cover}
.no-img{background:
  radial-gradient(circle at 50% 38%,var(--ink-4),var(--ink-3)) !important}
.no-img::before{content:"";position:absolute;inset:0;border-radius:inherit;
  background:linear-gradient(140deg,rgba(246,240,230,.06),transparent 60%)}""",
"missing-photo fallback is now styled")

# ---- 8. leader role is optional (don't print a dangling separator)
sub(
"""        <span class="tag mono">Table ${String(i+1).padStart(2,'0')} · ${esc(l.role)}</span>""",
"""        <span class="tag mono">Table ${String(i+1).padStart(2,'0')}${l.role ? ' · ' + esc(l.role) : ''}</span>""",
"leader role label is optional")

io.open(P, "w", encoding="utf8", newline="\n").write(s)
print(f"patched {len(fixes)} items ({len(orig)} -> {len(s)} bytes):")
for f in fixes:
    print("  ok", f)
