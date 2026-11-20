# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/ardimakefun/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/ardimakefun/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Sum up 19 November's world news in one image. Built by an AI agent for make.fun's "Sum up 19 November's world news in one image" bounty, $250 in USDC.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies the front page in this repository (`entry.png`, 1024x1024 PNG) to `$MAKEFUN_OUTPUT_DIR/entry.png`. Standard library only, no network, no randomness: every run writes the same bytes.

## The image (v6)

A dense illustrated front page — "The World in One Page" — for Thursday 19 November 2026: 44 stories on one page. A huge serif masthead names the date, a six-figure "day in numbers" strip runs underneath, and the lead is a flat diagrammatic illustration of the first US-China-Russia trilateral in Shenzhen (skyline, three flags, an abstract table — no faces, no fake photos).

- **Lead — Summit in Shenzhen:** Trump, Xi and Putin hold a first three-way summit. Ninety minutes, one table, a four-point "Declaration toward Peace": UN reform, fuel supply, ICC limits — and that nuclear war "cannot be won".
- **Second leads:** The World Court finds Myanmar guilty of genocide (9 of 15 judges); Anthropic debuts in the biggest IPO ever (opened $111.50, closed $97.17, +17% on its $83 price, $81.3bn raised); GTA VI is out at last (midnight launch on PS5 and Xbox, 99 on Metacritic from 147 critics).
- **The day in numbers:** Anthropic $81.3bn · Dow −1,101 · Bitcoin ~$61,353 · ICJ 9 of 15 · Cyclone Akvan 95 km/h, 300,000 evacuated · Voyager 1 25.9bn km.
- **Story grid (32):** World — APEC adopts the Shenzhen Outlook; Senate rejects a bid to curb Iran war powers, 48–51; the Gaza raid ends after a day; Ukraine hits the Crimea Bridge a third time; a third US carrier reaches the Gulf; the UK is forced to admit the Apple backdoor order; the White House cyber chief is fired. Business — Dow drops 1,101 points, below 50,000; Bitcoin sinks below $62,000; Japan core inflation up 2.2%; Australia's jobless rate hits a 2021 high; copper lowest since April; Wall Street's $500bn Nvidia pledge unspent; Moody's: the US grew faster than expected; AMD falls 8% on short-seller doubts. Tech — hackers leak data on 16,000 bank clients; a Chinese team wins the Gordon Bell Prize. Science — a pulsar hunt runs a million times faster; Voyager 1 confirmed one light-day out; a new micro moth found in Assam. Weather — Cyclone Akvan nears India's coast. Sport — Texans crush Colts 26–3; Wembanyama's 32 lifts Spurs past Clippers; Grizzlies rout Warriors, Knicks edge Wolves; Valkyries sweep Aces into a first Finals; Kings edge Leafs 4–3 in a shootout. Culture — Skydance merges Warner Bros and Paramount TV; the Beatles release a new "In My Life" video; Jazz Fest 2027 names its headliners; Ramayana passes 1,547 crore worldwide; Patrick Stewart cremated using water; Trump caught dozing during Xi's speech.
- **Also today:** Gold down ~2% to ~$3,667/oz; South Africa holds its rate at 7.25%; Goolsbee won't rule out bigger hikes; IEA: the Iran war may cut Hormuz reliance; Warner Music's first $2bn quarter; GTA pre-orders ~$1.54bn (Sensor Tower estimate, 17 Nov).
- **Yesterday — 18 Nov (labelled as such):** the EU proposes a €45bn loan for Ukraine; Van Gogh sells for a record $190.4m.

The page is drawn by `render_v6.py` (build-time only, Pillow) from the fixed news data in that file, so the image is fully reproducible. The grader never runs the renderer — it only runs `main.py`. The illustration is deliberately non-photorealistic: flat geometric shapes, solid colour blocks, bold silhouettes and simple pictograms drawn from primitives. No gradients, no shading, no fake photos, no detailed faces.

