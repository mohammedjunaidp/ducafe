import io, sys
P = "src/index.template.html"
s = io.open(P, encoding="utf8").read()
def sub(old, new, label):
    global s
    if old not in s:
        print("  !! NOT FOUND:", label); sys.exit(1)
    s = s.replace(old, new, 1); print("  ok", label)

# label carries the deck's phrase; the role gets its own line under the name
sub("""        <span class="tag mono">Know your leader${l.role ? ' · ' + esc(l.role) : ''}</span>""",
    """        <span class="tag mono">Know your leader</span>""",
    "label is just the deck's phrase")

sub("""        <h3 class="rv" data-d="1">${esc(l.name)}</h3>
        <ul class="traits rv" data-d="2">""",
    """        <h3 class="rv" data-d="1">${esc(l.name)}</h3>
        ${l.role ? `<p class="role rv" data-d="1">${esc(l.role)}</p>` : ''}
        <ul class="traits rv" data-d="2">""",
    "role sits on its own line under the name")

sub(""".leader-id .tag{color:var(--brass);margin-bottom:var(--s4);display:block;line-height:1.6;max-width:30ch}""",
    """.leader-id .tag{color:var(--brass);margin-bottom:var(--s4);display:block;line-height:1.6}
.leader-id .role{
  font-family:var(--serif);font-style:italic;color:var(--cream-dim);
  font-size:calc(1.0625rem * var(--present));line-height:1.35;margin-bottom:var(--s4);
}""",
    "role line styling")

# the h3 had the only bottom margin; the role line now owns that gap
sub(""".leader-id h3{font-size:calc(var(--t-name) * var(--present));margin-bottom:var(--s4)}""",
    """.leader-id h3{font-size:calc(var(--t-name) * var(--present));margin-bottom:var(--s2)}""",
    "tightened name/role spacing")

io.open(P, "w", encoding="utf8", newline="\n").write(s)
