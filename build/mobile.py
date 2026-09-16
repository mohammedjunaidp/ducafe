"""True mobile viewports: nest the page in a fixed-width iframe inside a big window."""
import io, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QA = os.path.join(ROOT, "qa")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PAGE = "_qa-assets.html"   # dist page but with on-disk assets

# build the page variant once (on-disk assets so headless decodes reliably)
import json, re
man = json.load(io.open(os.path.join(ROOT, "assets", "manifest.json"), encoding="utf8"))
paths = {k: "../assets/" + k + ".webp" for k in man}
page = io.open(os.path.join(ROOT, "dist", "du-cafe-3.0.html"), encoding="utf8").read()
page = re.sub(r"const ASSETS = \{.*?\};",
              "const ASSETS = " + json.dumps(paths, separators=(",", ":")) + ";",
              page, count=1, flags=re.S)
assert "../assets/leader_ravi.webp" in page
# deterministic: reveals on, ambient motion off (so colours are the settled ones)
page = page.replace("</head>", """<style>
  .rv{opacity:1 !important;translate:none !important}
  #steam,#confetti{display:none !important}
</style></head>""", 1)
io.open(os.path.join(QA, PAGE), "w", encoding="utf8", newline="\n").write(page)

SHOTS = [
    ("m01-door",   390, 844, "#door"),
    ("m02-menu",   390, 844, "#menu"),
    ("m03-table",  390, 1500, "#leader-nauman"),
    ("m07-ravi",   390, 1250, "#leader-ravi"),
    ("m04-board",  390, 1300, "#board"),
    ("m05-award",  390, 1400, "#award-eai"),
    ("m06-last",   390, 900, "#closing"),
    ("t01-table",  768, 1100, "#leader-ravi"),
    ("t02-award",  768, 1200, "#award-mad"),
]

for name, w, h, anchor in SHOTS:
    frame = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>html,body{{margin:0;background:#0a0807}}
iframe{{width:{w}px;height:{h}px;border:0;display:block}}</style></head>
<body><iframe src="{PAGE}{anchor}" scrolling="no"></iframe></body></html>"""
    fp = os.path.join(QA, f"_frame-{name}.html")
    io.open(fp, "w", encoding="utf8", newline="\n").write(frame)
    out = os.path.join(QA, f"{name}.png")
    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--run-all-compositor-stages-before-draw", "--disable-features=PaintHolding",
        "--virtual-time-budget=15000", f"--window-size={max(w,520)},{h}",
        f"--user-data-dir={os.path.join(QA, '.pm-' + name)}",
        f"--screenshot={out}", "file:///" + fp.replace("\\", "/"),
    ], capture_output=True)
    print(f"{name:12s} {w}x{h} {anchor:16s} {os.path.getsize(out)//1024 if os.path.exists(out) else 0:5d} KB")
