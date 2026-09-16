"""Check every name the page renders has a matching asset key."""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tpl = open(os.path.join(ROOT, "src", "index.template.html"), encoding="utf8").read()
man = json.load(open(os.path.join(ROOT, "assets", "manifest.json"), encoding="utf8"))


def slug(s):
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", s.lower()))


# pull the AWARDS + LEADERS blocks straight out of the template
def block(name):
    i = tpl.index(f"const {name} = ")
    depth, j = 0, tpl.index("[", i)
    for k in range(j, len(tpl)):
        if tpl[k] == "[":
            depth += 1
        elif tpl[k] == "]":
            depth -= 1
            if depth == 0:
                return tpl[j:k + 1]
    raise ValueError(name)


awards = block("AWARDS")
codes = re.findall(r"code:'([a-z]+)'", awards)
groups = re.findall(r"people:\[(.*?)\]\}", awards, re.S)
assert len(codes) == len(groups) == 6, (len(codes), len(groups))

expected, total = [], 0
for code, g in zip(codes, groups):
    names = re.findall(r"\['([^']+)','([^']*)'\]", g)
    total += len(names)
    print(f"{code.upper():4s} {len(names):3d} recipients")
    for nm, _ in names:
        expected.append(f"{code}_{slug(nm)}")

leaders = re.findall(r"id:'([a-z0-9\-]+)', name:", block("LEADERS"))
expected += [f"leader_{i}" for i in leaders]
expected += [k for k in re.findall(r"\['(candid_[a-z0-9_]+)'", tpl)]
expected.append("candid_s11_1")

missing = [e for e in expected if e not in man]
unused = [k for k in man if k not in expected]

print(f"\nrecipients total : {total}  (expect 51)")
print(f"leaders          : {len(leaders)}  (expect 8)")
print(f"asset keys wanted: {len(expected)}")
print(f"MISSING          : {missing or 'none'}")
print(f"unused in bundle : {unused or 'none'}")
