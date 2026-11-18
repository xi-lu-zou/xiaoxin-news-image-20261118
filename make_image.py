#!/usr/bin/env python3
"""Generate entry.png: the world news of Wednesday 18 November 2026 in one image.
Deterministic, no network, no assets — everything is drawn with PIL.
Canvas 1024x1024, editorial front-page collage style.
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 18, 20)
RED = (178, 34, 40)
BLUE = (24, 62, 120)
TEAL = (10, 110, 110)
GOLD = (196, 144, 32)
GREY = (90, 90, 95)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def wrap(s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def panel(x, y, w, h, accent):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=WHITE, outline=(205, 198, 182), width=2)
    d.rounded_rectangle([x, y, x + w, y + 30], radius=10, fill=accent)
    d.rectangle([x, y + 20, x + w, y + 30], fill=accent)

def headline(x, y, s, size, maxw, fill=INK, lh=None):
    f = F(SANS_B, size)
    lh = lh or int(size * 1.18)
    for i, ln in enumerate(wrap(s, f, maxw)):
        text(x, y + i * lh, ln, f, fill)
    return y + len(wrap(s, f, maxw)) * lh

def caption(x, y, s, maxw, size=17):
    f = F(SANS, size)
    for i, ln in enumerate(wrap(s, f, maxw)):
        text(x, y + i * int(size * 1.3), ln, f, (52, 52, 58))
    return y + len(wrap(s, f, maxw)) * int(size * 1.3)

def tag(x, y, s, fill=WHITE):
    text(x + 12, y + 5, s, F(SANS_B, 16), fill)

# ---------------- masthead ----------------
text(W // 2, 16, "T H E   W O R L D   I N   O N E   D A Y", F(SERIF_B, 25), INK, "ma")
d.line([36, 58, W - 36, 58], fill=INK, width=3)
text(W // 2, 66, "WEDNESDAY 18 NOVEMBER 2026", F(SERIF_B, 47), RED, "ma")
d.line([36, 128, W - 36, 128], fill=INK, width=3)
text(W // 2, 134, "Summits, strikes and a Senate flip — the day the world woke up to", F(SANS, 18), GREY, "ma")

# ---------------- lead panel: Shenzhen summit ----------------
LX, LY, LW, LH = 36, 168, W - 72, 218
panel(LX, LY, LW, LH, RED)
tag(LX, LY, "LEAD STORY  •  SHENZHEN, CHINA")
# skyline
base = LY + LH - 16
for bx, bh, bw in [(70, 62, 34), (112, 88, 28), (148, 52, 40), (196, 74, 26), (820, 66, 32), (862, 90, 26), (896, 54, 36)]:
    d.rectangle([bx, base - bh, bx + bw, base], fill=(210, 205, 192))
    for wy in range(base - bh + 8, base - 8, 14):
        for wx in range(bx + 5, bx + bw - 4, 11):
            d.rectangle([wx, wy, wx + 4, wy + 5], fill=(240, 220, 150))
# three flags on poles
def flag(cx, kind):
    px, py, fw, fh = cx - 46, LY + 62, 92, 56
    d.line([cx, py - 10, cx, py + fh], fill=(120, 120, 125), width=3)
    x0, y0 = cx - fw // 2, py
    if kind == "CN":
        d.rectangle([x0, y0, x0 + fw, y0 + fh], fill=(222, 41, 47))
        d.ellipse([x0 + 10, y0 + 9, x0 + 24, y0 + 23], fill=(255, 222, 0))
        for sx, sy in [(32, 7), (38, 16), (38, 27), (31, 34)]:
            d.ellipse([x0 + sx, y0 + sy, x0 + sx + 6, y0 + sy + 6], fill=(255, 222, 0))
    elif kind == "RU":
        d.rectangle([x0, y0, x0 + fw, y0 + fh // 3], fill=WHITE, outline=(180, 180, 180))
        d.rectangle([x0, y0 + fh // 3, x0 + fw, y0 + 2 * fh // 3], fill=(0, 57, 166))
        d.rectangle([x0, y0 + 2 * fh // 3, x0 + fw, y0 + fh], fill=(213, 43, 30))
    else:
        for i in range(7):
            col = (178, 34, 52) if i % 2 == 0 else WHITE
            d.rectangle([x0, y0 + i * fh // 7, x0 + fw, y0 + (i + 1) * fh // 7], fill=col)
        d.rectangle([x0, y0, x0 + 40, y0 + 30], fill=(10, 49, 97))
        for r in range(3):
            for c in range(4):
                d.ellipse([x0 + 5 + c * 9, y0 + 5 + r * 9, x0 + 8 + c * 9, y0 + 8 + r * 9], fill=WHITE)
flag(330, "CN"); flag(512, "RU"); flag(694, "US")
hy = headline(LX + 258, LY + 128, "XI MEETS PUTIN — TRUMP EN ROUTE FOR THREE-WAY SUMMIT", 25, 560)
# centre the lead headline block: draw over skyline centre (flags row sits above it)

# ---------------- row 2: Gulf + Ukraine ----------------
RY, RH = 402, 196
PW = (W - 72 - 16) // 2
# Gulf
panel(36, RY, PW, RH, BLUE); tag(36, RY, "MIDDLE EAST  •  STRAIT OF HORMUZ")
# strait sketch: two land masses + water gap + arcs
d.polygon([(60, RY + 118), (200, RY + 118), (168, RY + 168), (60, RY + 178)], fill=(233, 220, 190))
d.polygon([(330, RY + 96), (492, RY + 96), (492, RY + 178), (300, RY + 178), (268, RY + 132)], fill=(233, 220, 190))
text(74, RY + 122, "IRAN", F(SANS_B, 15), (120, 100, 60))
text(392, RY + 104, "QESHM I.", F(SANS_B, 13), (120, 100, 60))
for i, (sx, ex) in enumerate([(120, 300), (180, 380)]):
    yy = RY + 128 + i * 18
    d.arc([sx, yy - 26, ex, yy + 26], start=200, end=340, fill=RED, width=3)
    d.polygon([(ex, yy - 8), (ex + 12, yy), (ex, yy + 8)], fill=RED)
hy = headline(52, RY + 40, "US HITS QESHM ISLAND — IRAN FIRES BACK AT KUWAIT & BAHRAIN", 20, PW - 32)
caption(52, RY + 148, "", PW - 32)
# Ukraine
UX = 36 + PW + 16
panel(UX, RY, PW, RH, (84, 60, 140)); tag(UX, RY, "UKRAINE WAR  •  CRIMEA")
# bridge: two decks, one collapsed
wy = RY + 132
d.rectangle([UX + 16, wy + 18, UX + PW - 16, RY + RH - 10], fill=(168, 200, 226))
d.line([UX + 24, wy, UX + 190, wy], fill=INK, width=7)
d.line([UX + 300, wy, UX + PW - 24, wy], fill=INK, width=7)
d.line([UX + 190, wy, UX + 252, wy + 34], fill=RED, width=7)  # fallen span
for px_ in (70, 150, 330, 420):
    d.line([UX + px_, wy, UX + px_, wy + 20], fill=INK, width=4)
text(UX + PW // 2, wy + 40, "KERCH STRAIT", F(SANS_B, 13), (70, 110, 150), "ma")
headline(UX + 16, RY + 40, "KERCH BRIDGE STRUCK FOR A SECOND DAY — A SPAN FALLS", 20, PW - 32)

# ---------------- row 3: US Senate + Health ----------------
R3Y, R3H = 614, 176
panel(36, R3Y, PW, R3H, TEAL); tag(36, R3Y, "UNITED STATES  •  SENATE")
# capitol dome
cx = 36 + 92
d.arc([cx - 52, R3Y + 74, cx + 52, R3Y + 140], start=180, end=360, fill=(120, 140, 160))
d.rectangle([cx - 62, R3Y + 104, cx + 62, R3Y + 140], fill=(150, 165, 185))
d.line([cx, R3Y + 52, cx, R3Y + 74], fill=(120, 140, 160), width=4)
text(36 + 178, R3Y + 52, "56–44", F(SERIF_B, 52), BLUE)
headline(36 + 172, R3Y + 110, "PELTOLA WINS ALASKA — DEMOCRATS TAKE SENATE", 17, PW - 188)
# Health
HX = 36 + PW + 16
panel(HX, R3Y, PW, R3H, (168, 84, 20)); tag(HX, R3Y, "HEALTH  •  AFRICA & AMERICA")
# virus icon
vx, vy, vr = HX + 62, R3Y + 96, 30
for a in range(0, 360, 30):
    rad = math.radians(a)
    x1, y1 = vx + vr * math.cos(rad), vy + vr * math.sin(rad)
    x2, y2 = vx + (vr + 13) * math.cos(rad), vy + (vr + 13) * math.sin(rad)
    d.line([x1, y1, x2, y2], fill=RED, width=4)
    d.ellipse([x2 - 5, y2 - 5, x2 + 5, y2 + 5], fill=RED)
d.ellipse([vx - vr, vy - vr, vx + vr, vy + vr], fill=(226, 120, 110))
for sx, sy in [(-12, -8), (8, 4), (-2, 14)]:
    d.ellipse([vx + sx - 5, vy + sy - 5, vx + sx + 5, vy + sy + 5], fill=(190, 70, 60))
headline(HX + 128, R3Y + 44, "EBOLA DOUBLES IN DR CONGO: 11,000 CASES", 19, PW - 144)
caption(HX + 128, R3Y + 108, "US loses measles-free status after 26 years — 5,400 cases, 10 deaths", PW - 144, 16)

# ---------------- row 4: Disasters + Tech ----------------
R4Y, R4H = 806, 128
panel(36, R4Y, PW, R4H, (40, 90, 140)); tag(36, R4Y, "DISASTERS")
# cyclone spiral
sx, sy = 36 + 58, R4Y + 82
for r, a0 in [(26, 20), (18, 140), (10, 260)]:
    d.arc([sx - r, sy - r, sx + r, sy + r], start=a0, end=a0 + 250, fill=BLUE, width=4)
headline(36 + 108, R4Y + 40, "SIBERIA PLANE CRASH KILLS 19", 18, PW - 124)
caption(36 + 108, R4Y + 68, "Cyclone Xavier hits Cook Islands at Category 5 • 6.0 quake in Papua New Guinea", PW - 124, 15)
# Tech
TX = 36 + PW + 16
panel(TX, R4Y, PW, R4H, (60, 60, 66)); tag(TX, R4Y, "TECH & MARKETS")
# chip icon
chx, chy, cs = TX + 30, R4Y + 56, 52
d.rounded_rectangle([chx, chy, chx + cs, chy + cs], radius=6, outline=INK, width=3)
d.rounded_rectangle([chx + 14, chy + 14, chx + cs - 14, chy + cs - 14], radius=4, fill=GOLD)
for i in range(3):
    p = chy + 10 + i * 16
    d.line([chx - 10, p, chx, p], fill=INK, width=3); d.line([chx + cs, p, chx + cs + 10, p], fill=INK, width=3)
headline(TX + 108, R4Y + 40, "NVIDIA'S RECORD QUARTER", 18, PW - 124)
caption(TX + 108, R4Y + 68, "US tightens AI-chip curbs on China as AI stocks rebound", PW - 124, 15)

# ---------------- ticker ----------------
TY = 950
d.rectangle([0, TY, W, H], fill=INK)
ticker = "ISRAEL ELECTS KAHANA SPEAKER  •  COP31 CLIMATE TALKS STALL IN ANTALYA  •  CAMBRIDGE WORD OF THE YEAR: “HUMAN”"
f = F(SANS_B, 17)
while d.textlength(ticker, font=f) > W - 40 and f.size > 11:
    f = F(SANS_B, f.size - 1)
text(W // 2, TY + 16, ticker, f, WHITE, "ma")
text(W // 2, TY + 44, "One day, one picture — Wednesday 18 November 2026", F(SANS, 14), (200, 200, 205), "ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out)
print(out, os.path.getsize(out), "bytes")
