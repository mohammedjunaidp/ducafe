import io, sys
P = "src/index.template.html"
s = io.open(P, encoding="utf8").read()
done = []

def sub(old, new, label, n=1):
    global s
    if old not in s:
        print("  !! NOT FOUND:", label); sys.exit(1)
    s = s.replace(old, new, n); done.append(label)

# 1. mobile: the 4-column menu row squeezed titles to one word per line
sub("""/* ---------- 2 · THE TABLES ---------- */""",
"""@media (max-width:700px){
  .menu-row{grid-template-columns:auto minmax(0,1fr);row-gap:var(--s3);padding:var(--s5) var(--s2)}
  .menu-row .dots{display:none}
  .menu-row .t,.menu-row .go{grid-column:2}
  .menu-row .go{justify-self:start}
}

/* ---------- 2 · THE TABLES ---------- */""",
    "menu row stacks on mobile")

# 2. centred eyebrows: give the big type room, drop the one-sided rule
sub(""".chapter-head .eyebrow::after{content:"";height:1px;flex:1;background:linear-gradient(90deg,var(--brass-deep),transparent)}""",
    """.chapter-head .eyebrow::after{content:"";height:1px;flex:1;background:linear-gradient(90deg,var(--brass-deep),transparent)}
.eyebrow.center{justify-content:center;color:var(--brass);margin-bottom:var(--s6)}
.eyebrow.center::after{display:none}""",
    "centred eyebrow variant")
sub("""    <p class="eyebrow mono rv" style="justify-content:center;color:var(--brass)">Fun</p>""",
    """    <p class="eyebrow mono center rv">Fun</p>""", "fun eyebrow spacing")
sub("""    <p class="eyebrow mono rv" style="justify-content:center;color:var(--brass)">Over to you</p>""",
    """    <p class="eyebrow mono center rv">Over to you</p>""", "last-call eyebrow spacing")

# 3. six photos read better as 3+3 than 4+2
sub(""".pins{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:clamp(1.2rem,3vw,2.4rem)}""",
    """.pins{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(1.2rem,3vw,2.4rem)}
@media (max-width:900px){.pins{grid-template-columns:repeat(2,1fr)}}
@media (max-width:560px){.pins{grid-template-columns:1fr}}""",
    "noticeboard is a balanced 3x2")

io.open(P, "w", encoding="utf8", newline="\n").write(s)
print("patched:", len(done))
for d in done: print("  ok", d)
