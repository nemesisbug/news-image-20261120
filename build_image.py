#!/usr/bin/env python3
"""Draw "The World in One Day" -- Friday 20 November 2026.

A one-page newspaper front page summing up the day's world news in a
single 1024x1024 image. Deterministic: same bytes on every run, no
network, no timestamps, no randomness. Run: python3 build_image.py
writes entry.png next to this file.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (253, 252, 248)
INK = (17, 17, 17)
MUTED = (90, 88, 82)
RED = (178, 28, 28)
NAVY = (26, 48, 80)
TEAL = (14, 94, 98)
GOLD = (168, 124, 18)
LINE = (200, 196, 188)
CARD_BG = (255, 255, 255)
TAG_BG = (238, 234, 226)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
F_SANS = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped paragraph; returns y after the last line."""
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def tag(draw, x, y, label):
    """Small REPORTED / CLAIM / FORECAST tag; returns width used."""
    fnt = F_BOLD(8)
    tw = draw.textlength(label, font=fnt)
    pad = 4
    draw.rounded_rectangle([x, y, x + tw + pad * 2, y + 12], radius=2,
                           fill=TAG_BG, outline=LINE)
    draw.text((x + pad, y + 2), label, font=fnt, fill=MUTED)
    return int(tw + pad * 2 + 5)


# ---------------------------------------------------------------- stories
# (kicker, headline, body, tag, region)
HEROES = [
    ("WASHINGTON - IRAN",
     "Trump puts the Iran call off to 2027",
     "Trump told Axios aboard Air Force One: no decision on strikes until "
     "after Jan 1. He flew home from China.",
     "REPORTED", "MIDDLE EAST"),
    ("ODISHA - CYCLONE AKVAN",
     "Cyclone Akvan bears down on India's east coast",
     "300,000+ evacuated, 423 rescue teams out. Landfall near Gopalpur by "
     "noon; winds 90-100 km/h.",
     "FORECAST", "ASIA-PACIFIC"),
    ("MARKETS - THE SELL-OFF",
     "Stocks slide, Bitcoin hits 9-month low",
     "Wall Street fell 2%+ Thursday; Bitcoin under $62,000, gold at a "
     "14-month low. Asia fell again Friday.",
     "REPORTED", "WORLDWIDE"),
]

CARDS = [
    ("ETHIOPIAN AIRLINES", "Airline discloses a data breach",
     "Ethiopian Airlines warns customers their data may have been exposed "
     "in a cybersecurity breach.",
     "REPORTED", "AFRICA"),
    ("SPACE - JAPAN", "Hayabusa2 gives up its asteroid landing",
     "Engine trouble forces the probe to scrap its landing and rewrite its "
     "mission.", "REPORTED", "ASIA-PACIFIC"),
    ("GAMES", "GTA 6 sales pass Odyssey's $1.8bn",
     "Sensor Tower estimates $1.84bn in sales, passing The Odyssey's total "
     "worldwide box office.", "REPORTED", "WORLDWIDE"),
    ("UKRAINE - EUROPE", "Europe ready to talk with Russia",
     "Leaders signal readiness for talks on ending the war in Ukraine.",
     "REPORTED", "EUROPE"),
    ("KYIV", "Blasts near Austrian, Dutch embassies in Kyiv",
     "Projectiles land near the Austrian and Dutch embassies, causing minor "
     "damage; no staff are hurt.", "REPORTED", "EUROPE"),
    ("BAHRAIN", "Bapco plant nears full restart",
     "The Bapco refinery nears full resumption after six strikes disrupted "
     "operations.", "REPORTED", "MIDDLE EAST"),
    ("SENEGAL", "Dozens missing as migrant boat sinks",
     "A boat carrying migrants sinks off the coast; dozens missing and a "
     "search is under way.", "REPORTED", "AFRICA"),
    ("YEMEN", "\"It's just fireworks,\" say voices inside a besieged city",
     "People inside a besieged Yemeni city tell the BBC how they explain "
     "the shelling to their children.", "REPORTED", "MIDDLE EAST"),
    ("CRYPTO MARKETS", "Polymarket US launches oil, gas contracts",
     "Polymarket US adds short-cycle oil and gas contracts after its crypto "
     "contracts pass $1bn in volume.", "REPORTED", "AMERICAS"),
    ("SEOUL", "Top court partly overturns ex-PM Han's conviction",
     "The court sends the case back for retrial; other findings stand and "
     "Han stays in detention.", "REPORTED", "ASIA-PACIFIC"),
    ("FIJI", "Fiji declares a national disaster as drought bites",
     "A state of disaster over severe drought and water shortages blamed "
     "on El Nino.", "REPORTED", "ASIA-PACIFIC"),
    ("TECH", "Apple is building its own AI agent",
     "Apple is building an AI agent to rival OpenAI and Google, as the "
     "race reaches the iPhone.", "REPORTED", "AMERICAS"),
]

