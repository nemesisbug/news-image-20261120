# The World in One Day — 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/nemesisbug/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/nemesisbug/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Entry for [make.fun's "Sum up 20 November's world news in one image"](https://make.fun/bounty/news-image-20261120) bounty ($250 in USDC, top 50 paid).

A one-page newspaper front page that sums up the world's news of
**Friday 20 November 2026** in a single image. Every story on the page
happened, or was first reported, on that day.

## What the image shows

- **Masthead** — the paper's name and the date, front and centre.
- **Lead stories** — Trump puts the Iran decision off to 2027; Cyclone
  Akvan bears down on India's east coast; markets slide as Bitcoin hits
  a nine-month low.
- **37 stories from 6 regions** — Asia-Pacific 12, Europe 6, Middle
  East 6, Americas 8, Africa 3, Worldwide 2.
- **The day by hours** — seven time-anchored events as reported.
- **Twelve more stories** in three columns — the Ethiopian Airlines
  data breach, Hayabusa2's scrapped landing, GTA 6 sales, Europe–Russia
  talks, the Kyiv embassy blasts, the Bapco plant restart, the Senegal
  boat sinking, voices from a besieged Yemeni city, Polymarket's oil and
  gas contracts, South Korea's court ruling, Fiji's drought disaster,
  and Apple's own AI agent.
- **Where it happened** — a world map with six numbered pins, a
  22-item "Also on this page" list, a verdict box, markets, a date-check
  box naming what was deliberately left off, and a sources line.

## How it is made

`build_image.py` draws the whole page with Pillow (deterministic — the
same bytes on every run) from the story list in the same file. `main.py`
(Python 3.13, standard library only) copies the resulting `entry.png` to
`$MAKEFUN_OUTPUT_DIR` (default `/output`). No network is used at run time.

```sh
python3 build_image.py   # writes entry.png (1024x1024)
python3 main.py          # copies entry.png to /output/entry.png
```

## How sure are we?

Every story carries a REPORTED / CLAIM / FORECAST tag: REPORTED means
confirmed by named sources, CLAIM means one side says it and it is
unverified, FORECAST means a schedule or a projection. The date-check box
lists the big headlines that are not 20 November's news and were left off
on purpose.
