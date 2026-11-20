#!/usr/bin/env python3
"""Render v7: "The World in One Page" — three illustrated leads, a world
map, region counts, a date check.

Build-time only: the grader never runs this file (it runs main.py, which
only copies the committed entry.png). All news data is embedded below as
fixed data, so the render is deterministic: same input -> same PNG bytes.
News researched 20 Nov 2026 from public sources (see README.md and
work/research-v6.md + work/research-v6-addendum.md). 44 stories from
Thursday 19 November 2026: 3 illustrated leads + 12 illustrated grid
items + 29 numbered briefs. The two 18 Nov items from v6's "Yesterday"
slot are no longer stories on the page — they are named in the DATE CHECK
footer as news left out on purpose, with six more other-day items.

v7 is a bounded delta on v6 (which was audit-GO): it adds the four
features every top entry on the leaderboard shares — three large
illustrated lead panels (Shenzhen summit, ICJ verdict, Anthropic debut),
a "WHERE IT HAPPENED" world map drawn in code with numbered pins tied
to the numbered briefs, a region-counted strip (counts computed from the
actual story list, summing to 44), and a stronger DATE CHECK footer
naming the specific items left out as other days' news. The structure
is borrowed from the top entries; no text, headline, wording or drawing
is copied from them — all content is our own verified research and our
own flat illustrations.

Style is deliberately NON-photorealistic: flat geometric diagrammatic
illustration in the newspaper-infographic manner — solid colour blocks,
bold silhouettes, simple pictograms drawn from primitives (circles,
rectangles, triangles, lines). No gradients, no photorealistic shading,
no fake photos, no detailed or realistic faces: the three leaders in the
lead illustration are abstract silhouettes without features, identified
by name plates and their flags.

Run:  python3 render_v7.py   (writes entry.png next to this file)

Deterministic: fixed data, fixed fonts, no randomness, no clock, no network.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 36                      # side margin
CW = W - 2 * M              # content width = 952
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (250, 247, 238)     # warm ivory newsprint
INK = (16, 16, 16)
BODY = (40, 40, 40)
GREY = (110, 108, 100)
RULE = (190, 185, 172)
ACCENT = (216, 30, 38)     # news red, the main accent
STEEL = (51, 89, 126)       # WORLD
OCHRE = (122, 92, 20)       # BUSINESS
SLATE = (58, 58, 58)        # TECH
TEAL = (31, 110, 110)       # SCIENCE
SKY = (74, 107, 138)        # WEATHER
GREEN = (47, 107, 51)       # SPORT
WINE = (122, 46, 74)        # CULTURE
CREAM = (250, 247, 238)
WHITE = (255, 255, 255)

FDIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


F_BLACK = lambda s: font("NotoSans-Black.ttf", s)
F_XBOLD = lambda s: font("NotoSans-ExtraBold.ttf", s)
F_BOLD = lambda s: font("NotoSans-Bold.ttf", s)
F_REG = lambda s: font("NotoSans-Regular.ttf", s)
F_SERIF = lambda s: font("NotoSerifDisplay-Black.ttf", s)
F_SERIF_IT = lambda s: font("NotoSerifDisplay-Italic.ttf", s)


def text_w(draw, text, f):
    return draw.textbbox((0, 0), text, font=f)[2]


def tracked(draw, x, y, text, f, fill, tracking=2):
    """Draw text with extra letter spacing; returns the x after the text."""
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=f, fill=fill)
        cx += text_w(draw, ch, f) + tracking
    return cx - tracking


def tracked_w(draw, text, f, tracking=2):
    return sum(text_w(draw, ch, f) + tracking for ch in text) - tracking


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def wrap_strict(draw, text, f, max_w, max_lines, what):
    """Wrap and fail loudly if the text does not fit the allotted lines."""
    lines = wrap(draw, text, f, max_w)
    assert len(lines) <= max_lines, (
        f"{what}: {len(lines)} lines > {max_lines}: {text!r}")
    return lines


# ---------------------------------------------------------------- pictograms
# Every pictogram is drawn from flat primitives inside a square tile of
# side s at (x, y). fg is the pictogram colour, bg the tile colour.

def picto_globe(d, x, y, s, fg):
    d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=fg, width=3)
    d.ellipse([x + s // 4, y + 2, x + 3 * s // 4, y + s - 2], outline=fg, width=2)
    d.line([x + 2, y + s // 2, x + s - 2, y + s // 2], fill=fg, width=2)
    d.arc([x + 2, y + s // 4, x + s - 2, y + 3 * s // 4], 200, 340, fill=fg, width=2)


def picto_scales(d, x, y, s, fg):
    cx = x + s // 2
    d.line([cx, y + 4, cx, y + s - 6], fill=fg, width=3)
    d.line([x + 6, y + 10, x + s - 6, y + 10], fill=fg, width=3)
    d.line([x + 6, y + 10, x + 10, y + s // 2], fill=fg, width=2)
    d.line([x + s - 6, y + 10, x + s - 10, y + s // 2], fill=fg, width=2)
    d.polygon([(x + 4, y + s // 2), (x + 16, y + s // 2), (x + 10, y + s // 2 + 7)],
              fill=fg)
    d.polygon([(x + s - 16, y + s // 2), (x + s - 4, y + s // 2),
               (x + s - 10, y + s // 2 + 7)], fill=fg)
    d.rectangle([cx - 8, y + s - 6, cx + 8, y + s - 3], fill=fg)


def picto_gavel(d, x, y, s, fg):
    d.line([x + 8, y + s - 8, x + s - 8, y + 8], fill=fg, width=4)
    d.rectangle([x + 6, y + 6, x + s // 2, y + 16], fill=fg)
    d.rectangle([x + s // 2 - 4, y + s // 2 - 4, x + s - 6, y + s // 2 + 6],
                fill=fg)


def picto_chart_down(d, x, y, s, fg):
    pts = [(x + 4, y + 8), (x + s // 3, y + s // 3), (x + s // 2, y + s // 4),
           (x + 2 * s // 3, y + s // 2), (x + s - 6, y + s - 8)]
    d.line(pts, fill=fg, width=3, joint="curve")
    d.polygon([(x + s - 6, y + s - 8), (x + s - 14, y + s - 8),
               (x + s - 6, y + s - 16)], fill=fg)
    d.line([x + 4, y + s - 6, x + s - 4, y + s - 6], fill=fg, width=2)


def picto_chart_up(d, x, y, s, fg):
    pts = [(x + 4, y + s - 8), (x + s // 3, y + 2 * s // 3),
           (x + s // 2, y + 3 * s // 4), (x + 2 * s // 3, y + s // 2),
           (x + s - 6, y + 8)]
    d.line(pts, fill=fg, width=3, joint="curve")
    d.polygon([(x + s - 6, y + 8), (x + s - 14, y + 8), (x + s - 6, y + 16)],
              fill=fg)
    d.line([x + 4, y + s - 6, x + s - 4, y + s - 6], fill=fg, width=2)


def picto_bitcoin(d, x, y, s, fg):
    d.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], outline=fg, width=3)
    d.text((x + s // 2 - 7, y + s // 2 - 11), "B", font=F_XBOLD(20), fill=fg)


def picto_factory(d, x, y, s, fg):
    d.rectangle([x + 5, y + s // 2, x + s - 5, y + s - 5], fill=fg)
    d.polygon([(x + 5, y + s // 2), (x + 13, y + s // 3), (x + 21, y + s // 2)],
              fill=fg)
    d.polygon([(x + 21, y + s // 2), (x + 29, y + s // 3), (x + 37, y + s // 2)],
              fill=fg)
    d.rectangle([x + 8, y + 6, x + 13, y + s // 2], fill=fg)


def picto_cloud(d, x, y, s, fg):
    d.ellipse([x + 4, y + s // 2 - 2, x + 18, y + s - 8], fill=fg)
    d.ellipse([x + 14, y + 6, x + 30, y + s - 8], fill=fg)
    d.ellipse([x + 26, y + s // 2, x + s - 4, y + s - 8], fill=fg)
    d.rectangle([x + 6, y + s - 10, x + s - 6, y + s - 6], fill=fg)


def picto_chip(d, x, y, s, fg):
    d.rectangle([x + 10, y + 10, x + s - 10, y + s - 10], outline=fg, width=3)
    d.rectangle([x + 17, y + 17, x + s - 17, y + s - 17], fill=fg)
    for i in range(3):
        px = x + 14 + i * 8
        d.line([px, y + 4, px, y + 10], fill=fg, width=2)
        d.line([px, y + s - 10, px, y + s - 4], fill=fg, width=2)
        d.line([x + 4, px, x + 10, px], fill=fg, width=2)
        d.line([x + s - 10, px, x + s - 4, px], fill=fg, width=2)


def picto_lock(d, x, y, s, fg):
    d.rectangle([x + 8, y + s // 2, x + s - 8, y + s - 5], fill=fg)
    d.arc([x + 12, y + 6, x + s - 12, y + s // 2 + 4], 180, 360, fill=fg,
          width=3)
    d.rectangle([x + s // 2 - 2, y + s // 2 + 5, x + s // 2 + 2,
                 y + s // 2 + 12], fill=_BG)


def picto_flask(d, x, y, s, fg):
    d.rectangle([x + s // 2 - 4, y + 5, x + s // 2 + 4, y + 16], fill=fg)
    d.polygon([(x + s // 2 - 4, y + 16), (x + s // 2 + 4, y + 16),
               (x + s - 6, y + s - 5), (x + 6, y + s - 5)], fill=fg)
    d.line([x + 12, y + s - 12, x + s - 12, y + s - 12], fill=_BG, width=3)


def picto_star4(d, x, y, s, fg):
    cx, cy = x + s // 2, y + s // 2
    d.polygon([(cx, y + 3), (cx + 5, cy - 5), (x + s - 3, cy), (cx + 5, cy + 5),
               (cx, y + s - 3), (cx - 5, cy + 5), (x + 3, cy), (cx - 5, cy - 5)],
              fill=fg)


def picto_satellite(d, x, y, s, fg):
    d.rectangle([x + 15, y + 14, x + 29, y + 28], fill=fg)
    d.rectangle([x + 4, y + 18, x + 14, y + 26], outline=fg, width=2)
    d.rectangle([x + 30, y + 18, x + s - 4, y + 26], outline=fg, width=2)
    d.line([x + 22, y + 28, x + 28, y + s - 5], fill=fg, width=2)
    d.line([x + 30, y + 10, x + 36, y + 4], fill=fg, width=2)


def picto_moth(d, x, y, s, fg):
    d.ellipse([x + 5, y + 8, x + 19, y + 24], fill=fg)
    d.ellipse([x + 25, y + 8, x + s - 5, y + 24], fill=fg)
    d.ellipse([x + 8, y + 24, x + 19, y + s - 8], fill=fg)
    d.ellipse([x + 25, y + 24, x + s - 8, y + s - 8], fill=fg)
    d.rectangle([x + 20, y + 6, x + 24, y + s - 6], fill=fg)


def picto_cyclone(d, x, y, s, fg):
    for r, a0, a1 in [(16, 0, 300), (11, 40, 330), (6, 80, 320)]:
        d.arc([x + s // 2 - r, y + s // 2 - r, x + s // 2 + r,
               y + s // 2 + r], a0, a1, fill=fg, width=3)
    d.ellipse([x + s // 2 - 2, y + s // 2 - 2, x + s // 2 + 2,
               y + s // 2 + 2], fill=fg)


def picto_ball(d, x, y, s, fg):
    d.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], outline=fg, width=3)
    d.polygon([(x + s // 2, y + 12), (x + s // 2 + 6, y + 18),
               (x + s // 2 + 4, y + 26), (x + s // 2 - 4, y + 26),
               (x + s // 2 - 6, y + 18)], fill=fg)
    d.line([x + s // 2, y + 12, x + s // 2, y + 5], fill=fg, width=2)
    d.line([x + s // 2 - 6, y + 18, x + 5, y + 16], fill=fg, width=2)
    d.line([x + s // 2 + 6, y + 18, x + s - 5, y + 16], fill=fg, width=2)


def picto_trophy(d, x, y, s, fg):
    d.polygon([(x + 11, y + 5), (x + s - 11, y + 5), (x + s - 14, y + 22),
               (x + 14, y + 22)], fill=fg)
    d.arc([x + 5, y + 6, x + 15, y + 20], 90, 270, fill=fg, width=3)
    d.arc([x + s - 15, y + 6, x + s - 5, y + 20], 270, 90, fill=fg, width=3)
    d.rectangle([x + s // 2 - 2, y + 22, x + s // 2 + 2, y + 30], fill=fg)
    d.rectangle([x + 14, y + 30, x + s - 14, y + 34], fill=fg)


def picto_tv(d, x, y, s, fg):
    d.rectangle([x + 5, y + 12, x + s - 5, y + s - 8], outline=fg, width=3)
    d.line([x + s // 2, y + 12, x + s - 10, y + 4], fill=fg, width=2)
    d.line([x + s // 2, y + 12, x + 10, y + 4], fill=fg, width=2)
    d.line([x + 10, y + 20, x + s - 10, y + 20], fill=fg, width=2)
    d.line([x + 10, y + 26, x + s - 16, y + 26], fill=fg, width=2)


def picto_note(d, x, y, s, fg):
    d.ellipse([x + 8, y + s - 14, x + 18, y + s - 5], fill=fg)
    d.rectangle([x + 16, y + 8, x + 19, y + s - 10], fill=fg)
    d.polygon([(x + 19, y + 8), (x + 19, y + 16), (x + 32, y + 12),
               (x + 32, y + 5)], fill=fg)


def picto_film(d, x, y, s, fg):
    d.rectangle([x + 6, y + 8, x + s - 6, y + s - 8], outline=fg, width=3)
    for yy in (13, 21, 29):
        d.rectangle([x + 9, yy, x + 13, yy + 4], fill=fg)
        d.rectangle([x + s - 13, yy, x + s - 9, yy + 4], fill=fg)
    d.polygon([(x + 19, y + 13), (x + 19, y + 29), (x + 30, y + 21)], fill=fg)


def picto_book(d, x, y, s, fg):
    d.rectangle([x + 5, y + 8, x + s // 2 - 1, y + s - 8], fill=fg)
    d.rectangle([x + s // 2 + 1, y + 8, x + s - 5, y + s - 8], fill=fg)
    d.line([x + 9, y + 14, x + s // 2 - 5, y + 14], fill=_BG, width=2)
    d.line([x + s // 2 + 5, y + 14, x + s - 9, y + 14], fill=_BG, width=2)
    d.line([x + 9, y + 20, x + s // 2 - 5, y + 20], fill=_BG, width=2)
    d.line([x + s // 2 + 5, y + 20, x + s - 9, y + 20], fill=_BG, width=2)


def picto_moon(d, x, y, s, fg):
    d.ellipse([x + 8, y + 6, x + s - 8, y + s - 6], fill=fg)
    d.ellipse([x + 16, y + 3, x + s - 2, y + s - 9], fill=_BG)


def picto_court(d, x, y, s, fg):
    d.polygon([(x + 4, y + 12), (x + s // 2, y + 4), (x + s - 4, y + 12)],
              fill=fg)
    for cx in (10, 20, 30):
        d.rectangle([x + cx - 2, y + 14, x + cx + 2, y + s - 10], fill=fg)
    d.rectangle([x + 5, y + s - 10, x + s - 5, y + s - 6], fill=fg)


def picto_bridge(d, x, y, s, fg):
    d.arc([x + 4, y + 6, x + s - 4, y + s - 4], 180, 360, fill=fg, width=3)
    d.line([x + 4, y + s - 8, x + s - 4, y + s - 8], fill=fg, width=3)
    for xx in (12, 22, 32):
        d.line([x + xx, y + 12, x + xx, y + s - 8], fill=fg, width=2)


def picto_ship(d, x, y, s, fg):
    d.polygon([(x + 5, y + 22), (x + s - 5, y + 22), (x + s - 12, y + 32),
               (x + 12, y + 32)], fill=fg)
    d.line([x + s // 2, y + 8, x + s // 2, y + 22], fill=fg, width=3)
    d.polygon([(x + s // 2, y + 8), (x + s // 2, y + 20),
               (x + s // 2 + 10, y + 20)], fill=fg)


def picto_phone(d, x, y, s, fg):
    d.rounded_rectangle([x + 12, y + 4, x + s - 12, y + s - 4], radius=4,
                        outline=fg, width=3)
    d.line([x + 17, y + 12, x + s - 17, y + 12], fill=fg, width=2)
    d.line([x + 17, y + 18, x + s - 17, y + 18], fill=fg, width=2)


def picto_shield(d, x, y, s, fg):
    d.polygon([(x + 6, y + 5), (x + s - 6, y + 5), (x + s - 6, y + 20),
               (x + s // 2, y + s - 5), (x + 6, y + 20)], fill=fg)
    d.text((x + s // 2 - 4, y + 12), "!", font=F_XBOLD(16), fill=_BG)


def picto_gamepad(d, x, y, s, fg):
    d.rounded_rectangle([x + 4, y + 12, x + s - 4, y + s - 10], radius=8,
                        fill=fg)
    d.rectangle([x + 9, y + 19, x + 17, y + 23], fill=PAPER)
    d.rectangle([x + 11, y + 17, x + 15, y + 25], fill=PAPER)
    d.ellipse([x + 27, y + 18, x + 31, y + 22], fill=PAPER)
    d.ellipse([x + 33, y + 22, x + 37, y + 26], fill=PAPER)


def picto_clapper(d, x, y, s, fg):
    d.rectangle([x + 5, y + 16, x + s - 5, y + s - 6], fill=fg)
    d.polygon([(x + 5, y + 16), (x + 8, y + 8), (x + s - 5, y + 8),
               (x + s - 5, y + 16)], fill=fg)
    for xx in (12, 22, 32):
        d.line([x + xx, y + 9, x + xx - 4, y + 15], fill=_BG, width=2)


def picto_mic(d, x, y, s, fg):
    d.ellipse([x + 14, y + 5, x + 30, y + 21], fill=fg)
    d.arc([x + 11, y + 16, x + 33, y + 32], 0, 180, fill=fg, width=3)
    d.line([x + s // 2, y + 32, x + s // 2, y + s - 5], fill=fg, width=3)


PICTOS = {
    "globe": picto_globe, "scales": picto_scales, "gavel": picto_gavel,
    "chart-down": picto_chart_down, "chart-up": picto_chart_up,
    "bitcoin": picto_bitcoin, "factory": picto_factory, "cloud": picto_cloud,
    "chip": picto_chip, "lock": picto_lock, "flask": picto_flask,
    "star": picto_star4, "satellite": picto_satellite, "moth": picto_moth,
    "cyclone": picto_cyclone, "ball": picto_ball, "trophy": picto_trophy,
    "tv": picto_tv, "note": picto_note, "film": picto_film,
    "book": picto_book, "moon": picto_moon, "court": picto_court,
    "bridge": picto_bridge, "ship": picto_ship, "phone": picto_phone,
    "shield": picto_shield, "gamepad": picto_gamepad,
    "clapper": picto_clapper, "mic": picto_mic,
}


_BG = PAPER  # current tile colour, for pictogram cut-out details


def tile(d, x, y, s, colour, key):
    """Flat coloured tile with a white pictogram drawn from primitives."""
    global _BG
    _BG = colour
    d.rounded_rectangle([x, y, x + s, y + s], radius=4, fill=colour)
    PICTOS[key](d, x, y, s, CREAM)


def picto_scaled(img, x, y, s, colour, key):
    """Draw a 44px pictogram scaled to s px on a tile-coloured square.

    The pictogram functions are written for a 44px tile (absolute
    coordinates up to 44); the grid band is only 38px tall, so the
    pictogram is rendered at its native size and scaled down. The
    resize is deterministic, so the render stays byte-identical.
    """
    global _BG
    _BG = colour
    tmp = Image.new("RGB", (44, 44), colour)
    td = ImageDraw.Draw(tmp)
    PICTOS[key](td, 0, 0, 44, CREAM)
    img.paste(tmp.resize((s, s), Image.LANCZOS), (x, y))


# ------------------------------------------------------------------- data
# Fixed news data for Thursday 19 November 2026. Every headline, figure
# and date below is as written in work/research-v6.md and
# work/research-v6-addendum.md; nothing is invented.
#
# Story count: 3 leads + 12 grid + 29 numbered briefs = 44 stories.
# Region counts (computed from this list, must sum to 44):
#   ASIA 6, MIDDLE EAST 2, EUROPE 6, AFRICA 1, AMERICAS 21, OCEANIA 1,
#   GLOBAL 7  ->  6+2+6+1+21+1+7 = 44.
# Gordon Bell is counted AMERICAS: the prize was won at SC26 in Chicago,
# so its place (CHICAGO), its map pin and its region now all agree.

# Region colours for the counted strip (name, count, colour).
REGIONS = [
    ("ASIA", 6, (179, 71, 36)),
    ("MIDDLE EAST", 2, (138, 109, 27)),
    ("EUROPE", 6, (51, 89, 126)),
    ("AFRICA", 1, (47, 107, 51)),
    ("AMERICAS", 21, (107, 78, 142)),
    ("OCEANIA", 1, (31, 110, 110)),
    ("GLOBAL", 7, (85, 85, 85)),
]

# The three leads: (panel key, kicker, kicker colour, headline, deck).
# Panel art is drawn by draw_lead_* below.
LEADS = [
    ("summit", "SUMMIT — FIRST US-CHINA-RUSSIA TRILATERAL", ACCENT,
     "Trump, Xi and Putin hold first three-way summit",
     "Ninety minutes, one table, a four-point 'Declaration toward "
     "Peace': 'a nuclear war cannot be won' — plus UN reform, fuel "
     "supply, ICC limits."),
    ("icj", "THE HAGUE · JUSTICE", STEEL,
     "World Court finds Myanmar guilty of genocide",
     "9 of 15 judges find for The Gambia — a first for the court."),
    ("anthropic", "NEW YORK · MARKETS", OCHRE,
     "Anthropic debuts with record $81.3bn IPO",
     "Opened $111.50, closed $97.17, up 17% on $83. Raised $81.3bn."),
]

# Grid (12): (band colour, pictogram key, band mark, kicker, headline, deck)
# The band mark is a short white word/number drawn at the band's right.
GRID = [
    (WINE, "gamepad", "VI", "WORLDWIDE · GAMES",
     "GTA VI launches on PS5 and Xbox",
     "Midnight launch. 99 on Metacritic."),
    (STEEL, "globe", "21", "WORLD · APEC",
     "APEC adopts Shenzhen Outlook",
     "21 economies back the plan."),
    (STEEL, "bridge", "", "WORLD · CRIMEA",
     "Ukraine hits Crimea Bridge for a third time",
     "Neptune missiles halt trains."),
    (STEEL, "shield", "", "WORLD · GAZA",
     "Gaza raid ends after a day",
     "About 6,000 people fled."),
    (STEEL, "globe", "", "WORLD · ANTALYA",
     "COP31 draft drops fossil fuels",
     "Slim text cuts $120bn aid goal."),
    (STEEL, "globe", "5", "WORLD · BOGOTÁ",
     "Colombia unions strike nationwide over tax",
     "Marches in five cities over tax bill."),
    (SKY, "cyclone", "95", "WEATHER · INDIA",
     "Cyclone Akvan nears India's coast",
     "95 km/h; 300,000+ evacuated."),
    (OCHRE, "chart-down", "-1,101", "BUSINESS · MARKETS",
     "Dow drops 1,101 points, ends below 50,000",
     "Sixth straight day of losses."),
    (OCHRE, "bitcoin", "", "BUSINESS · CRYPTO",
     "Bitcoin sinks below $62,000",
     "Lowest since July: $61,353."),
    (TEAL, "satellite", "", "SCIENCE · SPACE",
     "Voyager 1 confirmed one light-day from Earth",
     "25.9bn km; signals take a day."),
    (GREEN, "ball", "26-3", "SPORT · NFL",
     "Texans crush Colts 26-3",
     "Colts scoreless after the first."),
    (GREEN, "trophy", "", "SPORT · WNBA",
     "Valkyries sweep Aces to first WNBA Finals",
     "Golden State wins 87-77 in OT."),
]

# Numbered briefs (29): (place, headline). Numbers 1-29 are printed in
# the list and, for the first brief at each distinct place, on the map
# (see PINS). Briefs 13, 21, 22, 27 have no single place at all.
BRIEFS = [
    ("WASHINGTON", "Senate rejects Iran war curb, 48-51"),
    ("GULF", "Third US carrier reaches the Gulf"),
    ("LONDON", "UK forced to admit Apple backdoor order"),
    ("WASHINGTON", "White House cyber chief fired"),
    ("TOKYO", "Japan core inflation up 2.2%"),
    ("CANBERRA", "Australia jobless rate hits 2021 high"),
    ("LONDON", "Copper lowest since April ($12,471/t)"),
    ("NEW YORK", "Wall Street's $500bn Nvidia pledge unspent"),
    ("NEW YORK", "Moody's: US grew faster than expected (2.3%)"),
    ("CALIFORNIA", "AMD falls 8% on short-seller doubts"),
    ("NEW YORK", "Hackers leak JPMorgan clients' data"),
    ("CHICAGO", "China team wins Gordon Bell (1.456 exaflops)"),
    ("SPACE", "Pulsar hunt runs a million times faster"),
    ("SAN ANTONIO", "Wemby's 32 lifts Spurs past Clippers"),
    ("MEMPHIS", "Grizzlies rout Warriors; Knicks edge Wolves"),
    ("TORONTO", "Kings edge Leafs 4-3 in shootout"),
    ("L.A.", "Skydance merges Warner Bros, Paramount TV"),
    ("LIVERPOOL", "Beatles release new 'In My Life' video"),
    ("NEW ORLEANS", "Jazz Fest 2027 names its headliners"),
    ("MUMBAI", "Ramayana passes 1,547 crore worldwide"),
    ("ENGLAND", "Patrick Stewart cremated using water"),
    ("MARKETS", "Gold down ~2% to ~$3,667/oz"),
    ("PRETORIA", "South Africa holds rate at 7.25%"),
    ("CHICAGO", "Goolsbee won't rule out bigger hikes"),
    ("HORMUZ", "IEA: Iran war may cut Hormuz reliance"),
    ("NEW YORK", "Warner Music's first $2bn quarter"),
    ("GLOBAL", "GTA pre-orders ~$1.54bn (Sensor Tower, 17 Nov)"),
    ("WASHINGTON", "US jobless claims jump unexpectedly"),
    ("OTTAWA", "Canada eases rules for small banks"),
]

# Map pins: (brief number, map-local x, map-local y). The map box is
# 330x175; positions are approximate (see the legend under the map).
# One pin per distinct place — the first brief for that place; briefs 4,
# 7, 9, 11, 13, 21, 22, 24, 26, 27, 28 share a place (or have none) and
# have no pin of their own, so the pins stay readable instead of merging
# into one red blob over the US east coast. Pins are spaced so no two
# 12px pin circles touch (the renderer asserts this).
PINS = [
    (1, 82, 52), (2, 226, 52), (3, 174, 32),
    (5, 306, 44), (6, 304, 148), (8, 90, 40),
    (10, 24, 40), (12, 64, 38),
    (14, 56, 70), (15, 68, 60), (16, 76, 30), (17, 30, 56),
    (18, 158, 22), (19, 70, 78), (20, 252, 74), (23, 196, 116),
    (25, 242, 64), (29, 88, 20),
]

# The day in numbers: (big figure, label) — all from stories on this page.
NUMBERS = [
    ("$81.3bn", "Anthropic IPO — biggest ever"),
    ("-1,101", "Dow points, first close below 50,000 since June"),
    ("~$61,353", "Bitcoin low, weakest since July"),
    ("9 of 15", "ICJ judges find Myanmar guilty"),
    ("95 km/h", "Cyclone Akvan; 300,000+ evacuated"),
    ("25.9bn km", "Voyager 1 — one light-day out"),
]

# DATE CHECK footer: items left out on purpose because they are other
# days' news (all from the research files).
DATE_CHECK = (
    "DATE CHECK — LEFT OUT ON PURPOSE, NOT 19 NOV: EU's €45bn Ukraine "
    "loan (proposed 18 Nov) · Van Gogh's $190.4m sale (18 Nov) · the "
    "Xi–Trump tarmac hug (18 Nov) · the Kuwait strikes (17–18 Nov) · "
    "the Gaza raid's start (18 Nov; its end is on this page) · Voyager "
    "crossing one light-day (18 Nov; NASA confirmed it 19 Nov) · "
    "COP31's scheduled close (20 Nov) · Cyclone Akvan's landfall "
    "(20 Nov). All other stories happened, or were first reported, on "
    "Thursday 19 November 2026."
)


def draw_flag_us(d, x, y, w, h):
    """Flat US flag: stripes + blue canton with a dot grid for stars."""
    stripe = h / 13
    for i in range(13):
        col = (178, 34, 52) if i % 2 == 0 else WHITE
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=col)
    cw, ch = w * 0.4, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            cx = x + 5 + c * (cw - 8) / 4
            cy = y + 4 + r * (ch - 7) / 3
            d.ellipse([cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5], fill=WHITE)


def draw_flag_cn(d, x, y, w, h):
    """Flat China flag: red field, one large + four small yellow stars."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    cx, cy = x + w * 0.22, y + h * 0.3
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 222, 0))
    for sx, sy in [(0.52, 0.12), (0.62, 0.28), (0.6, 0.5), (0.5, 0.62)]:
        px, py = x + w * sx, y + h * sy
        d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=(255, 222, 0))


