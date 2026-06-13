# Drop your generated PNGs here

Paste every image Nano Banana generated into **this folder** (`GAME/sprites/`). Don't worry about cleaning the green background — I'll chroma-key it out, despill the edges, and write the alpha-cut PNGs back.

## Filenames I'm expecting

If your file is named something different, just rename it to match. Anything not on this list, I'll inspect anyway and tell you where it fits.

### Hero (canonical facing: **RIGHT**)
- `hero_idle.png`
- `hero_run.png`
- `hero_jump.png`
- `hero_shoot.png` *(rifle)*
- `hero_shoot_pistol.png` *(optional)*
- `hero_hurt.png`
- `hero_win.png` *(optional)*

### Bots (canonical facing: **LEFT** — they advance toward the hero)
- `bot_skitter_idle.png`
- `bot_skitter_charge.png`
- `bot_gunner_idle.png`
- `bot_gunner_walk.png`
- `bot_heavy_idle.png`
- `bot_heavy_stomp.png`
- `bot_heavy_smash.png`

### Pickups
- `pickup_health.png`
- `pickup_ammo.png`
- `pickup_weapon.png`
- `pickup_score.png`

### Backgrounds
- `bg_far.png`
- `bg_mid.png`
- `bg_near.png`

## Why facing matters

The game will horizontally flip the sprite when the character moves the other way, so we only need **one** facing direction per pose. Canonical is **hero faces right** and **bots face left**. If any of your generations came out flipped, no problem — drop them in anyway and I'll flip them at processing time.

## When you're done pasting

Just reply "ready" (or list what you've got). I'll then:
1. List everything in the folder
2. Open each image and check pose + facing + sleeve fidelity + framing
3. Chroma-key the #00FF00 green out, despill the edges, save as transparent PNG
4. Tell you exactly which poses are missing or need a regen
5. Wire the cleaned sprites into the game
