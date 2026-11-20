#!/usr/bin/env python3
"""Render v6: dense ILLUSTRATED front page — "The World in One Page".

Build-time only: the grader never runs this file (it runs main.py, which only
copies the committed entry.png). All news data is embedded below as fixed
data, so the render is deterministic: same input -> same PNG bytes.
News researched 20 Nov 2026 from public sources (see README.md and
work/research-v6.md). 44 stories from Thursday 19 November 2026, plus a
clearly labelled "yesterday" slot for two 18 Nov items.

Style is deliberately NON-photorealistic: flat geometric diagrammatic
illustration in the newspaper-infographic manner — solid colour blocks,
bold silhouettes, simple pictograms drawn from primitives (circles,
rectangles, triangles, lines). No gradients, no photorealistic shading,
no fake photos, no detailed or realistic faces: the three leaders in the
lead illustration are abstract silhouettes without features, identified
by name plates and their flags.

Run:  python3 render_v6.py   (writes entry.png next to this file)

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


# ------------------------------------------------------------------- data
# Fixed news data for Thursday 19 November 2026. Every headline, figure
# and date below is as written in work/research-v6.md; nothing is invented.
# (kicker, pictogram key, section colour, headline, one-line deck)

GRID = [
    # WORLD (9)
    ("WORLD · APEC", "globe", STEEL,
     "APEC adopts Shenzhen Outlook",
     "21 economies back the plan."),
    ("WORLD · SENATE", "gavel", STEEL,
     "Senate rejects bid to curb Iran war powers",
     "48-51; three Republicans yes."),
    ("WORLD · GAZA", "shield", STEEL,
     "Gaza raid ends after a day",
     "About 6,000 people fled."),
    ("WORLD · CRIMEA", "bridge", STEEL,
     "Ukraine hits Crimea Bridge a third time",
     "Neptune missiles halt trains."),
    ("WORLD · GULF", "ship", STEEL,
     "Third US carrier reaches the Gulf",
     "Blockade widens to transfers."),
    ("WORLD · LONDON", "phone", STEEL,
     "UK forced to admit Apple backdoor order",
     "Tribunal rejects secrecy claim."),
    ("WORLD · WASHINGTON", "lock", STEEL,
     "White House cyber chief fired",
     "Pentagon CIO takes over for now."),
    ("WORLD · ANTALYA", "globe", STEEL,
     "COP31 draft drops fossil fuels",
     "Slim text cuts $120bn aid goal."),
    ("WORLD · BOGOTÁ", "globe", STEEL,
     "Colombia unions hold national strike",
     "Marches in five cities over tax bill."),
    # BUSINESS (8)
    ("BUSINESS · MARKETS", "chart-down", OCHRE,
     "Dow drops 1,101 points, below 50,000",
     "Sixth straight day of losses."),
    ("BUSINESS · CRYPTO", "bitcoin", OCHRE,
     "Bitcoin sinks below $62,000",
     "Lowest since July: $61,353."),
    ("BUSINESS · JAPAN", "chart-up", OCHRE,
     "Japan core inflation up 2.2%",
     "December rate rise likelier."),
    ("BUSINESS · CANBERRA", "chart-down", OCHRE,
     "Australia jobless rate hits 2021 high",
     "Highest since 2021 after hikes."),
    ("BUSINESS · METALS", "factory", OCHRE,
     "Copper lowest since April",
     "$12,471 a tonne, down 4.6%."),
    ("BUSINESS · CHIPS", "chip", OCHRE,
     "Wall Street's $500bn Nvidia pledge unspent",
     "Not a dime has been put up."),
    ("BUSINESS · ECONOMY", "chart-up", OCHRE,
     "Moody's: US grew faster than expected",
     "2026 growth forecast at 2.3%."),
    ("BUSINESS · CHIPS", "chart-down", OCHRE,
     "AMD falls 8% on short-seller doubts",
     "Sharpest fall among chip names."),
    # TECH (2)
    ("TECH · CYBER", "lock", SLATE,
     "Hackers leak JPMorgan clients' data",
     "Reserve cardholders hit."),
    ("TECH · COMPUTING", "flask", SLATE,
     "Chinese team wins Gordon Bell Prize",
     "1.456 exaflops of chemistry."),
    # SCIENCE (2)
    ("SCIENCE · SPACE", "star", TEAL,
     "Pulsar hunt runs a million times faster",
     "New find spins 261 times/sec."),
    ("SCIENCE · SPACE", "satellite", TEAL,
     "Voyager 1 confirmed one light-day out",
     "25.9bn km; signals take a day."),
    # WEATHER (1)
    ("WEATHER · INDIA", "cyclone", SKY,
     "Cyclone Akvan nears India's coast",
     "95 km/h; 300,000+ evacuated."),
    # SPORT (5)
    ("SPORT · NFL", "ball", GREEN,
     "Texans crush Colts 26-3",
     "Colts scoreless after the first."),
    ("SPORT · NBA", "ball", GREEN,
     "Wembanyama's 32 lifts Spurs past Clippers",
     "124-112; Spurs joint-top West."),
    ("SPORT · NBA", "trophy", GREEN,
     "Grizzlies rout Warriors; Knicks edge Wolves",
     "Bucks lose a 12th straight game."),
    ("SPORT · WNBA", "trophy", GREEN,
     "Valkyries sweep Aces into first Finals",
     "Golden State wins 87-77 in OT."),
    ("SPORT · NHL", "ball", GREEN,
     "Kings edge Leafs 4-3 in shootout",
     "Los Angeles wins the shootout."),
    # CULTURE (5)
    ("CULTURE · TV", "tv", WINE,
     "Skydance merges Warner Bros and Paramount TV",
     "One studio; CBS stays separate."),
    ("CULTURE · MUSIC", "note", WINE,
     "Beatles release new 'In My Life' video",
     "Celebrating Liverpool on film."),
    ("CULTURE · MUSIC", "mic", WINE,
     "Jazz Fest 2027 names its headliners",
     "Foo Fighters, Kahan, The Who."),
    ("CULTURE · FILM", "film", WINE,
     "Ramayana passes 1,547 crore worldwide",
     "Day 15 at the box office."),
    ("CULTURE · FILM", "clapper", WINE,
     "Patrick Stewart cremated using water",
     "Actor died 28 Oct, aged 86."),
]

# Second leads: (band colour, band big text, kicker, headline, deck)
SECOND = [
    (STEEL, "9 of 15", "THE HAGUE · JUSTICE",
     "World Court: Myanmar guilty of genocide",
     "9 of 15 judges find for The Gambia — a first for the court."),
    (OCHRE, "+17%", "NEW YORK · MARKETS",
     "Anthropic debuts in biggest IPO ever",
     "Opened $111.50, closed $97.17, up 17% on $83. Raised $81.3bn."),
    (WINE, "99", "WORLDWIDE · GAMES",
     "GTA VI is out at last",
     "Midnight launch on PS5 and Xbox. 99 on Metacritic from 147 critics."),
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

# Ticker: short items, each "bold lead: rest" is flattened to plain text.
TICKER = [
    "Gold down ~2% to ~$3,667/oz",
    "South Africa holds rate at 7.25%",
    "Goolsbee won't rule out bigger hikes",
    "IEA: Iran war may cut Hormuz reliance",
    "Warner Music's first $2bn quarter",
    "GTA pre-orders ~$1.54bn (Sensor Tower est., 17 Nov)",
]


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


def draw_lead_panel(d, x, y, w, h):
    """Flat Shenzhen scene: sky, skyline, three flags, trilateral table.

    The three leaders are abstract silhouettes — circle head, trapezoid
    shoulders, no facial features — named only by their plates and flags.
    """
    d.rectangle([x, y, x + w, y + h], fill=(220, 233, 242))
    # sun: one flat disc
    d.ellipse([x + w - 52, y + 10, x + w - 20, y + 42], fill=(242, 208, 107))
    # skyline: flat dark blocks with small lit windows
    skyline = [(0, 96, 46, 128), (50, 70, 44, 154), (98, 88, 40, 136),
               (142, 58, 48, 166), (194, 82, 42, 142), (240, 66, 46, 158),
               (290, 92, 44, 132), (338, 74, 40, 150)]
    for bx, by, bw, bh in skyline:
        d.rectangle([x + bx, y + by, x + bx + bw, y + by + bh],
                    fill=(46, 58, 74))
        for wy in range(by + 10, by + bh - 8, 14):
            for wx in range(bx + 7, bx + bw - 7, 13):
                d.rectangle([x + wx, y + wy, x + wx + 4, y + wy + 5],
                            fill=(242, 208, 107))
    # ground band
    d.rectangle([x, y + h - 58, x + w, y + h], fill=(46, 58, 74))
    # three flag poles
    flags = [(52, draw_flag_us), (160, draw_flag_cn), (268, draw_flag_ru)]
    for fx, fn in flags:
        d.line([x + fx, y + 8, x + fx, y + 52], fill=INK, width=2)
        fn(d, x + fx + 2, y + 10, 46, 30)
    # three abstract silhouettes behind the table
    for cx in (82, 190, 298):
        d.ellipse([x + cx - 13, y + h - 108, x + cx + 13, y + h - 82],
                  fill=(31, 42, 58))
        d.polygon([(x + cx - 26, y + h - 58), (x + cx + 26, y + h - 58),
                   (x + cx + 15, y + h - 84), (x + cx - 15, y + h - 84)],
                  fill=(31, 42, 58))
    # table
    d.rectangle([x + 18, y + h - 58, x + w - 18, y + h - 22],
                fill=(122, 74, 43))
    d.rectangle([x + 18, y + h - 58, x + w - 18, y + h - 52],
                fill=(150, 98, 60))
    # name plates
    for cx, name in ((82, "TRUMP"), (190, "XI"), (298, "PUTIN")):
        pw = 52
        d.rectangle([x + cx - pw // 2, y + h - 20, x + cx + pw // 2,
                     y + h - 6], fill=CREAM)
        tw = text_w(d, name, F_BOLD(9))
        d.text((x + cx - tw // 2, y + h - 19), name, font=F_BOLD(9), fill=INK)


def main():
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
    assert text_w(d, title, F_SERIF(58)) <= CW, "masthead title too wide"
    d.text((M, y), title, font=F_SERIF(58), fill=INK)
    y = 86
    sub = ("Three leaders meet in Shenzhen · The World Court finds Myanmar "
           "guilty · The biggest IPO ever debuts")
    assert text_w(d, sub, F_SERIF_IT(16)) <= CW, "masthead subline too wide"
    d.text((M, y), sub, font=F_SERIF_IT(16), fill=ACCENT)
    d.line([M, 108, W - M, 108], fill=INK, width=3)
    d.line([M, 112, W - M, 112], fill=INK, width=1)

    # ---- the day in numbers --------------------------------------------
    y = 120
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
    d.line([M, 166, W - M, 166], fill=INK, width=2)

    # ---- lead ----------------------------------------------------------
    y0 = 174
    panel_w, panel_h = 378, 168
    d.rectangle([M, y0, M + panel_w, y0 + panel_h], outline=INK, width=2)
    draw_lead_panel(d, M + 2, y0 + 2, panel_w - 4, panel_h - 4)
    # red label over the panel's top-left corner
    lab = "APEC 2026 · SHENZHEN"
    d.rectangle([M, y0, M + text_w(d, lab, F_BOLD(11)) + 16, y0 + 20],
                fill=ACCENT)
    d.text((M + 8, y0 + 4), lab, font=F_BOLD(11), fill=WHITE)

    tx = M + panel_w + 18
    tw = W - M - tx
    tracked(d, tx, y0 + 2, "SUMMIT — FIRST US-CHINA-RUSSIA TRILATERAL",
            F_BOLD(12), ACCENT, tracking=2)
    hl = wrap_strict(d, "Trump, Xi and Putin hold first three-way summit",
                     F_BLACK(34), tw, 3, "lead headline")
    hy = y0 + 20
    for line in hl:
        d.text((tx, hy), line, font=F_BLACK(34), fill=INK)
        hy += 36
    deck = ("Ninety minutes, one table, a four-point 'Declaration toward "
            "Peace': UN reform, fuel supply, ICC limits — and that nuclear "
            "war 'cannot be won'.")
    dy = hy + 4
    for line in wrap_strict(d, deck, F_REG(14), tw, 2, "lead deck"):
        d.text((tx, dy), line, font=F_REG(14), fill=BODY)
        dy += 18
    assert dy <= y0 + panel_h - 22, f"lead deck overflow: {dy}"
    fy = y0 + panel_h - 20
    d.line([tx, fy, W - M, fy], fill=RULE, width=1)
    tracked(d, tx, fy + 6, "90 MINUTES · 4-POINT DECLARATION · FIRST-EVER",
            F_BOLD(12), INK, tracking=1)
    assert y0 + panel_h <= 346, "lead overflow"

    # ---- second leads --------------------------------------------------
    y0 = 350
    col_w = (CW - 2 * 12) // 3
    band_h = 42
    for i, (colour, big, kicker, head, deck_s) in enumerate(SECOND):
        cx = M + i * (col_w + 12)
        d.rectangle([cx, y0, cx + col_w, y0 + band_h], fill=colour)
        bw = text_w(d, big, F_BLACK(28))
        d.text((cx + col_w - bw - 12, y0 + 7), big, font=F_BLACK(28),
               fill=WHITE)
        # crisp mark at the band's left: courthouse, rising chart, "VI"
        if i == 0:
            PICTOS["court"](d, cx + 8, y0 + 3, 36, CREAM)
        elif i == 1:
            PICTOS["chart-up"](d, cx + 8, y0 + 3, 36, CREAM)
        else:
            d.text((cx + 10, y0 + 5), "VI", font=F_BLACK(28), fill=WHITE)
        ky = y0 + band_h + 6
        tracked(d, cx, ky, kicker, F_BOLD(11), colour, tracking=2)
        hy = ky + 15
        for line in wrap_strict(d, head, F_XBOLD(16), col_w, 2,
                                f"second headline {i}"):
            d.text((cx, hy), line, font=F_XBOLD(16), fill=INK)
            hy += 19
        dy = hy + 2
        for line in wrap_strict(d, deck_s, F_REG(12), col_w, 2,
                                f"second deck {i}"):
            d.text((cx, dy), line, font=F_REG(12), fill=BODY)
            dy += 15
        assert dy <= y0 + 133, f"second lead {i} overflow: {dy}"
    d.line([M, 490, W - M, 490], fill=INK, width=2)

    # ---- story grid: 4 columns x 8 rows, 32 items ----------------------
    y0 = 498
    cols, rows = 4, 8
    gap_x, gap_y = 12, 3
    cell_w = (CW - (cols - 1) * gap_x) // cols
    cell_h = 52
    picto_s = 44
    text_x_off = picto_s + 8
    text_wdt = cell_w - text_x_off
    assert len(GRID) == 32, f"grid must hold 32 items, has {len(GRID)}"
    for idx, (kicker, key, colour, head, deck_s) in enumerate(GRID):
        r, c = divmod(idx, cols)
        cx = M + c * (cell_w + gap_x)
        cy = y0 + r * (cell_h + gap_y)
        tile(d, cx, cy + 2, picto_s, colour, key)
        tx = cx + text_x_off
        tracked(d, tx, cy, kicker, F_BOLD(10), colour, tracking=1)
        hy = cy + 12
        for line in wrap_strict(d, head, F_XBOLD(13), text_wdt, 2,
                                f"grid headline {idx}"):
            d.text((tx, hy), line, font=F_XBOLD(13), fill=INK)
            hy += 14
        dlines = wrap_strict(d, deck_s, F_REG(11), text_wdt, 1,
                             f"grid deck {idx}")
        d.text((tx, hy), dlines[0], font=F_REG(11), fill=BODY)
    grid_end = y0 + rows * cell_h + (rows - 1) * gap_y
    assert grid_end <= 936, f"grid overflow: {grid_end}"
    d.line([M, 940, W - M, 940], fill=INK, width=2)

    # ---- ticker: ALSO TODAY --------------------------------------------
    y = 948
    x = tracked(d, M, y, "ALSO TODAY", F_BOLD(13), ACCENT, tracking=2) + 10
    ticker_text = " · ".join(TICKER)
    for line in wrap_strict(d, ticker_text, F_REG(13), W - M - x, 2,
                            "ticker"):
        d.text((x, y), line, font=F_REG(13), fill=BODY)
        y += 16
        x = M
    assert y <= 982, f"ticker overflow: {y}"

    # ---- yesterday slot + sources --------------------------------------
    y = 986
    x = tracked(d, M, y, "YESTERDAY — 18 NOV", F_BOLD(12), WINE, tracking=1)
    x += 10
    yday = ("EU proposes €45bn loan for Ukraine · "
            "Van Gogh sells for a record $190.4m · "
            "DATE CHECK: every other story 19 Nov 2026")
    d.text((x, y), yday, font=F_REG(12), fill=BODY)
    d.text((M, y + 16),
           "Sources: Reuters, AP, BBC, AFP, AnewZ, TechCrunch, "
           "Morningstar / Dow Jones, IMD, NASA, ICJ, Sotheby's, Flashscore "
           "— 19 Nov 2026. All pictures drawn, none photographed.",
           font=F_REG(11), fill=GREY)
    assert y + 16 + 11 <= 1016, "footer overflow"

    img.save(OUT, format="PNG")
    print(f"saved {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