TIMELINE = [
    ("00:00 UTC", "Polymarket US launches oil, gas contracts", "Polymarket"),
    ("00:27 UTC", "Trump: no Iran call until 2027", "Axios"),
    ("00:34 UTC", "Ethiopian Airlines reports data breach", "Airline"),
    ("00:39 UTC", "Bapco plant nears restart after strikes", "Bahrain"),
    ("01:30 UTC", "Hayabusa2 drops asteroid landing", "JAXA"),
    ("01:43 UTC", "Europe ready for Russia talks", "BBC"),
    ("04:56 IST", "Odisha CM: 300,000 evacuated, 47 trains off", "ANI"),
]

STATS = [
    ("$61,995", "Bitcoin, a 9-month low"),
    ("-2.19%", "Dow Jones on Thursday"),
    ("$3,608", "Gold, a 14-month low"),
    ("300,000+", "evacuated ahead of Akvan"),
    ("423", "rescue teams deployed"),
    ("-3%", "Anthropic after hours"),
    ("7", "straight falls for Asia stocks"),
    ("$1.8bn", "GTA 6 passes Odyssey"),
]

ALSO = [
    ("N. KOREA", "Yongbyon enrichment expands, watchdog says.", "REPORTED", "ASIA-PACIFIC"),
    ("UKRAINE", "Crimean Bridge attack disrupts rail traffic.", "REPORTED", "EUROPE"),
    ("WASHINGTON", "US, Venezuela to restore military cooperation.", "REPORTED", "AMERICAS"),
    ("BANGLADESH", "Fire at Yunus home; arson suspected.", "REPORTED", "ASIA-PACIFIC"),
    ("DELHI", "Modi meets Prince and Princess of Wales.", "REPORTED", "ASIA-PACIFIC"),
    ("WELLINGTON", "NZ 243/5, Nicholls 113 not out.", "REPORTED", "ASIA-PACIFIC"),
    ("AI", "Anthropic -3% after hours after a 17% debut surge.", "REPORTED", "AMERICAS"),
    ("BRUSSELS", "NATO chief meets intelligence chiefs.", "REPORTED", "EUROPE"),
    ("BERLIN", "Merz pledges sustained Ukraine support.", "REPORTED", "EUROPE"),
    ("NEW YORK", "Polymarket US launches oil, gas contracts.", "REPORTED", "AMERICAS"),
    ("DEFENCE", "India signs Rs 1,976-cr Barak missile deal.", "REPORTED", "ASIA-PACIFIC"),
    ("UGANDA", "Landslide survivors seek justice at UN.", "REPORTED", "AFRICA"),
    ("WASHINGTON", "Fed's Waller 8:25 ET; Michigan data 10:00 ET.", "FORECAST", "AMERICAS"),
    ("KUALA LUMPUR", "Kossan profit +131% to RM87.4m.", "REPORTED", "ASIA-PACIFIC"),
    ("HOCKEY", "Women's Asian Champions Trophy begins.", "REPORTED", "ASIA-PACIFIC"),
    ("BADMINTON", "India beat Malaysia at Hong Kong Open.", "REPORTED", "ASIA-PACIFIC"),
    ("GULF", "Gulf Railway to link six nations, bypass Hormuz.", "REPORTED", "MIDDLE EAST"),
    ("BRUSSELS", "EU takes Austria to court over arrest warrant.", "REPORTED", "EUROPE"),
    ("DOHA", "Qatar FMs discuss Gulf developments by phone.", "REPORTED", "MIDDLE EAST"),
    ("RIYADH", "Saudi crown prince, CENTCOM chief talk defence.", "REPORTED", "MIDDLE EAST"),
    ("BOGOTA", "Colombia's president courts controversy.", "REPORTED", "AMERICAS"),
    ("BONDS", "10-yr yield eyes 29th close above 5%.", "REPORTED", "AMERICAS"),
]

