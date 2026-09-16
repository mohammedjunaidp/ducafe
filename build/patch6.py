"""Text-only pass: kill the 'table' framing and the literal-cafe labels.
No CSS values, no layout, no design changes -- copy and ids only."""
import io, sys
P = "src/index.template.html"
s = io.open(P, encoding="utf8").read()
done = []

def sub(old, new, label, n=1):
    global s
    if old not in s:
        print("  !! NOT FOUND:", label); sys.exit(1)
    s = s.replace(old, new, n); done.append(label)

# ── ids: #table-ravi -> #leader-ravi, #tables -> #leaders, #lastcall -> #closing
sub('<div id="leaders"></div>', '<div id="leaderList"></div>', "inner container renamed (frees up #leaders)")
sub("document.getElementById('leaders').innerHTML", "document.getElementById('leaderList').innerHTML", "JS container ref")
sub('<section id="tables">', '<section id="leaders">', "section id -> #leaders")
sub("/* ---------- 2 · THE TABLES ---------- */\n#tables{", "/* ---------- 2 · KNOW YOUR LEADER ---------- */\n#leaders{", "CSS id + comment")
sub("<!-- ═══════════ 2 · THE TABLES ═══════════ -->", "<!-- ═══════════ 2 · KNOW YOUR LEADER ═══════════ -->", "HTML comment")
sub('<article class="leader" id="table-${l.id}"', '<article class="leader" id="leader-${l.id}"', "per-leader id")
sub("['#table-ravi','Tables']", "['#leader-ravi','Leaders']", "rail target + label")
sub('<section id="lastcall" data-stop data-chapter="Last Call">',
    '<section id="closing" data-stop data-chapter="Over to you">', "closing section id + map label")
sub("/* ---------- 6 · LAST CALL ---------- */\n#lastcall{", "/* ---------- 6 · CLOSING ---------- */\n#closing{", "closing CSS id")
sub("#lastcall h2{", "#closing h2{", "closing h2")
sub("#lastcall .thanks{", "#closing .thanks{", "closing thanks")
sub("#lastcall .lead{", "#closing .lead{", "closing lead")
sub("<!-- ═══════════ 6 · LAST CALL ═══════════ -->", "<!-- ═══════════ 6 · CLOSING ═══════════ -->", "closing comment")
sub("go:'#lastcall' }", "go:'#closing' }", "menu link to closing")
sub("['#lastcall','Last call']", "['#closing','Close']", "rail closing entry")

# ── the actual offender: nobody is a numbered table
sub("""        <span class="tag mono">Table ${String(i+1).padStart(2,'0')}${l.role ? ' · ' + esc(l.role) : ''}</span>""",
    """        <span class="tag mono">Know your leader${l.role ? ' · ' + esc(l.role) : ''}</span>""",
    "per-leader tag uses the deck's own phrase + role")

sub("""      <h2 class="rv" data-d="1">The tables.</h2>
      <p class="lead rv" data-d="2">Eight people who normally show up as a name on a status call. Pull up a chair — they answered the questions nobody puts in a status call.</p>""",
    """      <h2 class="rv" data-d="1">You know the names.<br>Now meet the people.</h2>
      <p class="lead rv" data-d="2">Eight leaders answered the questions a status call never asks — what drives them, what they'd rather be doing on a Saturday, and the one thing nobody knew.</p>""",
    "leaders chapter reads as a story, not a seating plan")

# ── drop the literal-cafe furniture from the copy
sub("""<p class="open-sign mono rv in"><span class="bulb" aria-hidden="true"></span>Open · edition three</p>""",
    """<p class="open-sign mono rv in"><span class="bulb" aria-hidden="true"></span>Edition three</p>""",
    "hero badge no longer a café 'Open' sign")
sub("""      Push the door
      <svg""", """      Start here
      <svg""", "scroll cue")
sub("""      <p class="eyebrow mono rv">Today's menu</p>""",
    """      <p class="eyebrow mono rv">What's inside</p>""", "menu eyebrow")
sub("""      <p class="lead rv" data-d="2">Every du CAFÉ runs on the same four things. This one is no different — it's just no longer trapped in a slide deck.</p>""",
    """      <p class="lead rv" data-d="2">Every du CAFÉ comes back to the same four things. Here's where each one lives in the story.</p>""",
    "menu lead loses the dig at the deck")
sub("""      <p class="lead rv" data-d="2">The photos that never make it into a governance pack. Pinned to the wall by the counter, where they belong.</p>""",
    """      <p class="lead rv" data-d="2">The same eight people, off duty. No agenda and no slides — just the pictures they were willing to share.</p>""",
    "candid lead loses the dig at governance packs")
sub("""      <p class="lead rv" data-d="2">Six frames. <strong class="tnum">51</strong> names. Every one of them earned a spot on the wall this cycle.</p>""",
    """      <p class="lead rv" data-d="2">Six awards. <strong class="tnum">51</strong> names. Every one of them earned their place this cycle.</p>""",
    "wall lead")

# ── chapter-map / rail labels that named café rooms
sub('<section id="door" data-stop data-chapter="The Door">',
    '<section id="door" data-stop data-chapter="Opening">', "door map label")
sub('<section id="menu" data-stop data-chapter="The Menu">',
    '<section id="menu" data-stop data-chapter="What\'s inside">', "menu map label")
sub('<section id="board" data-stop data-chapter="Noticeboard">',
    '<section id="board" data-stop data-chapter="The candid side">', "candid map label")
sub("['#door','Door'],['#menu','Menu']", "['#door','Start'],['#menu','Inside']", "rail labels")
sub("['#board','Candids'],['#fun','Fun'],['#award-mad','Wall']",
    "['#board','Candids'],['#fun','Fun'],['#award-mad','Awards']", "rail awards label")
sub("/* ---------- 4 · THE BACK ROOM (fun) ---------- */", "/* ---------- 4 · FUN ---------- */", "fun CSS comment")
sub("<!-- ═══════════ 4 · THE BACK ROOM ═══════════ -->", "<!-- ═══════════ 4 · FUN ═══════════ -->", "fun HTML comment")
sub("/* ---------- 3 · THE NOTICEBOARD ---------- */", "/* ---------- 3 · THE CANDID SIDE ---------- */", "candid CSS comment")
sub("<!-- ═══════════ 3 · THE NOTICEBOARD ═══════════ -->", "<!-- ═══════════ 3 · THE CANDID SIDE ═══════════ -->", "candid HTML comment")
sub("/* ---------- 0 · THE DOOR ---------- */", "/* ---------- 0 · OPENING ---------- */", "door CSS comment")
sub("<!-- ═══════════ 0 · THE DOOR ═══════════ -->", "<!-- ═══════════ 0 · OPENING ═══════════ -->", "door HTML comment")
sub("/* ---------- 1 · TODAY'S MENU ---------- */", "/* ---------- 1 · WHAT'S INSIDE ---------- */", "menu CSS comment")
sub("<!-- ═══════════ 1 · TODAY'S MENU ═══════════ -->", "<!-- ═══════════ 1 · WHAT'S INSIDE ═══════════ -->", "menu HTML comment")

assert "Table ${String" not in s and "The tables." not in s
assert "#table-" not in s and "id=\"tables\"" not in s and "#lastcall" not in s
io.open(P, "w", encoding="utf8", newline="\n").write(s)
print(f"patched {len(done)} items")
for d in done: print("  ok", d)
