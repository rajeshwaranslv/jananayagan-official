#!/usr/bin/env python3
"""
generate_posters.py — generate Jana Nayagan game posters with Nano Banana 2.

Usage (from this folder):
    python generate_posters.py 1       # generate poster #1 only
    python generate_posters.py 2       # generate poster #2 only
    python generate_posters.py 3       # generate poster #3 only
    python generate_posters.py all     # generate all three
    python generate_posters.py         # defaults to 1 (sample first)

Output: poster_1.png, poster_2.png, poster_3.png in this folder.

Reads GEMINI_API_KEY from a .env file in this folder, or from the env.
Falls back to gemini-3-pro-image-preview (Nano Banana Pro) if the
flash variant is rejected — set MODEL env var to override.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# ---------- third-party imports with friendly errors ------------------------

try:
    from dotenv import load_dotenv
except ImportError:
    sys.exit("Missing dependency: python-dotenv. Run:\n"
             "    pip install -r requirements.txt")

try:
    from google import genai
    from google.genai import types  # noqa: F401  (kept for future config use)
except ImportError:
    sys.exit("Missing dependency: google-genai. Run:\n"
             "    pip install -r requirements.txt")

try:
    from PIL import Image
except ImportError:
    sys.exit("Missing dependency: Pillow. Run:\n"
             "    pip install -r requirements.txt")


# ---------- paths -----------------------------------------------------------

HERE = Path(__file__).resolve().parent
GAME = HERE.parent
SPRITES = GAME / "sprites"

# Try local .env first, then the sibling gemini-cli/.env we created earlier.
load_dotenv(HERE / ".env")
load_dotenv(GAME / "gemini-cli" / ".env")

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    sys.exit("GEMINI_API_KEY not found. Add it to posters/.env or "
             "gemini-cli/.env, or export it in your shell.")

MODEL = os.getenv("MODEL", "gemini-3.1-flash-image-preview")
FALLBACK_MODELS = [
    "gemini-3-pro-image-preview",
    "gemini-2.5-flash-image",
]

# ---------- shared style guidance fed into every poster ---------------------

STYLE_PREAMBLE = """\
You are designing a theatrical-quality movie poster for a 2D action video game
called "JANA NAYAGAN" (Tamil for "leader of the people").

The game is inspired by the Tamil action film "Jana Nayagan" starring
Thalapathy Vijay. Setting: a near-future dystopia, abandoned Indian-Tamil
megacity at night — collapsed flyovers, burning vehicles, neon shop signage
flickering in Tamil script, ash-thick haze, sodium-orange streetlights.

Hero: a charismatic male Tamil action protagonist, late-30s, athletic build,
tousled black hair, light stubble. Tactical olive cargo pants, fitted dark
combat shirt with sleeves pushed to forearms, leather strap across chest,
weathered boots. He carries a custom assault rifle. Confident, righteous,
slightly battle-worn. He is NOT a literal portrait of any real actor —
treat him as an original character inspired by the genre archetype.

Enemies: hulking armored "arm-bots" — heavy industrial robots, scratched
gunmetal plating, single glowing red optic, exposed hydraulics. Some lean
heavy and slow, others are skittering quadrupeds. They advance toward the
hero in groups.

Visual style: cinematic painterly realism — somewhere between a high-end
2D illustration and a photoreal film key-art. NOT pixel art, NOT 8-bit,
NOT chibi/anime. Think Tamil blockbuster poster + Blade Runner palette.
Strong rim lighting, volumetric haze, lens flare, dramatic chiaroscuro.
Teal-and-orange color grading with deep blacks.

The reference images attached are: (a) the official JANA NAYAGAN logo —
match its lettering, weight, and treatment; (b) sprite art of the hero
and enemies — use them only to anchor character design (silhouette,
clothing, weapon, robot architecture). The bright #00FF00 green
background in the sprite references is a chroma-key — IGNORE it
entirely; do not replicate green anywhere.

Final image MUST: include the JANA NAYAGAN logo composited tastefully
into the design (top, bottom, or sky), be high-resolution, vertical or
landscape per the brief, with no watermarks, no UI mockups, no
artist signatures.
"""

# ---------- the three posters -----------------------------------------------

POSTERS = {
    1: {
        "name": "poster_1.png",
        "label": "Hero portrait — vertical key art",
        "refs": [
            "jananayaganlogo.png",
            "hero_idle_rifle.png",
            "bot_heavy_idle.png",
        ],
        "prompt": STYLE_PREAMBLE + """
COMPOSITION FOR THIS POSTER (vertical 3:4 movie-poster orientation):

The hero stands centered, slightly heroic low-angle, full-body in frame,
rifle held diagonally across his torso (low ready). Dramatic backlight
silhouettes him against billowing smoke shot through with sodium-orange
glow. Behind and below him, four to six armored arm-bots emerge from
the haze — only their red optics and shoulder plating clearly visible,
the rest dissolving into the smoke. A collapsed concrete flyover frames
the upper third. Embers drift across the foreground.

Place the JANA NAYAGAN logo (from reference) at the very top, large,
slightly weathered as if etched in metal. Below the hero's feet, leave
clean negative space suggestive of where a release date / tagline would
sit (do NOT add placeholder text — just leave the room).

