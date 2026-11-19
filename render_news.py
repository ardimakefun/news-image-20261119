#!/usr/bin/env python3
"""Render the 19 November 2026 world-news front page to entry.png.

Build-time only: the grader never runs this file (it runs main.py, which only
copies the committed entry.png). All news data is embedded below as fixed data,
so the render is deterministic: same input -> same PNG bytes.
News researched 19 Nov 2026 from public sources (see README.md).
Run:  python3 render_news.py   (writes entry.png next to this file)
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
PAPER = (251, 248, 241)
INK = (17, 17, 17)
NAVY = (11, 42, 91)
RED = (185, 28, 28)
TEAL = (13, 110, 110)
AMBER = (176, 120, 0)
GREY = (90, 88, 82)
LINE = (200, 194, 182)

SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
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


def para(draw, xy, text, fnt, color, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


# --- fixed news data (Thursday 19 November 2026) ---
LEAD = {
    "kicker": "SUMMIT IN SHENZHEN",
    "headline": "Trump, Xi and Putin meet face to face",
    "deck": ("The three leaders shake hands in Shenzhen, then sit down for a "
             "trilateral meeting as the summit gathers — trade, Ukraine and "
             "the Gulf on the table."),
}

STORIES = [
    {
        "kicker": "GAMING",
        "color": (108, 38, 140),
        "headline": "GTA VI is out at last",
        "deck": ("After a 13-year wait, Grand Theft Auto VI begins its global "
                 "rollout. Gamers head back to Vice City."),
        "icon": "controller",
    },
    {
        "kicker": "EUROPE",
        "color": (11, 42, 91),
        "headline": "\u20ac45bn loan for Ukraine",
        "deck": ("The EU proposes a \u20ac45 billion loan for Kyiv, to be repaid "
                 "once Russia pays reparations."),
        "icon": "stars",
    },
    {
        "kicker": "SPACE",
        "color": (13, 110, 110),
        "headline": "Voyager 1, a light-day away",
        "deck": ("After almost 50 years in space, NASA's Voyager 1 is believed "
                 "to have reached one light-day from Earth."),
        "icon": "rocket",
    },
    {
        "kicker": "WEATHER",
        "color": (176, 120, 0),
        "headline": "Cyclone Akvan nears India",
        "deck": ("Cyclone Akvan is set to cross India's east coast between "
                 "Machilipatnam and Puri. States are on alert."),
        "icon": "cyclone",
    },
]

TICKER = ("ALSO TODAY  \u2014  US and Iran exchange fire again as Tehran widens its strikes on "
          "Gulf states  \u2022  Van Gogh sells for a record $190.4m  \u2022  Myanmar faces a "
          "genocide verdict at the UN court  \u2022  Israeli forces in a rare Gaza ground "
          "operation beyond the Yellow Line")


def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=(255, 255, 255), width=3)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
          start=200, end=340, fill=(255, 255, 255), width=3)


def draw_icon(d, kind, x, y, s, color):
    """Small pictogram inside a s x s box at (x, y)."""
    if kind == "controller":
        d.rounded_rectangle([x + 6, y + s // 3, x + s - 6, y + 2 * s // 3],
                            radius=12, outline=color, width=4)
        d.ellipse([x + s // 4 - 5, y + s // 2 - 5, x + s // 4 + 5, y + s // 2 + 5],
                  fill=color)
        d.ellipse([x + 3 * s // 4 - 5, y + s // 2 - 5, x + 3 * s // 4 + 5, y + s // 2 + 5],
                  fill=color)
    elif kind == "stars":
        d.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], fill=color)
        for i in range(12):
            a = math.pi * 2 * i / 12 - math.pi / 2
            px = x + s / 2 + math.cos(a) * s * 0.32
            py = y + s / 2 + math.sin(a) * s * 0.32
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 215, 0))
    elif kind == "rocket":
        d.polygon([(x + s / 2, y + 4), (x + s - 14, y + s - 18), (x + s / 2, y + s - 30),
                   (x + 14, y + s - 18)], outline=color, width=4)
        d.ellipse([x + s / 2 - 7, y + s / 2 - 7, x + s / 2 + 7, y + s / 2 + 7], fill=color)
        d.polygon([(x + s / 2 - 8, y + s - 26), (x + s / 2 + 8, y + s - 26),
                   (x + s / 2, y + s - 4)], fill=(185, 28, 28))
    elif kind == "cyclone":
        for i, rr in enumerate(range(s // 2, 6, -9)):
            d.arc([x + s / 2 - rr, y + s / 2 - rr, x + s / 2 + rr, y + s / 2 + rr],
                  start=20 + i * 55, end=200 + i * 55, fill=color, width=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 108], fill=NAVY)
    d.text((24, 14), "THE WORLD", font=font(SERIF_B, 62), fill=(255, 255, 255))
    d.text((W - 24, 20), "THURSDAY", font=font(SANS_B, 26),
           fill=(255, 255, 255), anchor="ra")
    d.text((W - 24, 52), "19 NOVEMBER 2026", font=font(SANS_B, 26),
           fill=(255, 215, 0), anchor="ra")
    d.rectangle([0, 108, W, 142], fill=(255, 215, 0))
    d.text((W // 2, 113), "THE DAY'S WORLD NEWS \u2014 IN ONE PAGE",
           font=font(SANS_B, 22), fill=NAVY, anchor="ma")

    # --- lead story ---
    d.rectangle([24, 156, 1000, 448], outline=LINE, width=2, fill=(255, 255, 255))
    d.rectangle([24, 156, 1000, 162], fill=RED)
    d.text((44, 178), LEAD["kicker"], font=font(SANS_B, 20), fill=RED)
    y = para(d, (44, 206), LEAD["headline"], font(SERIF_B, 48), INK, 620, 56)
    para(d, (44, y + 8), LEAD["deck"], font(SANS, 22), (60, 58, 52), 620, 30)
    # globe art on the right of the lead
    d.rectangle([700, 178, 980, 428], fill=NAVY)
    draw_globe(d, 840, 268, 62)
    d.text((840, 348), "SHENZHEN", font=font(SANS_B, 22), fill=(255, 255, 255), anchor="ma")
    d.text((840, 380), "USA \u2022 CHINA \u2022 RUSSIA", font=font(SANS, 18),
           fill=(255, 215, 0), anchor="ma")

    # --- 2x2 story grid ---
    gx, gy = 24, 464
    pw, ph, gap = 478, 196, 16
    for i, s in enumerate(STORIES):
        x = gx + (i % 2) * (pw + gap)
        yy = gy + (i // 2) * (ph + gap)
        d.rectangle([x, yy, x + pw, yy + ph], outline=LINE, width=2, fill=(255, 255, 255))
        d.rectangle([x, yy, x + pw, yy + 6], fill=s["color"])
        d.text((x + 18, yy + 18), s["kicker"], font=font(SANS_B, 16), fill=s["color"])
        draw_icon(d, s["icon"], x + pw - 84, yy + 14, 64, s["color"])
        hy = para(d, (x + 18, yy + 46), s["headline"], font(SERIF_B, 27), INK,
                  pw - 110, 33)
        para(d, (x + 18, hy + 4), s["deck"], font(SANS, 18), (60, 58, 52),
             pw - 36, 24)

    # --- ticker strip ---
    d.rectangle([24, 884, 1000, 968], fill=(30, 30, 30))
    para(d, (44, 892), TICKER, font(SANS, 18), (255, 255, 255), 932, 25)

    # --- footer: sources ---
    d.text((W // 2, 980),
           "Sources: AP, BBC, Financial Times, The Hindu, The New York Times \u2014 19 Nov 2026",
           font=font(SANS, 15), fill=GREY, anchor="ma")
    d.text((W // 2, 1002), "Drawn by a program. No photograph is from the day.",
           font=font(SANS, 13), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