# ---------------------------------------------------------------- drawing
def draw_icon(draw, x, y, kind, color):
    """52x52 pictogram tile; simple geometric glyphs, no text art."""
    draw.rounded_rectangle([x, y, x + 52, y + 52], radius=6, fill=color)
    cx, cy = x + 26, y + 26
    white = (255, 255, 255)
    if kind == "satellite":  # Voyager / Hayabusa2
        draw.line([x + 12, y + 40, x + 40, y + 12], fill=white, width=3)
        draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=white, width=3)
        draw.line([x + 10, y + 14, x + 20, y + 24], fill=white, width=2)
        draw.line([x + 42, y + 38, x + 32, y + 28], fill=white, width=2)
    elif kind == "asteroid":
        draw.ellipse([cx - 12, cy - 10, cx + 12, cy + 10], outline=white, width=3)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=white)
        draw.line([x + 8, y + 44, x + 22, y + 34], fill=white, width=2)
    elif kind == "star":  # GTA VI
        draw.text((x + 13, y + 12), "VI", font=F_BOLD(22), fill=white)
        draw.polygon([(cx, y + 38), (cx + 3, y + 44), (cx - 3, y + 44)], fill=white)
    elif kind == "talks":
        draw.ellipse([x + 10, y + 14, x + 28, y + 30], outline=white, width=3)
        draw.ellipse([x + 26, y + 22, x + 44, y + 38], outline=white, width=3)
    elif kind == "blast":
        for ang in range(0, 360, 45):
            import math
            r1, r2 = 6, 20
            a = math.radians(ang)
            draw.line([cx, cy, cx + r2 * math.cos(a), cy + r2 * math.sin(a)],
                      fill=white, width=3)
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=white)
    elif kind == "frame":  # Van Gogh
        draw.rectangle([x + 11, y + 12, x + 41, y + 40], outline=white, width=3)
        draw.ellipse([cx - 7, cy - 8, cx + 7, cy + 6], outline=white, width=2)
        draw.line([x + 14, y + 36, x + 38, y + 36], fill=white, width=2)
    elif kind == "boat":
        draw.polygon([(x + 10, y + 28), (x + 42, y + 28), (x + 36, y + 38),
                      (x + 16, y + 38)], fill=white)
        draw.line([cx, y + 12, cx, y + 28], fill=white, width=2)
        draw.polygon([(cx, y + 12), (cx + 12, y + 26), (cx, y + 26)], fill=white)
        draw.line([x + 10, y + 44, x + 42, y + 44], fill=white, width=2)
    elif kind == "city":  # Yemen
        for bx, bh in ((12, 22), (22, 30), (33, 18)):
            draw.rectangle([x + bx, y + 44 - bh, x + bx + 8, y + 44],
                           outline=white, width=2)
        draw.text((x + 12, y + 6), "\u201c \u201d", font=F_BOLD(16), fill=white)
    elif kind == "deal":  # Venezuela
        draw.arc([x + 10, y + 16, x + 30, y + 36], 90, 270, fill=white, width=3)
        draw.arc([x + 22, y + 16, x + 42, y + 36], 270, 90, fill=white, width=3)
        draw.line([x + 14, y + 38, x + 38, y + 38], fill=white, width=2)
    elif kind == "scales":  # Han Duck-soo
        draw.line([cx, y + 10, cx, y + 40], fill=white, width=3)
        draw.line([x + 12, y + 16, x + 40, y + 16], fill=white, width=3)
        draw.line([x + 12, y + 16, x + 8, y + 28], fill=white, width=2)
        draw.line([x + 12, y + 16, x + 16, y + 28], fill=white, width=2)
        draw.line([x + 40, y + 16, x + 36, y + 28], fill=white, width=2)
        draw.line([x + 40, y + 16, x + 44, y + 28], fill=white, width=2)
        draw.line([x + 14, y + 40, x + 38, y + 40], fill=white, width=3)
    elif kind == "wave":  # Fiji
        draw.ellipse([cx - 8, cy - 14, cx + 8, cy + 2], fill=white)
        for yy in (34, 40):
            draw.arc([x + 10, y + yy - 6, x + 42, y + yy + 6], 0, 180,
                     fill=white, width=2)
    elif kind == "lock":  # data breach
        draw.arc([x + 17, y + 12, x + 35, y + 28], 180, 360, fill=white, width=3)
        draw.rounded_rectangle([x + 12, y + 24, x + 40, y + 42], radius=3,
                               outline=white, width=3)
        draw.ellipse([cx - 3, cy + 2, cx + 3, cy + 8], fill=white)
    elif kind == "factory":  # refinery restart
        draw.rectangle([x + 10, y + 26, x + 34, y + 42], outline=white, width=3)
        draw.rectangle([x + 36, y + 14, x + 42, y + 42], outline=white, width=3)
        draw.ellipse([x + 36, y + 8, x + 42, y + 14], outline=white, width=2)
        draw.line([x + 14, y + 34, x + 30, y + 34], fill=white, width=2)
    elif kind == "chart":  # Polymarket
        for bx, bh in ((12, 12), (22, 20), (32, 30)):
            draw.rectangle([x + bx, y + 42 - bh, x + bx + 7, y + 42],
                           fill=white)
        draw.line([x + 10, y + 14, x + 42, y + 12], fill=white, width=2)
    else:  # "ai" fallback
        draw.text((x + 11, y + 13), "AI", font=F_BOLD(22), fill=white)


