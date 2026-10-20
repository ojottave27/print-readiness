# Demo: NonVerbalVennDiagram/040 rebuilt from meaning, with his 19 numbers.
import math, os, html

W, H = 480, 300
INK = "#231F20"
OUT = "out"
os.makedirs(OUT, exist_ok=True)

S = {"id": "S", "kind": "circle", "cx": 240, "cy": 100, "r": 78, "name": "Student"}
D = {"id": "D", "kind": "rect", "x0": 150, "y0": 72, "x1": 330, "y1": 138, "name": "Dancer"}
B = {"id": "B", "kind": "rect", "x0": 108, "y0": 118, "x1": 352, "y1": 184, "name": "Boys"}
T = {"id": "C", "kind": "tri", "p": [(240, 32), (170, 240), (310, 240)], "name": "Cricket player"}
SHAPES = [S, D, B, T]

def in_circle(s, x, y): return (x-s["cx"])**2 + (y-s["cy"])**2 <= s["r"]**2
def in_rect(s, x, y): return s["x0"]<=x<=s["x1"] and s["y0"]<=y<=s["y1"]
def _sg(p,q,r): return (p[0]-r[0])*(q[1]-r[1])-(q[0]-r[0])*(p[1]-r[1])
def in_tri(s, x, y):
    a,b,c = s["p"]
    d1,d2,d3 = _sg((x,y),a,b),_sg((x,y),b,c),_sg((x,y),c,a)
    return not (((d1<0)or(d2<0)or(d3<0)) and ((d1>0)or(d2>0)or(d3>0)))
CONTAINS = {"circle": in_circle, "rect": in_rect, "tri": in_tri}
def cell_of(x,y): return "".join(sorted(s["id"] for s in SHAPES if CONTAINS[s["kind"]](s,x,y)))

def seg_dist(p,a,b):
    ax,ay=a; bx,by=b; px,py=p
    dx,dy=bx-ax,by-ay; L=dx*dx+dy*dy
    t=0.0 if L==0 else max(0.0,min(1.0,((px-ax)*dx+(py-ay)*dy)/L))
    return math.hypot(px-(ax+t*dx), py-(ay+t*dy))
def boundary_dist(s,x,y):
    if s["kind"]=="circle": return abs(math.hypot(x-s["cx"],y-s["cy"])-s["r"])
    if s["kind"]=="rect": return min(x-s["x0"],s["x1"]-x,y-s["y0"],s["y1"]-y)
    a,b,c=s["p"]
    return min(seg_dist((x,y),a,b),seg_dist((x,y),b,c),seg_dist((x,y),c,a))
def clearance(x,y): return min(abs(boundary_dist(s,x,y)) for s in SHAPES)

# number, x, y  (positions chosen so each lands in its region with >=6px clearance)
NUM = [
    ("18", 296, 55), ("2", 240, 60),
    ("6", 156, 85), ("5", 180, 90), ("4", 240, 90), ("7", 300, 90),
    ("12", 156, 103), ("10", 160, 128), ("3", 180, 128), ("8", 240, 128), ("6", 300, 128), ("5", 322, 130),
    ("8", 170, 155), ("12", 138, 162), ("9", 336, 155),
    ("3", 210, 145), ("2", 270, 145),
    ("3", 220, 198), ("17", 256, 205),
]

errors = []
for txt,x,y in NUM:
    if clearance(x,y) < 6.0:
        errors.append("%s at (%d,%d): clearance %.1f" % (txt,x,y,clearance(x,y)))
for i in range(len(NUM)):
    for j in range(i+1, len(NUM)):
        _,x1,y1 = NUM[i]; _,x2,y2 = NUM[j]
        d = math.hypot(x1-x2, y1-y2)
        if d < 17.0:
            errors.append("%s/%s too close (%.1f)" % (NUM[i][0], NUM[j][0], d))

svg = []
svg.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
svg.append('<rect width="100%" height="100%" fill="white"/>')
svg.append('<g fill="none" stroke="%s" stroke-width="1">' % INK)
svg.append('<circle cx="%d" cy="%d" r="%d"/>' % (S["cx"],S["cy"],S["r"]))
svg.append('<rect x="%d" y="%d" width="%d" height="%d"/>' % (D["x0"],D["y0"],D["x1"]-D["x0"],D["y1"]-D["y0"]))
svg.append('<rect x="%d" y="%d" width="%d" height="%d"/>' % (B["x0"],B["y0"],B["x1"]-B["x0"],B["y1"]-B["y0"]))
svg.append('<polygon points="%s"/>' % " ".join("%d,%d" % p for p in T["p"]))
svg.append('</g>')
svg.append('<g font-family="Liberation Serif, Times New Roman, serif" font-size="13" fill="%s" text-anchor="middle">' % INK)
for txt,x,y in NUM:
    svg.append('<text x="%d" y="%d">%s</text>' % (x, y+5, txt))
svg.append('</g>')

# leader lines + labels, with open V arrowheads
svg.append('<g stroke="%s" stroke-width="1" fill="none">' % INK)
def vhead(x, y, direction):
    # small open V arrowhead at (x,y) pointing in direction (dx,dy normalized)
    dx, dy = direction
    L, A = 8, 0.5
    ax = x - L*(dx*math.cos(A) - dy*math.sin(A))
    ay = y - L*(dy*math.cos(A) + dx*math.sin(A))
    bx = x - L*(dx*math.cos(A) + dy*math.sin(A))
    by = y - L*(dy*math.cos(A) - dx*math.sin(A))
    return "M %.1f %.1f L %d %d L %.1f %.1f" % (ax,ay,x,y,bx,by)
# Student: arrow from text (upper right) pointing down-left to the circle ARC, above the Dancer rect
svg.append('<line x1="338" y1="58" x2="314" y2="67"/>')
svg.append('<path d="%s" fill="none"/>' % vhead(314,67,(-0.93,0.35)))
# Dancer: arrow from text (left) pointing right to D edge (150,100)
svg.append('<line x1="138" y1="100" x2="150" y2="100"/>')
svg.append('<path d="%s" fill="none"/>' % vhead(150,100,(1,0)))
# Boys: arrow from text (right) pointing left to B edge (352,150)
svg.append('<line x1="366" y1="150" x2="352" y2="150"/>')
svg.append('<path d="%s" fill="none"/>' % vhead(352,150,(-1,0)))
# Cricket: arrow from text (bottom right) to triangle base (300,240)
svg.append('<line x1="318" y1="262" x2="300" y2="240"/>')
svg.append('<path d="%s" fill="none"/>' % vhead(300,240,(-0.6,-0.8)))
svg.append('</g>')

svg.append('<g font-family="Liberation Serif, Times New Roman, serif" font-size="15" fill="%s">' % INK)
for name, lx, ly, anch in [(S["name"],344,63,"start"), (D["name"],132,105,"end"),
                            (B["name"],372,155,"start"), (T["name"],322,270,"start")]:
    svg.append('<text x="%d" y="%d" text-anchor="%s">%s</text>' % (lx,ly,anch,html.escape(name)))
svg.append('</g>')
svg.append('</svg>')

with open(os.path.join(OUT,"040.svg"),"w",encoding="utf-8") as f:
    f.write("\n".join(svg))

print("numbers:", len(NUM))
print("regions:")
for txt,x,y in NUM:
    print("  %-3s (%3d,%3d) -> %s" % (txt,x,y,cell_of(x,y) or "OUTSIDE"))
print("checks:", "PASS" if not errors else "FAIL")
for e in errors: print("  ", e)
print("svg ->", os.path.join(OUT,"040.svg"))
