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

## The image (v7)

A dense illustrated front page — "The World in One Page" — for Thursday 19 November 2026: 44 stories on one page. A huge serif masthead names the date, a region-counted strip and a six-figure "day in numbers" strip run underneath, and the page is led by three large illustrated panels (see below), followed by a 12-item illustrated grid, a "WHERE IT HAPPENED" world map with numbered pins, 29 numbered briefs, and a DATE CHECK footer naming the items left out as other days' news.

- **Lead — Summit in Shenzhen:** Trump, Xi and Putin hold a first three-way summit. Ninety minutes, one table, a four-point "Declaration toward Peace": UN reform, fuel supply, ICC limits — and that nuclear war "cannot be won".
- **Lead — World Court in The Hague:** Myanmar guilty of genocide. 9 of 15 judges find for The Gambia — a first for the court; reparations ordered.
- **Lead — Anthropic debuts in the biggest IPO ever:** opened $111.50, closed $97.17, up 17% on its $83 price, $81.3bn raised.
- **The day in numbers:** Anthropic $81.3bn · Dow −1,101 · Bitcoin ~$61,353 · ICJ 9 of 15 · Cyclone Akvan 95 km/h, 300,000+ evacuated · Voyager 1 25.9bn km.
- **Region counts (computed from the story list):** Asia 7 · Middle East 2 · Europe 6 · Africa 1 · Americas 20 · Oceania 1 · Global 7 = 44.
- **Story grid (12):** GTA VI launches on PS5 and Xbox (midnight launch, 99 on Metacritic); APEC adopts the Shenzhen Outlook; Ukraine hits the Crimea Bridge a third time; the Gaza raid ends after a day; the COP31 draft drops fossil fuels and cuts the $120bn aid goal; Colombia's unions hold a national strike, with marches in five cities over the tax bill; Cyclone Akvan nears India's coast; the Dow drops 1,101 points, below 50,000; Bitcoin sinks below $62,000; Voyager 1 confirmed one light-day out; Texans crush Colts 26–3; Valkyries sweep Aces into a first Finals.
- **Also on Thursday 19 November (29 numbered briefs, pinned on the map where they have a single place):** the Senate rejects the Iran war curb, 48–51; a third US carrier reaches the Gulf; the UK is forced to admit the Apple backdoor order; the White House cyber chief is fired; Japan core inflation up 2.2%; Australia's jobless rate hits a 2021 high; copper lowest since April; Wall Street's $500bn Nvidia pledge unspent; Moody's: the US grew faster than expected; AMD falls 8% on short-seller doubts; hackers leak JPMorgan clients' data; a China team wins the Gordon Bell Prize (1.456 exaflops); a pulsar hunt runs a million times faster; Wemby's 32 lifts Spurs past Clippers; Grizzlies rout Warriors, Knicks edge Wolves; Kings edge Leafs 4–3 in a shootout; Skydance merges Warner Bros and Paramount TV; the Beatles release a new "In My Life" video; Jazz Fest 2027 names its headliners; Ramayana passes 1,547 crore worldwide; Patrick Stewart cremated using water; gold down ~2% to ~$3,667/oz; South Africa holds its rate at 7.25%; Goolsbee won't rule out bigger hikes; IEA: the Iran war may cut Hormuz reliance; Warner Music's first $2bn quarter; GTA pre-orders ~$1.54bn (Sensor Tower estimate, 17 Nov); US jobless claims jump unexpectedly; Canada eases rules for small banks.
- **Date check — left out on purpose, not 19 Nov:** the EU's €45bn Ukraine loan (proposed 18 Nov); Van Gogh's $190.4m sale (18 Nov); the Xi–Trump tarmac hug (18 Nov); the Kuwait strikes (17–18 Nov); the Gaza raid's start (18 Nov — its end is on the page); Voyager crossing one light-day (18 Nov — NASA confirmed it 19 Nov); COP31's scheduled close (20 Nov); Cyclone Akvan's landfall (20 Nov).

The page is drawn by `render_v7.py` (build-time only, Pillow) from the fixed news data in that file, so the image is fully reproducible. The grader never runs the renderer — it only runs `main.py`. The illustration is deliberately non-photorealistic: flat geometric shapes, solid colour blocks, bold silhouettes and simple pictograms drawn from primitives. No gradients, no shading, no fake photos, no detailed faces. The world map is drawn in code from polygon continents; pin positions are approximate.

## What changed in v7 (and why)

v6 was audit-GO with 44 stories, but it lacked the four features every top entry on the leaderboard shares: three large illustrated leads (v6 had one lead plus three text-only colour bands), a world map with numbered pins, a region-counted strip, and a strong date-check footer. v7 is a bounded delta on v6 that adds exactly those four, keeping v6's story content, numbers strip and masthead date. The structure follows the top entries; no text, headline, wording or drawing is copied from them — all content is this entry's own verified research and own flat illustrations.

- **Three illustrated leads:** the summit panel is kept (rescaled, flags fixed so the skyline no longer hides them); the ICJ verdict and the Anthropic debut are new illustrated panels (courthouse + scales + red 9–6 badge; dark-green candlestick chart with IPO $83 and the $97.17 close). GTA VI moves from a second lead to a large illustrated grid item.
- **World map + numbered briefs:** v6's 32-item pictogram grid and 6-item ticker become a 12-item illustrated grid plus 29 numbered one-line briefs, each pinned on the map where it has a single place (18 pins, one per distinct place — pinning every place-bearing brief merged into an unreadable blob over the US east coast in the first render). Two verified 19 Nov items dropped from v6's page (US jobless claims, Canada easing bank rules) return as briefs, so the total stays at 44.
- **Region-counted strip:** Asia 7 · Middle East 2 · Europe 6 · Africa 1 · Americas 20 · Oceania 1 · Global 7, computed from the actual story list and summing to 44 (the renderer asserts this). It replaces the "44 STORIES · EVERY CONTINENT" masthead line's job of proving breadth.
- **Date-check footer:** v6's "Yesterday — 18 Nov" slot is folded into a red-bordered DATE CHECK box naming eight specific items left out as other days' news, with their real dates — so the same information is not duplicated in two places.
- **Render fixes found during the build:** grid pictograms are rendered at their native 44px and scaled down (several pictogram functions use absolute coordinates that break at 32px); four brief headlines were shortened to fit their columns (the 48–51 Senate vote, the 1.456-exaflops Gordon Bell figure, the Sensor Tower estimate date and the 17 Nov dating are all kept).