ICON_KIND = ["lock", "asteroid", "star", "talks", "blast", "factory",
             "boat", "city", "chart", "scales", "wave", "ai"]
ICON_COLORS = [NAVY, TEAL, (90, 40, 90), NAVY, RED, GOLD,
               (20, 90, 120), (120, 60, 20), (30, 90, 40), NAVY,
               TEAL, (40, 40, 90)]


def draw_hero_art(draw, x, y, w, h, which):
    """Flat illustration panel for a hero story."""
    if which == 0:  # Iran decision deferred to 2027
        draw.rectangle([x, y, x + w, y + h], fill=NAVY)
        draw.text((x + 16, y + 14), "2027", font=F_BOLD(44), fill=(255, 255, 255))
        draw.rounded_rectangle([x + 190, y + 18, x + 236, y + 62], radius=6,
                               fill=GOLD)
        draw.rectangle([x + 204, y + 30, x + 210, y + 50], fill=(255, 255, 255))
        draw.rectangle([x + 216, y + 30, x + 222, y + 50], fill=(255, 255, 255))
        draw.text((x + 16, y + 66), "NO DECISION UNTIL AFTER JAN 1",
                  font=F_BOLD(11), fill=(255, 214, 130))
        draw.line([x + 16, y + 88, x + w - 16, y + 88], fill=(120, 140, 170), width=1)
    elif which == 1:  # Cyclone Akvan
        draw.rectangle([x, y, x + w, y + h], fill=TEAL)
        import math
        cx, cy = x + 70, y + 52
        for r in (12, 22, 32):
            draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255), width=4)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
        for i, yy in enumerate((30, 46, 62)):
            x0 = x + 168 + i * 6
            draw.line([(x0, y + yy), (x0 + 26, y + yy - 6), (x0 + 52, y + yy)],
                      fill=(180, 225, 225), width=3, joint="curve")
        draw.text((x + 168, y + 66), "90-100 KM/H", font=F_BOLD(15),
                  fill=(255, 255, 255))
        draw.text((x + 16, y + 84), "LANDFALL BY NOON, NEAR GOPALPUR",
                  font=F_BOLD(10), fill=(200, 235, 235))
    else:  # Markets sell-off
        draw.rectangle([x, y, x + w, y + h], fill=(40, 22, 22))
        pts = [(x + 16, y + 30), (x + 70, y + 42), (x + 120, y + 34),
               (x + 175, y + 58), (x + 230, y + 52), (x + 290, y + 82)]
        draw.line(pts, fill=(255, 90, 90), width=4, joint="curve")
        draw.polygon([(x + 290, y + 82), (x + 272, y + 74), (x + 284, y + 62)],
                     fill=(255, 90, 90))
        draw.ellipse([x + 250, y + 8, x + 292, y + 50], outline=GOLD, width=3)
        draw.text((x + 258, y + 18), "B", font=F_BOLD(20), fill=GOLD)
        draw.text((x + 16, y + 84), "BITCOIN $61,995  ·  DOW -2.19%",
                  font=F_BOLD(10), fill=(255, 200, 200))


