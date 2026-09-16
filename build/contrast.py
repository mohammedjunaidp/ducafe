"""WCAG contrast audit for the palette actually used in the page."""

def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def L(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

def ratio(a, b):
    la, lb = L(a), L(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def mix(fg, bg, pct):
    """color-mix(in srgb, fg pct%, bg) approximation in sRGB."""
    f = [int(fg.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
    b = [int(bg.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(f[i]*pct + b[i]*(1-pct)):02x}" for i in range(3))

INK, INK2, INK3 = "#17120f", "#1f1814", "#29201a"
CREAM, DIM, MUTED = "#f6f0e6", "#cabfb1", "#9d9285"
BRASS, TERRA, DU = "#e9a93c", "#d9694f", "#18c0ac"
AWARDS = {"MAD": "#ffc857", "LBS": "#6ec8ff", "EAI": "#ff6fa5",
          "DSP": "#3ad9b8", "ICM": "#ff8a5b", "OMP": "#b69cff"}
PAPER, PAPER_INK = "#f3ece1", "#6d6154"

checks = [
    ("body text  cream / ink",          CREAM, INK,  4.5),
    ("secondary  dim / ink",            DIM,   INK,  4.5),
    ("tertiary   muted / ink",          MUTED, INK,  4.5),
    ("muted / card ink-2",              MUTED, INK2, 4.5),
    ("muted / card ink-3",              MUTED, INK3, 4.5),
    ("cream / card ink-3",              CREAM, INK3, 4.5),
    ("brass eyebrow / ink",             BRASS, INK,  4.5),
    ("terracotta label / ink-2",        TERRA, INK2, 4.5),
    ("du teal / ink",                   DU,    INK,  4.5),
    ("polaroid caption ink / paper",    PAPER_INK, PAPER, 4.5),
]
for code, c in AWARDS.items():
    checks.append((f"{code} accent text / ink", c, INK, 4.5))
    checks.append((f"{code} tile: ink text / 92% accent", INK, mix(c, "#000000", 0.92), 4.5))

print(f"{'pair':40s} {'ratio':>7s}  {'need':>5s}  verdict")
print("-" * 70)
fails = 0
for label, fg, bg, need in checks:
    r = ratio(fg, bg)
    ok = r >= need
    fails += not ok
    print(f"{label:40s} {r:7.2f}  {need:5.1f}  {'PASS' if ok else '** FAIL **'}")
print("-" * 70)
print(f"{len(checks)} pairs checked, {fails} failing AA")