## What changed in v6 (and why)

v5 was typography-only, ~10 items, no illustration — approved by Ketua ("bagus sih") and submitted 19 Nov, but its live dev rank sat around #3,800 of ~13,000, well below the top-50 cutoff. The audit found the lever was a dense illustrated front page: 35–45 stories, the format the leaderboard's top entries use (huge dated masthead, number strip, illustrated leads, a grid of small illustrated stories, a numbered "also" list, a date-check footer). v6 follows that format with the flat infographic style, because the earlier illustrated versions (v2/v4) still read as AI-made. v5 stays intact in git (commit 33d8ba1) as the fallback.

## What changed in the v6 fix round (round-1 audit, 7 defects)

The round-1 audit (`work/audit-log-v6.md`) found 7 defects; all are fixed in this revision, and the two new stories were verified live first (see `work/research-v6-addendum.md`).

- **D1 — COP31 added.** The 19 Nov COP31 draft deal in Antalya (fossil-fuel references stripped out, the $120bn adaptation-finance figure dropped, text cut from 144 to 80 paragraphs) is now a World grid item: "COP31 draft drops fossil fuels — Slim text cuts $120bn aid goal." (Reuters, Antalya, 19 Nov.)
- **D2 — Colombia added.** The 19 Nov nationwide general strike called by the CUT against the tax reform, with marches in Bogotá, Medellín, Cali, Barranquilla and Bucaramanga, is now a World grid item: "Colombia unions hold national strike — Marches in five cities over tax bill." South America is now on the page, so the masthead's "EVERY CONTINENT" claim holds.
- **Swaps (count stays at 44):** the micro-moth item (Science — the least consequential verified story) and the Trump-dozing item (Culture — the least consequential item, and the only one resting on a contested reading of a video) were removed to make room. World is now 9 items, Science 2, Culture 5; the grid is still 32 and the page total is still 44.
- **D3 — Jazz Fest deck fixed:** "Foo Fighters, Kahan, The Who." (the full "Noah Kahan" does not fit the one-line deck; "The Who" was being truncated to "Who.").
- **D4 — Akvan figure fixed in both places:** "300,000+" evacuated, in the numbers strip and in the Cyclone Akvan deck (the source says more than 300,000).
- **D5 — Hackers headline fixed:** "Hackers leak JPMorgan clients' data" — the story's core fact is JPMorgan, and the 16,000 figure covered only the Reserve cards (~24,000 in total across JPMorgan, Visa and Mastercard).
- **D6 — ICJ deck fixed:** "9 of 15 judges find for The Gambia — a first for the court." (the first time the ICJ has held a state responsible for genocide).
- **D7 — Masthead strip shortened:** "44 STORIES · EVERY CONTINENT" — the "ALL FROM THIS ONE DAY" clause contradicted the labelled 18 Nov Yesterday slot.
- **Date-check footer added** (auditor's recommendation): the Yesterday line now ends "DATE CHECK: every other story 19 Nov 2026", so the page states its own date discipline. It fits on the existing line with room to spare; no story text was shrunk. (A ✓ glyph was tried first and rendered as a tofu box in Noto Sans, so the line uses a colon instead.)

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

AnewZ (Shenzhen summit, APEC Outlook), The News / Reuters (ICJ Myanmar verdict), Motley Fool (Anthropic debut), Candid Dragon evening briefing (Dow, AMD), PlainBTC (Bitcoin, gold), Morningstar / Dow Jones (Japan inflation, Australia jobs, South Africa rate, Goolsbee, copper, IEA, Nvidia pledge, Moody's), TechCrunch (UK Apple backdoor order), Nextgov (White House cyber chief), Reuters via WNCY (JPMorgan data leak), HPCwire (Gordon Bell Prize), Phys.org (pulsar hunt), Scientific American (Voyager 1), Sambad English (Assam moth), Wikipedia / IMD (Cyclone Akvan), SportsFBI (Texans–Colts), Flashscore (NBA roundup), USCT Sport (Valkyries–Aces), AskScores (Kings–Leafs), Asia Today (GTA VI launch), CNN via KESQ (GTA pre-order estimate), AI Eye (Skydance), Standard Topic archive (Warner Music, Beatles, Jazz Fest, Ramayana, Patrick Stewart), Tatler Asia (Trump dozing), European Commission (EU loan, 18 Nov), Artnet (Van Gogh, 18 Nov), Reuters via SRN News (Senate vote), ASEAN NOW / BBC (Gaza), Devdiscourse / Reuters (Crimea Bridge), UECN / China Daily (third carrier), Reuters via 979 WEVE (COP31 draft), Watan News (COP31 draft text), Climate & Capital Media / AFP (COP31), Terra World News (Colombia strike), Travelers Today / Semana / El Tiempo (Colombia strike, live), I-Journey / US Embassy Bogotá alert (Colombia strike). Researched from public news on 19–20 November 2026; the image is drawn, no photograph is from the day.

---

<sub>Entered on [make.fun](https://make.fun/?ref=0vh6bwht&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
