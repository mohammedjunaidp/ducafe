import io, sys
P = "src/index.template.html"
s = io.open(P, encoding="utf8").read()
done = []
def sub(old, new, label):
    global s
    if old not in s:
        print("  !! NOT FOUND:", label); sys.exit(1)
    s = s.replace(old, new, 1); done.append(label)

# roles confirmed by the user (the deck never stated these two)
sub("{ id:'ravi', name:'Ravi', role:'ADM Delivery',",
    "{ id:'ravi', name:'Ravi', role:'Engagement Delivery Lead',",
    "Ravi -> Engagement Delivery Lead")
sub("{ id:'srinivasan', name:'Srinivasan', role:'Delivery',",
    "{ id:'srinivasan', name:'Srinivasan', role:'Senior Project Manager',",
    "Srinivasan -> Senior Project Manager")

# Shalini and "Shalini V" are one person -> use Shalini V everywhere
sub("{ id:'shalini', name:'Shalini', role:'L3 / TT',",
    "{ id:'shalini', name:'Shalini V', role:'L3TT',",
    "Shalini -> Shalini V (L3TT)")

io.open(P, "w", encoding="utf8", newline="\n").write(s)
print("patched:", len(done))
for d in done: print("  ok", d)