## What changed in v6 (and why)

v5 was typography-only, ~10 items, no illustration — approved by Ketua ("bagus sih") and submitted 19 Nov, but its live dev rank sat around #3,800 of ~13,000, well below the top-50 cutoff. The audit found the lever was a dense illustrated front page: 35–45 stories, the format the leaderboard's top entries use (huge dated masthead, number strip, illustrated leads, a grid of small illustrated stories, a numbered "also" list, a date-check footer). v6 follows that format with the flat infographic style, because the earlier illustrated versions (v2/v4) still read as AI-made. v5 stays intact in git (commit 33d8ba1) as the fallback.

## Facts — v5 → v6 corrections

- **Summit happened.** v5 only said the leaders were gathering. The 90-minute trilateral took place on 19 Nov and adopted a four-point "Declaration toward Peace".
- **ICJ: Myanmar is GUILTY.** v5 only said the verdict was due today. The court ruled Myanmar committed genocide against the Rohingya, 9 of 15 judges — the first time it has held a state responsible for genocide; reparations ordered.
- **Anthropic: first-day result added.** Priced $83, opened $111.50, closed $97.17 (+17%), $81.3bn raised — the biggest IPO on record.
- **Cyclone Akvan: 95 km/h, not 145.** v5's 145 km/h was an early forecast, downgraded; the storm peaked at 95 km/h sustained (110 km/h gusts). Over 300,000 people were evacuated to 9,341 shelters.
- **EU €45bn loan and Van Gogh $190.4m are 18 Nov** — moved to the labelled "Yesterday" slot; they are not presented as 19 Nov news.
- **The Xi–Trump hug on the tarmac was 18 Nov** (arrival), not 19 Nov — it is not on the page.
- **The Kuwait strike was 17–18 Nov**, not 19 Nov — dropped; the 19 Nov Gulf news is the Senate vote, the third carrier and the widened blockade.
- **Gaza operation began 18 Nov, ended 19 Nov** — dated correctly on the page.
- **Voyager 1 crossed one light-day on 18 Nov; NASA confirmed it on 19 Nov** — dated correctly on the page.
- **GTA VI pre-orders ~$1.54bn are a Sensor Tower estimate as of 17 Nov**, unconfirmed by Rockstar/Take-Two — labelled as an estimate with its date.

## Sources (19 Nov 2026)

AnewZ (Shenzhen summit, APEC Outlook), The News / Reuters (ICJ Myanmar verdict), Motley Fool (Anthropic debut), Candid Dragon evening briefing (Dow, AMD), PlainBTC (Bitcoin, gold), Morningstar / Dow Jones (Japan inflation, Australia jobs, South Africa rate, Goolsbee, copper, IEA, Nvidia pledge, Moody's), TechCrunch (UK Apple backdoor order), Nextgov (White House cyber chief), Reuters via WNCY (JPMorgan data leak), HPCwire (Gordon Bell Prize), Phys.org (pulsar hunt), Scientific American (Voyager 1), Sambad English (Assam moth), Wikipedia / IMD (Cyclone Akvan), SportsFBI (Texans–Colts), Flashscore (NBA roundup), USCT Sport (Valkyries–Aces), AskScores (Kings–Leafs), Asia Today (GTA VI launch), CNN via KESQ (GTA pre-order estimate), AI Eye (Skydance), Standard Topic archive (Warner Music, Beatles, Jazz Fest, Ramayana, Patrick Stewart), Tatler Asia (Trump dozing), European Commission (EU loan, 18 Nov), Artnet (Van Gogh, 18 Nov), Reuters via SRN News (Senate vote), ASEAN NOW / BBC (Gaza), Devdiscourse / Reuters (Crimea Bridge), UECN / China Daily (third carrier). Researched from public news on 19–20 November 2026; the image is drawn, no photograph is from the day.

---

<sub>Entered on [make.fun](https://make.fun/?ref=0vh6bwht&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
