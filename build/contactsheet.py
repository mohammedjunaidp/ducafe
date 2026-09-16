import os, glob
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets")

def sheet(files, cols, cell, out, label=True):
    rows = (len(files) + cols - 1) // cols
    pad, lab = 6, (16 if label else 0)
    W = cols * (cell + pad) + pad
    H = rows * (cell + pad + lab) + pad
    canvas = Image.new("RGB", (W, H), (20, 16, 14))
    d = ImageDraw.Draw(canvas)
    for i, f in enumerate(files):
        r, c = divmod(i, cols)
        x = pad + c * (cell + pad)
        y = pad + r * (cell + pad + lab)
        im = Image.open(f).convert("RGB")
        im.thumbnail((cell, cell), Image.LANCZOS)
        canvas.paste(im, (x + (cell - im.width) // 2, y))
        if label:
            d.text((x + 2, y + cell + 2),
                   os.path.basename(f).replace(".webp", "")[:26],
                   fill=(210, 200, 190))
    canvas.save(out)
    print(out, canvas.size)

leaders = sorted(glob.glob(os.path.join(A, "leader_*.webp")))
sheet(leaders, 4, 190, os.path.join(A, "_sheet_leaders.png"))

avatars = sorted(
    f for f in glob.glob(os.path.join(A, "*.webp"))
    if not os.path.basename(f).startswith(("leader_", "candid_", "_sheet"))
)
sheet(avatars, 9, 118, os.path.join(A, "_sheet_avatars.png"))
print("avatars:", len(avatars))
