import io, sys
P = "src/index.template.html"
s = io.open(P, encoding="utf8").read()
done = []

def sub(old, new, label):
    global s
    if old not in s:
        print("  !! NOT FOUND:", label); sys.exit(1)
    s = s.replace(old, new, 1); done.append(label)

# 1. THE BUG: .shot was an inline <span> containing a display:block <img>,
#    so aspect-ratio / height:100% were ignored and images rendered erratically.
sub(".polaroid .shot{position:relative;aspect-ratio:4/5;overflow:hidden;border-radius:2px;background:#ddd4c6}",
    ".polaroid .shot{display:block;position:relative;aspect-ratio:4/5;overflow:hidden;border-radius:2px;background:#ddd4c6}",
    ".shot is block-level (fixes blank polaroids)")

# 2. menu row had 4 children but only 3 columns -> the CTA wrapped onto row 2
sub("  display:grid;grid-template-columns:auto 1fr auto;align-items:baseline;",
    "  display:grid;grid-template-columns:auto minmax(0,1fr) minmax(var(--s6),1fr) auto;align-items:baseline;",
    "menu row has 4 grid columns")
sub(".menu-row .dots{border-bottom:1px dotted var(--line-2);align-self:center;height:1px;min-width:var(--s5)}",
    ".menu-row .dots{border-bottom:1px dotted rgba(246,240,230,.26);align-self:center;height:1px;min-width:var(--s5)}",
    "leader dots more visible")
sub(".menu-row .go{display:inline-flex;align-items:center;gap:.4rem;",
    ".menu-row .go{display:inline-flex;align-items:center;gap:.4rem;white-space:nowrap;justify-self:end;",
    "menu CTA pinned right, no wrap")

# 3. MAD's middle letter has no expansion -> it rendered as "A / A"
sub("""          ${a.acro.map(([ch,w]) => `<li class="rv"><span class="ch" aria-hidden="true">${ch}</span><span class="word">${ch}${esc(w)}</span></li>`).join('')}""",
    """          ${a.acro.map(([ch,w]) => `<li class="rv"><span class="ch" aria-hidden="true">${ch}</span>${w ? `<span class="word">${ch}${esc(w)}</span>` : ''}</li>`).join('')}""",
    "acronym omits the word when there is no expansion")

# 4. amber over espresso + a teal layer on top of it read as olive, not lamplight
sub("""    radial-gradient(ellipse at 50% 0%,rgba(233,169,60,.30),rgba(233,169,60,.10) 38%,transparent 68%),
    radial-gradient(ellipse at 50% 0%,rgba(24,192,172,.14),transparent 55%);""",
    """    radial-gradient(ellipse at 50% 0%,rgba(255,188,96,.34),rgba(238,146,58,.13) 40%,transparent 70%),
    radial-gradient(ellipse at 12% 92%,rgba(24,192,172,.11),transparent 56%);""",
    "hero light reads as warm lamplight")

# 5. long polaroid captions collided with the frame number
sub("""  display:flex;justify-content:space-between;align-items:center;gap:var(--s3);
  padding:.7rem .2rem .8rem;color:#6d6154;""",
    """  display:flex;justify-content:space-between;align-items:baseline;gap:var(--s3);
  padding:.7rem .2rem .8rem;color:#6d6154;text-align:left;""",
    "polaroid caption alignment")
sub("""  <span class="cap"><span>${esc(cap)}</span><span class="tnum">no. ${String(i+1).padStart(2,'0')}</span></span>""",
    """  <span class="cap"><span>${esc(cap)}</span><span class="tnum" style="flex:none">no. ${String(i+1).padStart(2,'0')}</span></span>""",
    "frame number never shrinks")
sub("""['candid_s4_3','Captain for the afternoon'],""", """['candid_s4_3','Captain for a day'],""",
    "shortened a caption that wrapped")

io.open(P, "w", encoding="utf8", newline="\n").write(s)
print("patched:", len(done))
for d in done: print("  ok", d)
