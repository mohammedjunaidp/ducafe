"""Turn the raw slide extractions into web-ready, face-centred WebP assets.

Reads   : C:\\Users\\2457903\\Downloads\\du_cafe_people
Writes  : du-cafe-3/assets/*.webp  +  assets/manifest.json
"""
import base64
import json
import os
import re

import cv2
import numpy as np
from PIL import Image

SRC = r"C:\Users\2457903\Downloads\du_cafe_people"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def detect_face(pil):
    """Biggest frontal face as (cx, cy, size) in pixels, or None."""
    arr = np.array(pil.convert("RGB"))
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    gray = cv2.equalizeHist(gray)
    h, w = gray.shape
    scale = 640 / max(h, w) if max(h, w) > 640 else 1.0
    if scale != 1.0:
        gray = cv2.resize(gray, (int(w * scale), int(h * scale)))
    faces = CASCADE.detectMultiScale(gray, 1.08, 6, minSize=(28, 28))
    if len(faces) == 0:
        return None
    x, y, fw, fh = max(faces, key=lambda f: f[2] * f[3])
    return (x + fw / 2) / scale, (y + fh / 2) / scale, fh / scale


def square_crop(pil, head_frac, fallback_y=0.30):
    """Square crop. If a face is found, size the box so the head height is
    `head_frac` of the frame and centre it slightly above middle."""
    W, H = pil.size
    face = detect_face(pil)
    if face:
        cx, cy, fh = face
        side = min(max(fh / head_frac, 64), min(W, H) * 3)
        cy -= side * 0.06                      # leave a little headroom
    else:
        side = min(W, H)
        cx, cy = W / 2, H * fallback_y + side / 2
    side = min(side, min(W, H))
    left = max(0, min(W - side, cx - side / 2))
    top = max(0, min(H - side, cy - side / 2))
    return pil.crop((int(left), int(top), int(left + side), int(top + side))), bool(face)


def save_webp(pil, name, size, quality, square=False):
    if square:
        pil = pil.resize((size, size), Image.LANCZOS)
    else:
        pil.thumbnail((size, size), Image.LANCZOS)
    path = os.path.join(OUT, name + ".webp")
    pil.save(path, "WEBP", quality=quality, method=6)
    return path


manifest, stats = {}, {"faces": 0, "nofaces": []}

for fn in sorted(os.listdir(SRC)):
    if fn.startswith("_") or not re.search(r"\.(jpe?g|png)$", fn, re.I):
        continue
    stem = os.path.splitext(fn)[0]
    src = Image.open(os.path.join(SRC, fn))
    if src.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", src.size, (28, 22, 19))
        bg.paste(src.convert("RGBA"), mask=src.convert("RGBA").split()[-1])
        src = bg
    else:
        src = src.convert("RGB")

    if stem.startswith("leader_"):
        img, found = square_crop(src, head_frac=0.40)
        path = save_webp(img, stem, 560, 82, square=True)
    elif stem.startswith("candid_s11"):
        path = save_webp(src, stem, 1700, 70)
        found = True
    elif stem.startswith("candid_"):
        path = save_webp(src, stem, 1000, 74)
        found = True
    else:                                        # 51 awardee avatars
        img, found = square_crop(src, head_frac=0.52)
        path = save_webp(img, stem, 300, 80, square=True)

    if stem.startswith(("leader_",)) or not stem.startswith("candid_"):
        if found:
            stats["faces"] += 1
        else:
            stats["nofaces"].append(stem)

    with open(path, "rb") as f:
        manifest[stem] = "data:image/webp;base64," + base64.b64encode(f.read()).decode()
    print(f"{stem:34s} {os.path.getsize(path)//1024:4d} KB  face={'Y' if found else 'n'}")

with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf8") as f:
    json.dump(manifest, f)

total = sum(len(v) for v in manifest.values())
print(f"\n{len(manifest)} assets | faces found {stats['faces']} | "
      f"no face: {stats['nofaces']}")
print(f"base64 payload: {total/1024/1024:.2f} MB")
