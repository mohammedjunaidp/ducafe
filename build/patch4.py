import io, sys
P = "src/index.template.html"
s = io.open(P, encoding="utf8").read()
done = []
def sub(old, new, label):
    global s
    if old not in s:
        print("  !! NOT FOUND:", label); sys.exit(1)
    s = s.replace(old, new, 1); done.append(label)

# e.target can be document/window (programmatic dispatch, some AT); .matches would throw
# and take the whole shortcut handler down with it.
sub("""  if (e.target.matches('input, textarea')) { if (e.key === 'Escape') e.target.blur(); return; }""",
    """  const t = e.target;
  if (t instanceof Element && t.matches('input, textarea, [contenteditable]')) {
    if (e.key === 'Escape') t.blur();
    return;
  }""",
    "keydown guard no longer throws on non-Element targets")

# "1 of 51 name match" -> "1 of 51 names matches"
sub("""  status.textContent = !v ? ''
    : hits ? `${hits} of ${frames.length} ${hits === 1 ? 'name' : 'names'} match “${q.value.trim()}”.`
           : `No name on the wall matches “${q.value.trim()}”.`;""",
    """  status.textContent = !v ? ''
    : hits ? `${hits} of ${frames.length} names match “${q.value.trim()}” — ` +
             `${hits === 1 ? 'here it is' : 'here they are'}.`
           : `No name on the wall matches “${q.value.trim()}”.`;""",
    "search status reads correctly for 1 and many")

io.open(P, "w", encoding="utf8", newline="\n").write(s)
print("patched:", len(done))
for d in done: print("  ok", d)