def draw_flag_ru(d, x, y, w, h):
    """Flat Russia flag: white / blue / red horizontal tricolour."""
    for i, col in enumerate([WHITE, (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)


def draw_lead_summit(d, x, y, w, h):
    """Flat Shenzhen scene, 309x96: sky, skyline, three flags, table.

    The three leaders are abstract silhouettes — circle head, trapezoid
    shoulders, no facial features — named only by their plates and flags.
    """
    d.rectangle([x, y, x + w, y + h], fill=(220, 233, 242))
    # sun: one flat disc
    d.ellipse([x + w - 40, y + 6, x + w - 14, y + 32], fill=(242, 208, 107))
    # skyline: flat dark blocks with small lit windows, baseline y+h-34.
    # Tops stay at or below y+30 so the flags (y+4..y+28) stay visible.
    base = y + h - 34
    skyline = [(0, 34, 34), (38, 32, 30), (72, 40, 28), (104, 30, 34),
               (142, 34, 30), (176, 30, 32), (212, 36, 28), (244, 32, 30),
               (278, 38, 31)]
    for bx, by, bw in skyline:
        d.rectangle([x + bx, y + by, x + bx + bw, base], fill=(46, 58, 74))
        for wy in range(by + 8, base - y - 6, 12):
            for wx in range(bx + 6, bx + bw - 5, 11):
                d.rectangle([x + wx, y + wy, x + wx + 3, y + wy + 4],
                            fill=(242, 208, 107))
    # ground band
    d.rectangle([x, base, x + w, y + h], fill=(46, 58, 74))
    # three flag poles
    for fx, fn in ((38, draw_flag_us), (130, draw_flag_cn),
                   (222, draw_flag_ru)):
        d.line([x + fx, y + 2, x + fx, y + 30], fill=INK, width=2)
        fn(d, x + fx + 2, y + 4, 40, 24)
    # three abstract silhouettes behind the table
    for cx in (60, 152, 244):
        d.ellipse([x + cx - 10, y + 30, x + cx + 10, y + 50],
                  fill=(31, 42, 58))
        d.polygon([(x + cx - 19, base), (x + cx + 19, base),
                   (x + cx + 11, y + 46), (x + cx - 11, y + 46)],
                  fill=(31, 42, 58))
    # table
    d.rectangle([x + 12, base, x + w - 12, y + h - 12], fill=(122, 74, 43))
    d.rectangle([x + 12, base, x + w - 12, base + 5], fill=(150, 98, 60))
    # name plates
    for cx, name in ((60, "TRUMP"), (152, "XI"), (244, "PUTIN")):
        d.rectangle([x + cx - 23, y + h - 22, x + cx + 23, y + h - 11],
                    fill=CREAM)
        tw = text_w(d, name, F_BOLD(8))
        d.text((x + cx - tw // 2, y + h - 21), name, font=F_BOLD(8),
               fill=INK)


def draw_lead_icj(d, x, y, w, h):
    """Flat World Court scene, 309x96: brick courthouse, gold scales,
    red 9-6 vote badge. The 9-6 split is the 9-of-15 verdict."""
    d.rectangle([x, y, x + w, y + h], fill=(228, 233, 238))
    # courthouse: pediment, brick body, white columns, steps
    d.polygon([(x + 10, y + 30), (x + 150, y + 30), (x + 80, y + 10)],
              fill=(172, 74, 52))
    d.rectangle([x + 10, y + 30, x + 150, y + h - 8], fill=(186, 92, 66))
    d.rectangle([x + 72, y + 60, x + 88, y + h - 8], fill=(60, 48, 40))
    for cx in (22, 48, 104, 130):
        d.rectangle([x + cx, y + 34, x + cx + 8, y + h - 12], fill=CREAM)
    d.rectangle([x + 10, y + h - 12, x + 150, y + h - 8], fill=CREAM)
    for i, sw in enumerate((164, 156, 148)):
        d.rectangle([x + 80 - sw // 2, y + h - 8 + i * 3,
                     x + 80 + sw // 2, y + h - 6 + i * 3],
                    fill=(120, 110, 96))
    # scales of justice, gold
    gold = (201, 162, 39)
    d.line([x + 205, y + 22, x + 205, y + h - 12], fill=gold, width=3)
    d.ellipse([x + 201, y + 16, x + 209, y + 24], fill=gold)
    d.line([x + 172, y + 30, x + 238, y + 30], fill=gold, width=3)
    d.line([x + 172, y + 30, x + 164, y + 52], fill=gold, width=2)
    d.line([x + 172, y + 30, x + 180, y + 52], fill=gold, width=2)
    d.line([x + 238, y + 30, x + 230, y + 52], fill=gold, width=2)
    d.line([x + 238, y + 30, x + 246, y + 52], fill=gold, width=2)
    d.polygon([(x + 158, y + 52), (x + 186, y + 52), (x + 172, y + 62)],
              fill=gold)
    d.polygon([(x + 224, y + 52), (x + 252, y + 52), (x + 238, y + 62)],
              fill=gold)
    d.rectangle([x + 196, y + h - 12, x + 214, y + h - 6], fill=gold)
    # vote badge, top right
    d.rounded_rectangle([x + w - 66, y + 6, x + w - 8, y + 32], radius=4,
                        fill=ACCENT)
    badge = "9–6"
    bw = text_w(d, badge, F_BLACK(17))
    d.text((x + w - 37 - bw // 2, y + 9), badge, font=F_BLACK(17),
           fill=WHITE)


def draw_lead_anthropic(d, x, y, w, h):
    """Flat NASDAQ debut, 309x96: dark-green board, rising candlesticks,
    ANT label, IPO $83 tag, $97.17 close."""
    d.rectangle([x, y, x + w, y + h], fill=(13, 58, 45))
    for gy in (24, 48, 72):
        d.line([x + 8, y + gy, x + w - 8, y + gy], fill=(30, 90, 70),
               width=1)
    # candlesticks, trending up left to right: (x0, top, bottom, up?)
    candles = [(150, 62, 78, False), (172, 56, 70, True),
               (194, 44, 62, True), (216, 50, 60, False),
               (238, 34, 52, True), (260, 26, 44, True),
               (282, 18, 36, True)]
    closes = []
    for cx0, top, bot, up in candles:
        col = (74, 222, 128) if up else (231, 76, 60)
        mid = (top + bot) // 2
        d.line([x + cx0 + 5, y + top - 6, x + cx0 + 5, y + bot + 6],
               fill=col, width=2)
        d.rectangle([x + cx0, y + top, x + cx0 + 10, y + bot], fill=col)
        closes.append((x + cx0 + 5, y + mid))
    # yellow trend line through the closes
    d.line(closes, fill=(242, 208, 107), width=2, joint="curve")
    d.text((x + 10, y + 8), "ANT", font=F_BLACK(26), fill=WHITE)
    d.text((x + 10, y + 38), "NASDAQ · FIRST DAY", font=F_BOLD(9),
           fill=(150, 220, 150))
    d.rectangle([x + 10, y + h - 30, x + 76, y + h - 10], fill=(9, 40, 31))
    d.text((x + 16, y + h - 26), "IPO $83", font=F_BOLD(11), fill=WHITE)
    close = "$97.17"
    cw = text_w(d, close, F_BLACK(16))
    d.text((x + w - cw - 10, y + h - 28), close, font=F_BLACK(16),
           fill=WHITE)


def draw_map(d, x, y, w, h):
    """Schematic world map, 330x175: flat tan continents on pale ocean,
    numbered red pins tied to the briefs list. Positions approximate."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 231, 240))
    land = (232, 220, 184)
    edge = (200, 186, 140)
    continents = [
        # North America
        [(14, 30), (40, 14), (70, 10), (100, 16), (118, 26), (108, 40),
         (98, 44), (92, 58), (80, 66), (66, 86), (56, 78), (48, 64),
         (30, 56), (16, 44)],
        # Greenland
        [(104, 6), (122, 4), (128, 12), (114, 16), (104, 12)],
        # South America
        [(76, 96), (102, 90), (116, 104), (110, 128), (98, 156),
         (88, 142), (78, 118)],
        # Europe
        [(162, 26), (180, 14), (200, 18), (206, 30), (196, 42),
         (180, 48), (168, 40)],
        # UK
        [(158, 24), (164, 20), (166, 28), (160, 30)],
        # Africa
        [(166, 60), (192, 54), (212, 64), (210, 88), (200, 118),
         (188, 108), (176, 84)],
        # Asia
        [(212, 18), (258, 8), (306, 16), (322, 32), (300, 50),
         (282, 64), (264, 56), (246, 44), (224, 34)],
        # India
        [(250, 58), (262, 60), (258, 88), (248, 84)],
        # Japan
        [(308, 28), (314, 26), (316, 40), (310, 44)],
        # Australia
        [(272, 128), (300, 124), (310, 136), (296, 150), (276, 144)],
    ]
    for poly in continents:
        pts = [(x + px, y + py) for px, py in poly]
        d.polygon(pts, fill=land, outline=edge)
    # SE Asia islands: three small dots
    for ix, iy in ((282, 78), (292, 84), (276, 88)):
        d.ellipse([x + ix - 3, y + iy - 2, x + ix + 3, y + iy + 2],
                  fill=land, outline=edge)
    # numbered pins
    for num, px, py in PINS:
        d.ellipse([x + px - 6, y + py - 6, x + px + 6, y + py + 6],
                  fill=ACCENT, outline=WHITE, width=1)
        label = str(num)
        lw = text_w(d, label, F_BOLD(8))
        d.text((x + px - lw // 2, y + py - 5), label, font=F_BOLD(8),
               fill=WHITE)


LEAD_DRAW = {"summit": draw_lead_summit, "icj": draw_lead_icj,
             "anthropic": draw_lead_anthropic}


def main():
    # ---- story-count honesty checks (masthead, strip, footer must agree)
    assert len(LEADS) + len(GRID) + len(BRIEFS) == 44, (
        f"story total {len(LEADS) + len(GRID) + len(BRIEFS)} != 44")
    assert sum(n for _, n, _ in REGIONS) == 44, (
        f"region counts sum to {sum(n for _, n, _ in REGIONS)} != 44")
    assert {n for n, _, _ in PINS} == {1, 2, 3, 5, 6, 8, 10, 12, 14, 15,
                                        16, 17, 18, 19, 20, 23, 25, 29}, (
        "map pins must be one per distinct brief place")
    for i, (n1, x1, y1) in enumerate(PINS):
        for n2, x2, y2 in PINS[i + 1:]:
            assert (x1 - x2) ** 2 + (y1 - y2) ** 2 > 12 ** 2, (
                f"map pins {n1} and {n2} touch")

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    y = 8
    tracked(d, M, y, "THE WORLD IN ONE DAY", F_BOLD(13), ACCENT, tracking=3)
    right = "44 STORIES · EVERY CONTINENT"
    tracked(d, W - M - tracked_w(d, right, F_BOLD(13), 3), y, right,
            F_BOLD(13), GREY, tracking=3)
    y = 24
    title = "Thursday 19 November 2026"
    assert text_w(d, title, F_SERIF(54)) <= CW, "masthead title too wide"
    d.text((M, y), title, font=F_SERIF(54), fill=INK)
    y = 86
    sub = ("Three leaders meet in Shenzhen · The World Court finds Myanmar "
           "guilty · The biggest IPO ever debuts")
    assert text_w(d, sub, F_SERIF_IT(16)) <= CW, "masthead subline too wide"
    d.text((M, y), sub, font=F_SERIF_IT(16), fill=ACCENT)
    d.line([M, 108, W - M, 108], fill=INK, width=3)
    d.line([M, 112, W - M, 112], fill=INK, width=1)

    # ---- region-counted strip ------------------------------------------
    y = 118
    seg_w = CW // len(REGIONS)
    for i, (name, count, colour) in enumerate(REGIONS):
        sx = M + i * seg_w
        d.rectangle([sx, y, sx + seg_w - 1, y + 19], fill=colour)
        label = f"{name} {count}"
        lw = text_w(d, label, F_BOLD(11))
        assert lw <= seg_w - 6, f"region label too wide: {label}"
        d.text((sx + (seg_w - lw) // 2, y + 4), label, font=F_BOLD(11),
               fill=WHITE)

    # ---- the day in numbers --------------------------------------------
    y = 141
    cell_w = (CW - 5 * 10) // 6
    for i, (num, label) in enumerate(NUMBERS):
        cx = M + i * (cell_w + 10)
        assert text_w(d, num, F_XBOLD(18)) <= cell_w, f"number too wide: {num}"
        d.text((cx, y), num, font=F_XBOLD(18), fill=ACCENT if i == 0 else INK)
        ly = y + 22
        for line in wrap_strict(d, label, F_REG(10), cell_w, 2,
                                f"number label {num}"):
            d.text((cx, ly), line, font=F_REG(10), fill=BODY)
            ly += 12
        if i < 5:
            d.line([cx + cell_w + 5, y + 2, cx + cell_w + 5, y + 42],
                   fill=RULE, width=1)
    d.line([M, 189, W - M, 189], fill=INK, width=2)

    # ---- three illustrated leads ---------------------------------------
    y0 = 195
    panel_h = 110
    col_w = (CW - 2 * 12) // 3
    for i, (key, kicker, colour, head, deck_s) in enumerate(LEADS):
        cx = M + i * (col_w + 12)
        LEAD_DRAW[key](d, cx, y0, col_w, panel_h)
        d.rectangle([cx, y0, cx + col_w, y0 + panel_h], outline=INK, width=2)
        ky = y0 + panel_h + 6
        tracked(d, cx, ky, kicker, F_BOLD(11), colour, tracking=1)
        hy = ky + 15
        hlines = wrap_strict(d, head, F_XBOLD(17), col_w, 2,
                             f"lead headline {i}")
        assert len(hlines[-1].split()) > 1, (
            f"lead headline {i} ends with an orphan word: {head!r}")
        for line in hlines:
            d.text((cx, hy), line, font=F_XBOLD(17), fill=INK)
            hy += 20
        dy = hy + 4
        for line in wrap_strict(d, deck_s, F_REG(12), col_w, 3,
                                f"lead deck {i}"):
            d.text((cx, dy), line, font=F_REG(12), fill=BODY)
            dy += 14
        assert dy <= y0 + panel_h + 108, f"lead {i} overflow: {dy}"
    d.line([M, 419, W - M, 419], fill=INK, width=2)

    # ---- story grid: 4 columns x 3 rows, 12 items ----------------------
    y0 = 425
    cols, rows = 4, 3
    gap_x, gap_y = 12, 8
    cell_w = (CW - (cols - 1) * gap_x) // cols
    cell_h = 94
    band_h = 38
    assert len(GRID) == 12, f"grid must hold 12 items, has {len(GRID)}"
    for idx, (colour, key, mark, kicker, head, deck_s) in enumerate(GRID):
        r, c = divmod(idx, cols)
        cx = M + c * (cell_w + gap_x)
        cy = y0 + r * (cell_h + gap_y)
        d.rectangle([cx, cy, cx + cell_w, cy + band_h], fill=colour)
        picto_scaled(img, cx + 4, cy + 3, 32, colour, key)
        if mark:
            mw = text_w(d, mark, F_BLACK(20))
            d.text((cx + cell_w - mw - 8, cy + 8), mark, font=F_BLACK(20),
                   fill=WHITE)
        tracked(d, cx, cy + band_h + 4, kicker, F_BOLD(10), colour,
                tracking=1)
        hy = cy + band_h + 16
        hlines = wrap_strict(d, head, F_XBOLD(13), cell_w, 2,
                             f"grid headline {idx}")
        assert len(hlines[-1].split()) > 1, (
            f"grid headline {idx} ends with an orphan word: {head!r}")
        for line in hlines:
            d.text((cx, hy), line, font=F_XBOLD(13), fill=INK)
            hy += 14
        dlines = wrap_strict(d, deck_s, F_REG(11), cell_w, 1,
                             f"grid deck {idx}")
        d.text((cx, hy), dlines[0], font=F_REG(11), fill=BODY)
        assert hy + 11 <= cy + cell_h, f"grid item {idx} overflow"
    grid_end = y0 + rows * cell_h + (rows - 1) * gap_y
    assert grid_end <= 723, f"grid overflow: {grid_end}"
    d.line([M, 729, W - M, 729], fill=INK, width=2)

    # ---- map + numbered briefs -----------------------------------------
    y = 735
    tracked(d, M, y, "WHERE IT HAPPENED", F_BOLD(12), ACCENT, tracking=2)
    briefs_x = M + 330 + 16
    tracked(d, briefs_x, y, "ALSO ON THURSDAY 19 NOVEMBER 2026",
            F_BOLD(12), ACCENT, tracking=2)
    map_y = 751
    map_w, map_h = 330, 175
    draw_map(d, M, map_y, map_w, map_h)
    d.rectangle([M, map_y, M + map_w, map_y + map_h], outline=INK, width=2)
    legend = ("One pin per place — first brief for that place; "
              "positions approximate.")
    assert text_w(d, legend, F_REG(9)) <= map_w, "map legend too wide"
    d.text((M, map_y + map_h + 3), legend, font=F_REG(9), fill=GREY)
    col_w = (W - M - briefs_x - 12) // 2
    assert len(BRIEFS) == 29, f"briefs must be 29, have {len(BRIEFS)}"
    for idx, (place, head) in enumerate(BRIEFS):
        col, row = divmod(idx, 15)
        bx = briefs_x + col * (col_w + 12)
        by = map_y + row * 12.5
        num = str(idx + 1)
        nw = text_w(d, num, F_BOLD(10))
        rest = f"{place} — {head}"
        assert nw + 4 + text_w(d, rest, F_REG(10)) <= col_w, (
            f"brief {idx + 1} too wide: {num} {rest!r}")
        d.text((bx, by), num, font=F_BOLD(10), fill=ACCENT)
        d.text((bx + nw + 4, by), f"{place} — {head}", font=F_REG(10),
               fill=BODY)
    assert map_y + 14 * 12.5 + 10 <= 938, "briefs overflow"

    # ---- date check ----------------------------------------------------
    y = 944
    d.rectangle([M, y, W - M, y + 54], outline=ACCENT, width=2)
    dy = y + 7
    for line in wrap_strict(d, DATE_CHECK, F_REG(11), CW - 20, 3,
                            "date check"):
        d.text((M + 10, dy), line, font=F_REG(11), fill=BODY)
        dy += 14
    assert dy <= y + 54, f"date check overflow: {dy}"

    # ---- sources -------------------------------------------------------
    src = ("Sources: Reuters, AP, BBC, AFP, AnewZ, TechCrunch, "
           "Morningstar / Dow Jones, IMD, NASA, ICJ, Flashscore — 19 Nov "
           "2026. All pictures drawn in code; map positions approximate.")
    assert text_w(d, src, F_REG(10)) <= CW, "sources line too wide"
    d.text((M, 1004), src, font=F_REG(10), fill=GREY)

    img.save(OUT, format="PNG")
    print(f"saved {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()



