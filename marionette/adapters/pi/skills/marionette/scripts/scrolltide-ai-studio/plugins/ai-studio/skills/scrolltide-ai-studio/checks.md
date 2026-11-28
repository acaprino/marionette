# Checking the page

A scroll page can look perfect at the top and be broken three screens down. Check it where it
changes. Run the checkpoint script, then look at every picture it takes.

```bash
# a running dev server
node <skill>/scripts/scrollshot.mjs http://localhost:5173 shots
# a build output, served for you
node <skill>/scripts/scrollshot.mjs dist shots --reduced
# a single file
node <skill>/scripts/scrollshot.mjs index.html shots
```

`<skill>` is this skill's folder. Run it from the project folder, so it finds the project's
Playwright (`npm i -D playwright && npx playwright install chromium` if it isn't there). It writes
`desktop-first-paint.png`, `desktop-000.png` … `desktop-100.png`, `mobile-000.png` …
`mobile-100.png`, the same for `reduced-` with `--reduced`, and `report.json`, and prints what's
blocking. Long films want more checkpoints: `--stops 0,10,20,30,40,50,60,70,80,90,100`.

No browser available at all? Say so plainly and check the code against the lists below. Never say
a page was checked visually when it wasn't.

## 1. Blocking: fix all of these

The script reports most of them:

- Script errors, console errors, failed requests, HTTP errors, broken images.
- A video that never became playable.
- The page scrolls sideways at either width.
- The `<h1>` falling back to a system font because the web font didn't load.
- A first paint that flashes white on a dark page (no ground colour on `html`/`body`).
- `npm run build` (and `npm run lint` where the build has one) not clean.
- Placeholder copy left in ("Lorem", "Your headline", "Feature 1"), or the library build's invented
  brand still showing anywhere.
- A library download URL in the finished code (the report lists media served from other hosts).

## 2. The scroll: look at every checkpoint

Open the shots in order, desktop then mobile, and answer for each one:

- **Did something change since the last checkpoint?** The report marks identical neighbours. Inside a
  pinned stage that means the stage is stuck: the section isn't pinning, the loop isn't running, or
  frames didn't load.
- **Is the subject in frame?** On the phone shots especially: the portrait cut, the focal point and
  `object-position` exist for this.
- **Can every visible line be read?** Over film or layers, at both widths. Nothing clipped by the
  viewport or by the pinned box.
- **Do the holds hold?** Where copy or a card belongs to a beat, at least one checkpoint should catch
  it fully in. If none does, add stops inside that window (`--stops 30,33,36`) and look again.
- **Does the stage hand off cleanly?** After a pinned section ends: no blank band, no seam, no jump
  in colour. The apron (house-style.md) should already be the next section's colour.
- **Reduced motion (`reduced-*.png`):** every block that should be visible is visible; nothing is
  waiting on an entrance that never runs.

Fix anything that fails at any checkpoint.

## 3. The house style: fix the three worst

Hold the page against `house-style.md` and fix the **three** things that most break it, the ones a
visitor would notice first. Typical offenders, in order of how often they show up:

1. More than one accent colour, or coloured glows on cards.
2. Display type too small or too loose: under the clamp ranges, or tracking left at `0`.
3. A pure `#000` or `#fff` ground where the build had a tinted ink or paper.
4. Two things moving for attention in the same viewport.
5. Default easing (`ease`, `linear`) on entrances instead of the house curves.
6. Vague copy where a specific number or name would do the work.

## 4. Shoot once more

Run the script again after the fixes and look again. One more round is normal. If something
blocking is still there after that, say exactly what and why instead of going round in circles.
If something can't be fixed from here (no suitable media, a font the user must license), tell the
user what would fix it.

## What to report

- Which checkpoints you looked at, and the desktop and mobile shot that best show the scroll moment.
- What the script flagged and what you changed for each.
- Anything you couldn't check, and why.