# Coarse continent outlines (lon, lat), schematic map only.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 62), (-65, 60), (-55, 52), (-60, 47), (-70, 44), (-75, 38),
     (-80, 32), (-85, 28), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 11), (-62, 10), (-52, 5), (-50, -5), (-35, -8),
     (-40, -20), (-48, -28), (-58, -38), (-65, -45), (-70, -52), (-73, -45),
     (-72, -30), (-78, -15), (-80, -5)],
    [(-18, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (30, -30), (20, -35),
     (15, -27), (12, -18), (12, -5), (8, 4), (-8, 5), (-15, 11)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (30, 60), (28, 65), (25, 70), (18, 70),
     (12, 65), (5, 60), (-5, 50), (-9, 43)],
    [(30, 60), (40, 68), (55, 70), (70, 72), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (160, 55), (142, 50),
     (140, 40), (130, 33), (122, 30), (110, 20), (105, 10), (100, 5),
     (95, 15), (90, 22), (85, 20), (80, 8), (75, 12), (70, 20), (60, 25),
     (52, 28), (45, 30), (40, 36), (35, 36), (30, 42)],
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (147, -39),
     (153, -32), (150, -22), (146, -19), (142, -11), (136, -12), (130, -13),
     (122, -14), (114, -21)],
]

PINS = [
    (1, -77, 39, "Washington"),
    (2, 30.5, 50.4, "Kyiv"),
    (3, 84.9, 19.3, "Gopalpur"),
    (4, -17.4, 14.7, "Dakar"),
    (5, 178.4, -18.1, "Suva"),
    (6, 174.8, -41.3, "Wellington"),
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 240, 244),
                   outline=LINE)
    for poly in CONTINENTS:
        pts = [(x + (lon + 180) / 360 * w, y + (90 - lat) / 180 * h)
               for lon, lat in poly]
        draw.polygon(pts, fill=(190, 200, 195), outline=(120, 130, 125))
    for num, lon, lat, name in PINS:
        px = x + (lon + 180) / 360 * w
        py = y + (90 - lat) / 180 * h
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                     outline=(255, 255, 255), width=2)
        draw.text((px - 3, py - 6), str(num), font=F_BOLD(9),
                  fill=(255, 255, 255))
    return y + h

