# Jana Nayagan poster generator (Nano Banana 2)

Generates three movie-poster creatives for the game using Google's latest
image model — `gemini-3.1-flash-image-preview` (Nano Banana 2). Falls back
to Nano Banana Pro (`gemini-3-pro-image-preview`) and the older 2.5 Flash
Image if the preview model isn't available on your key.

## One-time setup

Open Terminal, then:

```
cd "/Users/ikevinadams/Documents/Claude/Projects/GAME/posters"
pip3 install -r requirements.txt
```

Your API key is already in `.env` (gitignored).

## Generate the sample first

```
python3 generate_posters.py 1
```

That writes `poster_1.png` into this folder. Open it. If you like the
direction, generate the other two:

```
python3 generate_posters.py 2
python3 generate_posters.py 3
```

Or do all three at once:

```
python3 generate_posters.py all
```

## What each poster is

| # | Format | Concept |
|---|--------|---------|
| 1 | Vertical 3:4 | Hero portrait key art — Vijay-styled hero with rifle, robots silhouetted in smoke, logo at top |
| 2 | Landscape 16:9 | Frozen-action moment — hero firing, arm-bot mid-shatter, sparks, neon street |
| 3 | Ultra-wide 21:9 | Panoramic dystopia — entire ruined city, hero small, wave of bots advancing, logo in sky |

## Re-roll one you don't like

Re-running the same number overwrites the file:

```
python3 generate_posters.py 2
```

## Tweaking style

Open `generate_posters.py` and edit:
- `STYLE_PREAMBLE` — global style direction (palette, hero design, robot design)
- `POSTERS[n]["prompt"]` — composition for an individual poster
- `POSTERS[n]["refs"]` — which sprite images to feed as visual references

## Why this isn't running inside Cowork

Claude's Cowork sandbox can't reach Google's Gemini endpoint
(`generativelanguage.googleapis.com`) — outbound is blocked at the proxy.
Your Mac doesn't have that restriction, which is why this script runs
on your machine instead.
