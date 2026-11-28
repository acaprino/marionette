# Scrolltide house style

The numbers in this file are measured, not invented: on 23 November 2026 we read the source of all
317 published Scrolltide builds (155 templates, 124 components, 24 sections, 14 UI screens) and
counted what they actually use. Where a rule is a house decision rather than a measurement, it says so.

Use these as the defaults for anything you build or change. The library build you start from
outranks this file: if its prompt sets a value on purpose, keep it.

## The idea

**One scroll moment, real media, a quiet ground.** Every page is organised around a single thing
that happens because the visitor scrolls: a camera moves, layers part, a path draws itself, a reel
slides past. Everything else on the page stays still enough for that one thing to read.

Name the moment in one sentence before you build ("scrolling cranes the camera from the pool to
the ring"). If you can't, the page doesn't have one yet.

## Ground

The page colour is the stage the media sits on, never a decoration.

- **Dark ground is ink, not black.** Of 61 dark builds, 38 tint their near-black cool (`#04050a`,
  `#05070c`, `#07080b`, `#03060a`) and only 5 use pure `#000000`.
- **Light ground is paper, not white.** Of 57 light builds, 47 are warm stone (`#e9e1d3`,
  `#efe9df`, `#f2eee6`, `#ebe8e1`) and 1 uses pure `#ffffff`.
- Dark and light are close to even across the library (61 against 57 builds that set a page
  colour), so pick for the brand, not by habit.
- **Hand off with an apron.** When a pinned stage ends, its last layer carries a solid block of the
  next section's colour below it, so the stage climbs off and the page continues with no seam.
- Set the ground on `html` and `body` in the first CSS rule so nothing flashes before it paints.

## Accent

House rule: **one accent hue per page.** Use it on small working parts: an eyebrow label, a status
dot, a progress bar, the one highlighted word, a focus ring. Cards and panels stay neutral graphite
(dark) or stone (light) with a faint inset highlight. Give the richness to the media, not to
colour washes.

Never give each card or tile its own coloured glow. A row of orange, violet and mint corner glows
reads as generated filler. Never use a purple-to-blue gradient as the page's visual.

## Type

Measured across the builds that load web fonts:

| Role | What the library uses | Share |
|---|---|---|
| Text and UI | Inter | 68% of builds |
| Display with character | Satoshi, Michroma, Bodoni Moda, Playfair Display, Archivo, Fraunces, Anton | varies by brand |
| The one serif word | Instrument Serif italic | 17% |
| Readouts and labels | JetBrains Mono, Geist Mono, IBM Plex Mono, Martian Mono | 13%+ |

- **One or two families** in 70% of builds. Three when it's display + text + a mono for readouts.
- **The serif word.** In a sans headline, set the single word doing the work in an italic serif
  ("Not *Machines*", "a little *theatre*"). One word, not a phrase.
- **Display sizes** are fluid. The most common clamps: section heads `clamp(…, 5vw, 64px)`; heroes
  `clamp(…, 6vw, 80px)` to `clamp(…, 8vw, 104px)`.
- **A wordmark that must run edge to edge is sized by measurement, not `vw`.** Measure it at a
  probe size and scale it to the container (`patterns/type.md`). Font advance widths make `vw` guesses
  overflow or fall short.
- **Tracking**: body and UI `-0.01em`; display `-0.02em` to `-0.04em`; uppercase mono labels
  `+0.08em`, `+0.14em`, `+0.16em` or `+0.2em`.
- **Line height**: display at `1`; huge display at `0.9` to `0.95`; body at 1.5 to 1.6.
- Numbers that change (counters, clocks, prices) get `font-variant-numeric: tabular-nums`.

## Shape

- **Actions are pills**: `border-radius: 999px` is the most used radius in the library by far.
- **Cards sit at 28px.** The second most used radius, and the house card shape.
- **Technical parts are crisp**: 2–6px for tags, HUD frames, film stills and data chips.
- Inside a rounded container, an inner shape's radius is the outer radius minus the gap, or square.

## Motion

Timed motion (entrances, hovers, state changes):

| Use | Curve | Why |
|---|---|---|
| Entrances and reveals | `cubic-bezier(0.16, 1, 0.3, 1)` | The library's most used curve (52 builds) |
| Softer entrances | `cubic-bezier(0.22, 1, 0.36, 1)` | Second most used (44) |
| Pops, toggles, checks | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Spring overshoot (27) |
| Leg and card swaps | `cubic-bezier(0.2, 0.7, 0.1, 1)` | Quick settle (27) |
| Sheets and state swaps | `cubic-bezier(0.65, 0, 0.35, 1)` | Symmetric in-out (13) |

Durations, by how often they appear: **200ms** for hovers; **250–400ms** for UI state;
**600–800ms** for entrances; **1.2–1.6s** for big reveals and preloader exits.

Scroll-driven motion is different: it isn't timed at all. It is **arithmetic on scroll progress**:
each beat is a range of progress, eased with `easeOutCubic` or `smoothstep` inside its range
(`patterns/engine.md`). Never put a CSS transition on a property the scroll writes every frame.

## Scroll

- **One rAF loop runs the page.** 63% of builds run their own `requestAnimationFrame` loop; the
  scroll builds advance Lenis from it (`lerp: 0.09`) and let every section read its own progress
  and write styles directly. Scroll never goes through framework state. ScrollTrigger appears in 1%
  of builds and Motion's `useScroll` in 2%: they are not how we do scroll.
- **Stage lengths**: a full scroll film most often runs **600vh** (50 builds). A single pinned beat
  runs **200–450vh** (SELENE's hero is 440, its trajectory 380, its reel 340). Use `svh` for stage
  heights so mobile browser bars don't resize the stage mid-scroll.
- **Frames, not video, for scrubbing.** 62 builds scrub a canvas frame sequence; 13 scrub a
  `<video>`. Writing `currentTime` on every tick produces async seeks that drop under fast scrolling;
  a decoded frame is an array index (`patterns/film.md`).
- **Speed-ramp long films.** Map scroll progress to film time through a monotone curve: flat stretches
  hold on the beats that matter, steep stretches travel.
- **One heavy thing per viewport.** A frame film, a WebGL scene or a layered stage, not two at once.

## Media

- **Download, never hotlink.** Every asset lives in the project's own `public/` and ships with it. A
  library build's download URL must not appear in the finished code.
- **Two cuts of everything that fills the screen**: `d` (landscape) and `m` (portrait), swapped with
  `<picture>` or by aspect, so phones get a composition, not a crop.
- **Layered stills are cut from one render**, so every layer shares one crop and stays registered at
  every viewport (`patterns/layers.md`).
- **WebP for frames and layers; H.264 MP4 plus VP9 WebM for looping video**, with a poster.
- Generated imagery is fine. Say so on the page if the brand is real.

## Words

- **All copy in one content file** (`src/content.ts` in the library builds), so a rebrand is one file.
- **Specific numbers with units** carry more than adjectives: "384,400 km", "481 frames",
  "Two commissions open this winter".
- **Live readouts** give a page texture: a mission clock, an elevation in degrees, a local time, a
  countdown. Mono, small, tracked out, at reduced opacity.
- Headlines are short, with a line break where the thought breaks. Buttons say what happens
  ("Reserve a seat", "Commission a button").
- Invented brands and products are fine for a demo. Mark them as placeholders in the content file.
  Never invent a real company's prices, reviews or customer counts.

## Always

- `prefers-reduced-motion` honoured (75% of builds do; all new work must). Under it: no smooth
  scrolling, scroll mappings still apply but without smoothing, ambient loops stop, the final state of
  every entrance is shown.
- Pointer-only effects switched off under `(hover: none)`.
- Every reveal visible without JavaScript: hide reveal targets only once a `js` class is on `<html>`.
- No sideways scroll at 390, 768, 1280 or 1920 wide.
- Real `<title>`, alt text on meaningful images, `aria-hidden` on decorative layers, visible focus.

## Never

- Rainbow glows on cards, glassmorphism stacked on glassmorphism, blobs as the visual.
- Two scroll libraries, or an animation library layered on a hand-written loop.
- A pinned stage that scroll-jacks: Lenis smoothing is the only change to how the page scrolls.
- Placeholder boxes or grey rectangles where media should be. With no media, build a type-led page.
- Stock-photo heroes with a dark overlay to make the text readable.
