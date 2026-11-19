#!/usr/bin/env python3
"""Render the 19 November 2026 world-news front page to entry.png (v2).

Build-time only: the grader never runs this file (it runs main.py, which only
copies the committed entry.png). All news data is embedded below as fixed data,
so the render is deterministic: same input -> same PNG bytes.
News researched 19 Nov 2026 from public sources (see README.md).
Run:  python3 render_news.py   (writes entry.png next to this file)

v2 changes vs v1:
- Facts corrected: summit headline no longer claims a completed trilateral
  meeting (Xi hugged Trump on the tarmac; the three-way meeting is set for
  Thursday); EU loan and Voyager are Wednesday events, so they move to the
  ticker; Myanmar verdict is scheduled for today (outcome not claimed).
- Added: Anthropic's $81.3bn IPO / Nasdaq debut today (ANT, $83), ICJ Myanmar
  verdict today, Gulf fire spreading to Kuwait overnight, Crimean Bridge hit
  again (ticker).
- Design like a real newspaper front page: a filled hero illustration for the
  lead (flags + Shenzhen skyline, no empty navy block), an illustrated banner
  on every story, denser text so no box sits half-empty.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
PAPER = (250, 246, 238)
INK = (17, 17, 17)
NAVY = (10, 35, 80)
NAVY_DARK = (8, 28, 62)
RED = (178, 24, 24)
GOLD = (255, 205, 0)
TEAL = (13, 110, 110)
GREY = (90, 88, 82)
LINE = (200, 194, 182)

SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, color, max_w, leading, max_lines=None):
    """Draw wrapped paragraph; returns y after last line. Truncates to max_lines."""
    x, y = xy
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


# --- fixed news data (Thursday 19 November 2026) ---
LEAD = {
    "kicker": "SUMMIT IN SHENZHEN  —  APEC 2026",
    "headline": "Trump, Xi and Putin gather in Shenzhen",
    "deck": ("Xi hugged Trump on the tarmac as the leaders gathered for a "
             "first trilateral meeting today — nuclear arms, Ukraine and "
             "the Gulf on the table."),
    "foot": "3 LEADERS  •  3 NUCLEAR POWERS  •  1 TABLE",
}

ROW2 = [
    {
        "kicker": "GAMING",
        "color": (108, 38, 140),
        "headline": "GTA VI is out at last",
        "deck": ("After 13 years, the game unlocks at midnight worldwide on "
                 "PS5 and Xbox."),
        "art": "vice",
    },
    {
        "kicker": "MARKETS",
        "color": (13, 90, 60),
        "headline": "Anthropic's $81bn debut",
        "deck": ("The Claude maker priced its IPO at $83 — the biggest "
                 "debut ever. Shares start trading today."),
        "art": "chart",
    },
]

ROW3 = [
    {
        "kicker": "THE HAGUE",
        "color": (11, 42, 91),
        "headline": "World court rules on Myanmar today",
        "deck": ("The ICJ rules on The Gambia's case over the 2017 Rohingya "
                 "crackdown."),
        "art": "scales",
    },
    {
        "kicker": "WEATHER",
        "color": (150, 100, 0),
        "headline": "Akvan bears down on India",
        "deck": ("Red alert on the Andhra coast; landfall forecast by noon "
                 "Friday."),
        "art": "storm",
    },
    {
        "kicker": "THE GULF",
        "color": (150, 30, 30),
        "headline": "Gulf fire spreads to Kuwait",
        "deck": ("Iran struck US targets in Kuwait after US jets hit Qeshm "
                 "Island."),
        "art": "gulf",
    },
]

TICKER = ("ALSO TODAY  —  EU proposes a €45bn loan for Ukraine, repayable only "
          "after Russia pays reparations  •  Voyager 1 crossed one light-day on "
          "Wednesday, 25.9bn km out  •  Van Gogh sells for a record $190.4m at "
          "Sotheby's  •  Israeli tanks cross Gaza's Yellow Line in a rare ground "
          "operation  •  Crimean Bridge hit again; traffic halted")


# ---------------------------------------------------------------- art panels
def skyline(d, x0, y0, x1, y1, base, win):
    """Deterministic city skyline filling [x0,y0,x1,y1]; base colour, lit windows."""
    heights = [0.55, 0.8, 0.45, 0.95, 0.65, 0.85, 0.5, 0.75, 0.6, 0.9, 0.4, 0.7]
    n = len(heights)
    bw = (x1 - x0) / n
    for i, h in enumerate(heights):
        bx = x0 + i * bw
        top = y1 - h * (y1 - y0)
        d.rectangle([bx + 1, top, bx + bw - 1, y1], fill=base)
        for r in range(int(top) + 8, int(y1) - 6, 12):
            for c in range(int(bx) + 5, int(bx + bw) - 6, 11):
                if (r // 12 + c // 11) % 3 == 0:
                    d.rectangle([c, r, c + 4, r + 5], fill=win)
    tx = x0 + (x1 - x0) * 0.62
    d.rectangle([tx - 9, y0 + 6, tx + 9, y1], fill=base)
    d.polygon([(tx - 9, y0 + 6), (tx + 9, y0 + 6), (tx, y0 - 14)], fill=base)
    d.ellipse([tx - 3, y0 - 20, tx + 3, y0 - 14], fill=win)


def draw_flag_us(d, x, y, w, h):
    for i in range(7):
        d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                    fill=(178, 24, 24) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 0.42, y + h * 0.55], fill=(20, 40, 110))
    for r in range(3):
        for c in range(4):
            d.ellipse([x + 6 + c * 11, y + 5 + r * 10, x + 10 + c * 11, y + 9 + r * 10],
                      fill=(255, 255, 255))


def draw_flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 30, 30))
    d.ellipse([x + 8, y + 8, x + 26, y + 26], fill=GOLD)
    for cx, cy in [(x + 38, y + 10), (x + 46, y + 20), (x + 44, y + 32), (x + 34, y + 34)]:
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=GOLD)


def draw_flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(20, 60, 180))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(200, 20, 20))


def hero_art(d, x0, y0, x1, y1):
    """Lead illustration: three flags, Shenzhen label, skyline. Fills the panel."""
    d.rectangle([x0, y0, x1, y1], fill=NAVY_DARK)
    fw, fh = 104, 62
    xs = [x0 + 16, x0 + 132, x0 + 248]
    drawers = [draw_flag_us, draw_flag_cn, draw_flag_ru]
    for fx, fn in zip(xs, drawers):
        d.rectangle([fx + fw // 2 - 2, y0 + 8, fx + fw // 2 + 2, y0 + 14 + fh], fill=GOLD)
        fn(d, fx, y0 + 14, fw, fh)
    d.text(((x0 + x1) // 2, y0 + 96), "SHENZHEN",
           font=font(SANS_B, 30), fill=(255, 255, 255), anchor="ma")
    d.text(((x0 + x1) // 2, y0 + 132), "USA  •  CHINA  •  RUSSIA",
           font=font(SANS, 17), fill=GOLD, anchor="ma")
    d.text(((x0 + x1) // 2, y0 + 158), "FIRST MEETING OF THE THREE",
           font=font(SANS_B, 13), fill=(180, 200, 230), anchor="ma")
    skyline(d, x0, y1 - 78, x1, y1, (4, 16, 40), GOLD)


def palm(d, x, ybase, h, color):
    d.line([x, ybase, x, ybase - h], fill=color, width=4)
    for ang in (200, 240, 290, 330):
        a = math.radians(ang)
        d.arc([x - 18, ybase - h - 14, x + 18, ybase - h + 14],
              start=ang - 40, end=ang + 40, fill=color, width=3)


def art_vice(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(32, 16, 64))
    d.ellipse([x1 - 58, y0 + 10, x1 - 18, y0 + 50], fill=(255, 220, 120))
    d.text((x0 + 12, y0 + 8), "VICE CITY", font=font(SANS_B, 22),
           fill=(255, 90, 180))
    d.text((x0 + 12, y0 + 36), "LEONIDA  •  $1.5BN PRE-ORDERS",
           font=font(SANS_B, 12), fill=(200, 180, 255))
    skyline(d, x0, y1 - 32, x1, y1, (8, 6, 20), (255, 90, 180))
    palm(d, x0 + 215, y1 - 2, 26, (6, 30, 12))
    palm(d, x0 + 330, y1 - 2, 22, (6, 30, 12))


def art_chart(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(10, 52, 42))
    for gy in range(y0 + 16, y1 - 8, 16):
        d.line([x0 + 8, gy, x1 - 8, gy], fill=(40, 90, 75), width=1)
    bars = [16, 22, 18, 30, 26, 38, 46]
    bw = (x1 - x0 - 150) / len(bars)
    for i, bh in enumerate(bars):
        bx = x0 + 150 + i * bw
        d.rectangle([bx + 3, y1 - 8 - bh, bx + bw - 3, y1 - 8], fill=(60, 160, 120))
    pts = [(x0 + 152, y1 - 26), (x0 + 205, y1 - 46), (x0 + 255, y1 - 36),
           (x0 + 305, y1 - 62)]
    d.line(pts, fill=GOLD, width=4, joint="curve")
    d.polygon([(x0 + 305, y1 - 62), (x0 + 293, y1 - 58), (x0 + 305, y1 - 76)],
              fill=GOLD)
    d.text((x0 + 12, y0 + 6), "ANT", font=font(SANS_B, 30), fill=(255, 255, 255))
    d.text((x0 + 12, y0 + 40), "$83", font=font(SANS_B, 26), fill=GOLD)
    d.text((x0 + 12, y0 + 70), "BIGGEST IPO EVER",
           font=font(SANS_B, 11), fill=(180, 230, 210))


def art_scales(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=NAVY)
    cx, cy = (x0 + x1) // 2, y0 + 8
    d.rectangle([cx - 2, cy, cx + 2, y1 - 6], fill=GOLD)
    d.line([cx - 42, cy + 5, cx + 42, cy + 5], fill=GOLD, width=3)
    for s in (-1, 1):
        px = cx + s * 42
        d.line([px, cy + 5, px, cy + 19], fill=GOLD, width=2)
        d.pieslice([px - 16, cy + 15, px + 16, cy + 31], start=0, end=180, fill=GOLD)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=GOLD)
    d.rectangle([x0, y1 - 6, x1, y1], fill=GOLD)


def art_storm(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(8, 70, 80))
    d.polygon([(x1 - 70, y0), (x1, y0), (x1, y1), (x1 - 110, y1),
               (x1 - 88, y0 + 28)], fill=(210, 180, 120))
    cx, cy = x0 + 58, y0 + 28
    for i, rr in enumerate(range(26, 4, -6)):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr],
              start=15 + i * 60, end=195 + i * 60, fill=(255, 255, 255), width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=GOLD)


def art_gulf(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(18, 38, 72))
    d.polygon([(x0, y0), (x1, y0), (x1, y0 + 18), (x0 + 150, y0 + 24),
               (x0 + 120, y0 + 40), (x0, y0 + 34)], fill=(210, 185, 130))
    d.rectangle([x0, y0 + 34, x1, y1], fill=(30, 90, 160))
    for (mx, my, lab) in [(x0 + 70, y1 - 14, "QESHM"), (x0 + 165, y1 - 14, "BAHRAIN"),
                          (x0 + 215, y0 + 12, "KUWAIT")]:
        d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=(255, 60, 40))
        d.text((mx + 8, my - 7), lab, font=font(SANS_B, 10), fill=(255, 255, 255))


ART = {"vice": art_vice, "chart": art_chart, "scales": art_scales,
       "storm": art_storm, "gulf": art_gulf}


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead, like a real paper ---
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.text((24, 10), "THE WORLD", font=font(SERIF_B, 58), fill=(255, 255, 255))
    d.text((W - 24, 14), "THURSDAY", font=font(SANS_B, 24),
           fill=(255, 255, 255), anchor="ra")
    d.text((W - 24, 46), "19 NOVEMBER 2026", font=font(SANS_B, 24),
           fill=GOLD, anchor="ra")
    d.rectangle([0, 96, W, 126], fill=GOLD)
    d.text((W // 2, 101),
           "SHENZHEN  •  NEW YORK  •  THE HAGUE  •  MUMBAI  —  THE DAY'S WORLD NEWS IN ONE PAGE",
           font=font(SANS_B, 16), fill=NAVY, anchor="ma")
    d.rectangle([0, 126, W, 130], fill=RED)

    # --- lead story with a filled hero illustration ---
    d.rectangle([24, 140, 1000, 448], outline=LINE, width=2, fill=(255, 255, 255))
    d.rectangle([24, 140, 1000, 146], fill=RED)
    d.text((44, 158), LEAD["kicker"], font=font(SANS_B, 19), fill=RED)
    y = para(d, (44, 186), LEAD["headline"], font(SERIF_B, 44), INK, 556, 50,
             max_lines=3)
    y = para(d, (44, y + 10), LEAD["deck"], font(SANS, 20), (60, 58, 52), 556, 28,
             max_lines=4)
    d.rectangle([44, 402, 600, 404], fill=LINE)
    d.text((44, 414), LEAD["foot"], font=font(SANS_B, 16), fill=NAVY)
    hero_art(d, 612, 158, 980, 434)

    # --- row 2: two stories, each with an illustrated banner ---
    for i, s in enumerate(ROW2):
        x = 24 + i * (478 + 16)
        yy = 460
        d.rectangle([x, yy, x + 478, yy + 220], outline=LINE, width=2,
                    fill=(255, 255, 255))
        d.rectangle([x, yy, x + 478, yy + 6], fill=s["color"])
        ART[s["art"]](d, x + 12, yy + 14, x + 478 - 12, yy + 100)
        d.text((x + 18, yy + 108), s["kicker"], font=font(SANS_B, 16),
               fill=s["color"])
        hy = para(d, (x + 18, yy + 130), s["headline"], font(SERIF_B, 26), INK,
                  478 - 36, 30, max_lines=1)
        para(d, (x + 18, hy + 4), s["deck"], font(SANS, 17), (60, 58, 52),
             478 - 36, 21, max_lines=2)

    # --- row 3: three stories, each with a small illustrated banner ---
    for i, s in enumerate(ROW3):
        x = 24 + i * (314 + 17)
        yy = 692
        d.rectangle([x, yy, x + 314, yy + 188], outline=LINE, width=2,
                    fill=(255, 255, 255))
        d.rectangle([x, yy, x + 314, yy + 6], fill=s["color"])
        ART[s["art"]](d, x + 10, yy + 12, x + 314 - 10, yy + 68)
        d.text((x + 14, yy + 74), s["kicker"], font=font(SANS_B, 14),
               fill=s["color"])
        hy = para(d, (x + 14, yy + 92), s["headline"], font(SERIF_B, 20), INK,
                  314 - 28, 23, max_lines=2)
        para(d, (x + 14, hy + 3), s["deck"], font(SANS, 15), (60, 58, 52),
             314 - 28, 19, max_lines=2)

    # --- ticker strip ---
    d.rectangle([24, 892, 1000, 958], fill=(30, 30, 30))
    para(d, (44, 898), TICKER, font(SANS, 16), (255, 255, 255), 932, 21,
         max_lines=3)

    # --- footer: sources ---
    d.text((W // 2, 968),
           "Sources: NYT, Reuters, BBC, AP, Smithsonian / NASA, IMD, Sotheby's, Nasdaq — 19 Nov 2026",
           font=font(SANS, 14), fill=GREY, anchor="ma")
    d.text((W // 2, 990), "All pictures drawn by a program. No photograph is from the day.",
           font=font(SANS, 12), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