Mood: messianic, defiant, cinematic. The audience should feel the
hero is one man facing a city of machines.
""",
    },
    2: {
        "name": "poster_2.png",
        "label": "Action shot — horizontal explosive moment",
        "refs": [
            "jananayaganlogo.png",
            "hero_shoot.png",
            "bot_gunner_idle.png",
        ],
        "prompt": STYLE_PREAMBLE + """
COMPOSITION FOR THIS POSTER (landscape 16:9, frozen-action key art):

A single freeze-frame of combat. The hero is on the right third of
frame, mid-fire — rifle shouldered, muzzle flash blooming bright
white-hot, a single empty shell ejecting and frozen in mid-air,
his coat (or shirt sleeves) snapping in the blast wave. On the left
third, an arm-bot is mid-shatter: its armored chestplate cracking
open in radiating lines, sparks and shards of metal exploding outward
toward camera, red optic flickering and dying. Between them, the
bullet's path is visible as a faint heat-warp.

Background: rain-slick neon-lit Tamil street, blurred Tamil-script
neon signage in bokeh, two more arm-bot silhouettes advancing in
the deep background. Color grade: heavy teal shadows, white-orange
muzzle flash as the only warm light source; the explosion is the
hero of the lighting.

Place the JANA NAYAGAN logo (from reference) in the lower-left
quadrant, smaller than poster #1, like a film studio plate.

Mood: kinetic, brutal, frozen-second-of-impact.
""",
    },
    3: {
        "name": "poster_3.png",
        "label": "Wide cinematic — panoramic dystopia",
        "refs": [
            "jananayaganlogo.png",
            "bg_far.png",
            "bg_near.png",
            "hero_idle_rifle.png",
            "bot_heavy_idle.png",
        ],
        "prompt": STYLE_PREAMBLE + """
COMPOSITION FOR THIS POSTER (landscape ultra-wide 21:9 panoramic):

A cinematic establishing shot of the entire battlefield. Camera is
low and far, looking down a ruined six-lane Tamil arterial road at
dusk-going-night. Collapsed glass-and-concrete towers lean inward
on both sides, broken neon Tamil shop signs hang at angles, flames
flicker in upper-floor windows. Three military helicopter spotlights
sweep through the haze from the sky.

In the deep middle distance, the hero is a small but unmistakable
silhouette walking toward camera, rifle at his shoulder, coat
trailing. Between him and camera: a wave of arm-bots — at least
twelve to fifteen robots in varied silhouettes (heavy stompers,
quadruped skitters, bipedal gunners) — advancing in a loose
phalanx. Their red optics form a constellation of points across
the frame. Burning car wrecks dot the road. Embers, ash, and
papers swirl in the air.

Place the JANA NAYAGAN logo (from reference) high in the sky as
if rendered in light against the smoke clouds — large, godlike,
the title literally hanging over the war.

Mood: epic, end-of-world, one-man-army. This is the establishing
poster — the audience should understand the entire game in a
single glance.
""",
    },
}

# ---------- generation core -------------------------------------------------

def load_refs(filenames: list[str]) -> list[Image.Image]:
    refs: list[Image.Image] = []
    for fn in filenames:
        p = SPRITES / fn
        if not p.exists():
            print(f"  ! missing reference: {p}", file=sys.stderr)
            continue
        refs.append(Image.open(p))
    return refs


def generate_one(client: genai.Client, model: str, n: int) -> bool:
    spec = POSTERS[n]
    out = HERE / spec["name"]
    print(f"\n[poster {n}] {spec['label']}")
    print(f"  model: {model}")
    print(f"  refs : {', '.join(spec['refs'])}")
    print(f"  out  : {out}")

    contents: list = [spec["prompt"]] + load_refs(spec["refs"])

    t0 = time.time()
    try:
        response = client.models.generate_content(model=model, contents=contents)
    except Exception as e:
        print(f"  ! API error: {e}", file=sys.stderr)
        return False

    saved = False
    text_notes: list[str] = []
    for part in (response.candidates[0].content.parts or []):
        if getattr(part, "inline_data", None) and part.inline_data.data:
            out.write_bytes(part.inline_data.data)
            saved = True
        elif getattr(part, "text", None):
            text_notes.append(part.text)

    if text_notes:
        print("  model said:", " ".join(text_notes)[:300])

    if saved:
        print(f"  ok in {time.time() - t0:.1f}s -> {out}")
        return True
    print("  ! no image returned by model", file=sys.stderr)
    return False


def generate_with_fallback(client: genai.Client, n: int) -> bool:
    if generate_one(client, MODEL, n):
        return True
    for fb in FALLBACK_MODELS:
        if fb == MODEL:
            continue
        print(f"  retrying with fallback model: {fb}")
        if generate_one(client, fb, n):
            return True
    return False


def main() -> int:
    arg = (sys.argv[1] if len(sys.argv) > 1 else "1").lower()
    if arg == "all":
        targets = [1, 2, 3]
    else:
        try:
            n = int(arg)
            if n not in POSTERS:
                raise ValueError
            targets = [n]
        except ValueError:
            print(f"invalid argument '{arg}'. use 1, 2, 3, or all.", file=sys.stderr)
            return 2

    client = genai.Client(api_key=API_KEY)

    ok_count = 0
    for n in targets:
        if generate_with_fallback(client, n):
            ok_count += 1

    print(f"\nDone. {ok_count}/{len(targets)} posters generated in {HERE}")
    return 0 if ok_count == len(targets) else 1


if __name__ == "__main__":
    sys.exit(main())
