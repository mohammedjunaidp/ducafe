"""Render each chapter in isolation so headless Chrome never has to scroll."""
import io, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "dist", "du-cafe-3.0.html")
QA = os.path.join(ROOT, "qa")
os.makedirs(QA, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

base = io.open(SRC, encoding="utf8").read()

# For QA, swap the inlined base64 for real file:// URLs. Headless Chrome decodes
# on-disk WebP reliably; giant data URIs race the screenshot.
import json, re
_man = json.load(io.open(os.path.join(ROOT, "assets", "manifest.json"), encoding="utf8"))
_paths = {k: "../assets/" + k + ".webp" for k in _man}
base = re.sub(r"const ASSETS = \{.*?\};",
              "const ASSETS = " + json.dumps(_paths, separators=(",", ":")) + ";",
              base, count=1, flags=re.S)
assert "../assets/leader_ravi.webp" in base, "asset swap failed"

# keep = css selector of the ONE thing to show; everything else in <main> is hidden
SHOTS = [
    ("01-door",      "#door",               "1440,900"),
    ("02-menu",      "#menu",               "1440,1000"),
    ("02b-leadhead", "#leaders",             "1440,620"),
    ("03-table",     "#leader-ravi",         "1440,1150"),
    ("04-table-sh",  "#leader-shalini",      "1440,1150"),
    ("05-board",     "#board",              "1440,1500"),
    ("06-fun",       "#fun",                "1440,700"),
    ("07-award-mad", "#award-mad",           "1440,1150"),
    ("08-award-omp", "#award-omp",           "1440,900"),
    ("09-lastcall",  "#closing",           "1440,1000"),
    ("10-m-menu",    "#menu",               "390,900"),
    ("11-m-table",   "#leader-nauman",       "390,1400"),
    ("12-m-award",   "#award-eai",           "390,1500"),
    ("13-m-board",   "#board",              "390,1400"),
]

CSS = """
<style id="qa">
  /* hide every chapter, then re-show just the target (higher specificity wins) */
  main > section, #leaderList > .leader, #awards > .award {{ display:none !important }}
  main > {sel}, #leaderList > {sel}, #awards > {sel} {{ display:block !important }}
  #leaders:has({sel}), #wall:has({sel}) {{ display:block !important }}
  #leaders:has({sel}) > .wrap, #wall:has({sel}) > .wrap {{ display:none !important }}
  /* deterministic: reveals on, ambient motion off */
  .rv {{ opacity:1 !important; translate:none !important }}
  #steam, #confetti, #rail, #progress {{ display:none !important }}
  main > section {{ padding-top:2.5rem !important }}
</style>
"""

only = sys.argv[1] if len(sys.argv) > 1 else None
for name, sel, win in SHOTS:
    if only and only not in name:
        continue
    page = base.replace("</head>", CSS.format(sel=sel) + "</head>")
    p = os.path.join(QA, f"_{name}.html")
    io.open(p, "w", encoding="utf8", newline="\n").write(page)
    out = os.path.join(QA, f"{name}.png")
    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        # without these, base64 images are still decoding when the shot is taken
        "--run-all-compositor-stages-before-draw",
        "--disable-features=PaintHolding",
        "--virtual-time-budget=15000", f"--window-size={win}",
        f"--user-data-dir={os.path.join(QA, '.prof-' + name)}",
        f"--screenshot={out}", "file:///" + p.replace("\\", "/"),
    ], capture_output=True)
    kb = os.path.getsize(out) // 1024 if os.path.exists(out) else 0
    print(f"{name:14s} {sel:18s} {win:10s} {kb:5d} KB")