# ---------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 8  # margin

    # Top rule + masthead
    d.rectangle([0, 0, W, 6], fill=INK)
    d.text((M, 12), "THE WORLD IN ONE DAY", font=F_SERIF(42), fill=INK)
    d.rectangle([W - 218, 10, W - M, 62], outline=INK, width=2)
    d.text((W - 208, 13), "FRIDAY", font=F_BOLD(15), fill=RED)
    d.text((W - 208, 31), "20 NOVEMBER 2026", font=F_BOLD(13), fill=INK)
    d.text((W - 208, 47), "DAY 324 OF 2026", font=F_SANS(10), fill=MUTED)

    # Red subhead: the 3 biggest stories
    sub = ("TRUMP DEFERS IRAN CALL TO 2027  ·  CYCLONE AKVAN BEARS DOWN ON "
           "INDIA  ·  MARKETS SLIDE AS BITCOIN HITS 9-MONTH LOW")
    d.text((M, 70), sub, font=F_BOLD(13), fill=RED)

    # Story-count banner
    regions = {}
    for _, _, _, _, reg in HEROES + CARDS:
        regions[reg] = regions.get(reg, 0) + 1
    # Timeline-only + also-list stories counted separately below.
    # (This edition's timeline items all repeat heroes/cards: none new.)
    extra_regions = {}
    for k, v in extra_regions.items():
        regions[k] = regions.get(k, 0) + v
    also_regions = {}
    for _, _, _, reg in ALSO:
        also_regions[reg] = also_regions.get(reg, 0) + 1
    for k, v in also_regions.items():
        regions[k] = regions.get(k, 0) + v
    total = 3 + 12 + len(ALSO)
    order = ["ASIA-PACIFIC", "EUROPE", "MIDDLE EAST", "AMERICAS", "AFRICA",
             "WORLDWIDE"]
    parts = [f"{r} {regions.get(r, 0)}" for r in order]
    d.rectangle([M, 92, W - M, 114], fill=NAVY)
    d.text((M + 10, 98), f"{total} STORIES FROM 6 REGIONS",
           font=F_BOLD(13), fill=(255, 255, 255))
    d.text((W - M - 10 - d.textlength("  ·  ".join(parts), font=F_SANS(11)),
            99), "  ·  ".join(parts), font=F_SANS(11), fill=(200, 215, 235))

    # Stat strip: 8 numbers
    y0, y1 = 120, 164
    bw = (W - 2 * M - 7 * 6) / 8
    for i, (num, label) in enumerate(STATS):
        bx = M + i * (bw + 6)
        d.rectangle([bx, y0, bx + bw, y1], outline=LINE, fill=CARD_BG)
        d.text((bx + 6, y0 + 5), num, font=F_BOLD(15), fill=RED)
        para(d, bx + 6, y0 + 24, label, F_SANS(8), bw - 12, fill=MUTED,
             leading=10)

    # Day by hours
    d.text((M, 170), "THE DAY BY HOURS", font=F_BOLD(12), fill=INK)
    d.line([M, 186, W - M, 186], fill=LINE, width=1)
    cw = (W - 2 * M) / 7
    for i, (t, what, src) in enumerate(TIMELINE):
        cx = M + i * cw
        d.text((cx + 2, 191), t, font=F_BOLD(9), fill=RED)
        para(d, cx + 2, 203, what, F_SANS(9), cw - 8, leading=11)
        if i:
            d.line([cx, 190, cx, 232], fill=LINE, width=1)
    d.line([M, 236, W - M, 236], fill=INK, width=2)

    # Heroes: 3 columns
    hy, hh = 244, 172
    hw = (W - 2 * M - 2 * 8) / 3
    for i, (kicker, head, body, tg, reg) in enumerate(HEROES):
        hx = M + i * (hw + 8)
        draw_hero_art(d, hx, hy, hw, 96, i)
        yy = hy + 104
        d.text((hx, yy), kicker, font=F_BOLD(9), fill=RED)
        tagw = tag(d, hx + hw - 66, yy - 1, tg)
        yy = para(d, hx, yy + 13, head, F_BOLD(14), hw, leading=15)
        para(d, hx, yy + 2, body, F_SANS(10), hw, leading=11)

    # Secondary cards: 3 cols x 4 rows
    cy0 = 428
    ch = 78
    for idx, (kicker, head, body, tg, reg) in enumerate(CARDS):
        row, col = divmod(idx, 3)
        cx = M + col * (hw + 8)
        cy = cy0 + row * (ch + 2)
        d.rectangle([cx, cy, cx + hw, cy + ch], outline=LINE, fill=CARD_BG)
        draw_icon(d, cx + 6, cy + 6, ICON_KIND[idx], ICON_COLORS[idx])
        tx = cx + 64
        d.text((tx, cy + 5), kicker, font=F_BOLD(8), fill=RED)
        yy = para(d, tx, cy + 17, head, F_BOLD(11), hw - 70, leading=13)
        para(d, tx, yy, body, F_SANS(9), hw - 70, leading=11)
        tag(d, cx + 6, cy + ch - 15, tg)

    # Bottom band
    by0 = 752
    d.line([M, by0 - 6, W - M, by0 - 6], fill=INK, width=2)

    # Map (left)
    mw = 296
    d.text((M, by0), "WHERE IT HAPPENED", font=F_BOLD(11), fill=INK)
    draw_map(d, M, by0 + 18, mw, 148)
    d.text((M, by0 + 170), "1 Washington  2 Kyiv  3 Gopalpur",
           font=F_SANS(9), fill=MUTED)
    d.text((M, by0 + 182), "4 Dakar  5 Suva  6 Wellington",
           font=F_SANS(9), fill=MUTED)

    # Also on this page (middle, two columns)
    ax = M + mw + 12
    aw = 348
    d.text((ax, by0), "ALSO ON THIS PAGE", font=F_BOLD(11), fill=INK)
    col_w = (aw - 8) / 2
    for j, (kicker, text, tg, reg) in enumerate(ALSO):
        col, row = divmod(j, 11)
        xx = ax + col * (col_w + 8)
        yy = by0 + 16 + row * 18
        # First line: kicker + as many words as fit; second line: the rest,
        # wrapped to the column and truncated with an ellipsis if too long.
        kfnt, tfnt = F_BOLD(8), F_SANS(8)
        prefix = f"{kicker} - "
        pw = d.textlength(prefix, font=kfnt)
        words = text.split()
        line1_words = []
        cur = ""
        for w_ in words:
            trial = (cur + " " + w_).strip()
            if d.textlength(trial, font=tfnt) <= col_w - pw or not cur:
                cur = trial
                line1_words.append(w_)
            else:
                break
        line1 = cur
        line2 = " ".join(words[len(line1_words):])
        if d.textlength(line2, font=tfnt) > col_w:
            while line2 and d.textlength(line2 + "...", font=tfnt) > col_w:
                line2 = line2.rsplit(" ", 1)[0]
            line2 += "..."
            print(f"WARNING truncated ALSO item: {kicker}")
        d.text((xx, yy), prefix, font=kfnt, fill=RED)
        d.text((xx + pw, yy), line1, font=tfnt, fill=INK)
        if line2:
            d.text((xx, yy + 8), line2, font=tfnt, fill=INK)

    # Verdict + markets (right)
    rx = ax + aw + 12
    rw = W - M - rx
    d.rectangle([rx, by0, rx + rw, by0 + 96], outline=INK, width=2,
                fill=(255, 248, 235))
    d.text((rx + 8, by0 + 6), "THE VERDICT", font=F_BOLD(11), fill=RED)
    para(d, rx + 8, by0 + 22,
         "Washington hits pause on Iran until 2027. Stocks slide and "
         "Bitcoin hits a nine-month low; India braces for Akvan's landfall.",
         F_SANS(10), rw - 16, leading=12)
    my = by0 + 104
    d.rectangle([rx, my, rx + rw, by0 + 196], outline=LINE, fill=CARD_BG)
    d.text((rx + 8, my + 6), "MARKETS & MONEY", font=F_BOLD(11), fill=INK)
    para(d, rx + 8, my + 22,
         "Bitcoin $61,995 (-1.4%) - S&P 500 7,176 (-2.0%) - Nasdaq -2.3% - "
         "Dow 49,097 (-2.19%) - Gold $3,608 (-2.1%) - Silver $42.52 - Brent "
         "$91.98 - Asia -1%, 7th straight fall - 10-yr yield 5.05% - VIX 28.4",
         F_SANS(10), rw - 16, leading=12)

    # Footer: date check + sources
    fy = 968
    d.line([M, fy, W - M, fy], fill=INK, width=2)
    d.text((M, fy + 4), "DATE CHECK - LEFT OFF, NOT 20 NOVEMBER:",
           font=F_BOLD(9), fill=RED)
    para(d, M, fy + 16,
         "Van Gogh record sale (Wed 18 Nov) - Venezuela military deal "
         "(Wed 18 Nov) - Voyager 1 light-day milestone (Wed 18 Nov) - "
         "Shenzhen trilateral 'peace declaration' (Thu 19 Nov) - ICJ Myanmar "
         "genocide ruling (Thu 19 Nov) - Anthropic IPO pricing $83 "
         "(Wed 18 Nov) - Nvidia Q3 beat (Tue 17 Nov).",
         F_SANS(9), W - 2 * M, leading=10)
    d.text((M, 1006),
           "HOW SURE ARE WE?  REPORTED = confirmed by named sources  ·  "
           "CLAIM = one side says, unverified  ·  FORECAST = schedule or "
           "projection.",
           font=F_SANS(8), fill=MUTED)
    d.text((M, 1015),
           "Stories as reported by Friday morning, 20 November 2026. "
           "Disputed claims are attributed, not stated as fact. Sources: "
           "Reuters, AP, AFP, BBC, The Hindu, Axios, Yonhap, Antara, IMD.",
           font=F_SANS(8), fill=MUTED)

    img.save(OUT, optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    build()
