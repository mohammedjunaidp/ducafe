"""Inline the WebP assets into the template -> one self-contained HTML file."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "src", "index.template.html")
MAN = os.path.join(ROOT, "assets", "manifest.json")
DIST = os.path.join(ROOT, "dist")
os.makedirs(DIST, exist_ok=True)
OUT = os.path.join(DIST, "du-cafe-3.0.html")

html = open(TPL, encoding="utf8").read()
manifest = json.load(open(MAN, encoding="utf8"))

# drop the two flat background images that aren't photos
for junk in ("candid_s11_0", "candid_s4_1"):
    manifest.pop(junk, None)

# --- verify every key the template asks for actually exists -------------
wanted = set(re.findall(r'data-src="([a-z0-9_\-]+)"', html))
wanted |= set(re.findall(r"data-src=\"\$\{a\.code\}_\$\{slug\(nm\)\}\"", html)) and set()
missing = sorted(w for w in wanted if w not in manifest)
if missing:
    print("!! template references missing assets:", missing)

payload = json.dumps(manifest, separators=(",", ":"))
html = re.sub(r"/\*__ASSETS__\*/.*?/\*__END__\*/", lambda m: payload, html, flags=re.S)

with open(OUT, "w", encoding="utf8") as f:
    f.write(html)

print(f"assets inlined : {len(manifest)}")
print(f"output         : {OUT}")
print(f"size           : {os.path.getsize(OUT)/1024/1024:.2f} MB")
