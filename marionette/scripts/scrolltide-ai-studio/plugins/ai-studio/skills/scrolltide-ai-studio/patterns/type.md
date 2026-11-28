# Type moves

Four type patterns the library leans on. None of them needs a library.

## A wordmark that fits exactly

A single line that runs edge to edge at every width (SELENE's and NAÏADE's closing wordmarks). Don't
guess at a `vw` value: advance widths differ per font, so the guess overflows on one screen and falls
short on another. Measure at a probe size and scale to the container.

```js
/** el: inline-block, white-space: nowrap, inside the container it should span. */
export function fitText(el) {
  const parent = el.parentElement;
  const PROBE = 100;
  const fit = () => {
    el.style.fontSize = `${PROBE}px`;
    const cs = getComputedStyle(parent);
    const available = parent.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    // offsetWidth is the layout box, unaffected by per-letter transforms (scrollWidth is not).
    const natural = el.offsetWidth;
    if (natural > 0) el.style.fontSize = `${(PROBE * available) / natural}px`;
  };
  fit();
  document.fonts?.ready.then(fit); // re-fit once the web font swaps in; its metrics differ
  const ro = new ResizeObserver(fit);
  ro.observe(parent);
  return () => ro.disconnect();
}
```

```css
.wordmark { display: inline-block; white-space: nowrap; line-height: 0.8; letter-spacing: -0.04em; }
```

Widely tracked wordmarks carry trailing tracking after the last letter. Pull it back with a negative
`margin-right` equal to the tracking (`margin-right: -0.24em` for `letter-spacing: 0.24em`) so the
line looks centred.

## A title that resolves

On a pinned stage, a title can arrive by closing its tracking and losing its blur as the scroll
reaches it: `letter-spacing` from `0.6em` to `0.24em`, `blur` from 10px to 0, over a window like
`[0.08, 0.24]`. The code is in `layers.md`. Drop the filter once it reaches 0
(`filter = ''`) so the browser stops compositing it.

## Live readouts

Small mono numbers that change with the scroll or the clock make a page feel instrumented: a mission
clock, an elevation, distance flown, a local time, a countdown to a date.

```js
import { drive } from './scroll-engine.js';
import { easeOutCubic, range } from './scroll-math.js';

// Mission clock driven by scroll progress: 0 → 1 maps to T+ 00:00:00 → T+ 01:30:00
const hms = (s) => [s / 3600, (s % 3600) / 60, s % 60].map((v) => String(Math.floor(v)).padStart(2, '0')).join(':');
drive(stage, (p) => {
  clock.textContent = `T+ ${hms(p * 5400)}`;
  // The elevation follows the same window the subject climbs in, so the number and the picture agree.
  elev.textContent = `${(easeOutCubic(range(p, 0.04, 0.5)) * 12.4).toFixed(1)}°`;
});

// Local time, once a minute
const local = () => (timeEl.textContent = new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Lisbon' }) + ' in Lisbon');
local();
setInterval(local, 60_000);
```

```css
.hud { font-family: var(--font-mono); font-size: 0.625rem; letter-spacing: 0.14em; text-transform: uppercase; opacity: 0.75; font-variant-numeric: tabular-nums; }
```

Mark readouts that tick every frame `aria-hidden="true"`; they're texture, not content.

## One nav colour over any background

A nav that sits over a dark film one moment and an ivory card the next doesn't need to switch
colours in code. Make it white and blend it:

```css
.nav { position: fixed; inset: 0 0 auto; z-index: 50; color: #fff; mix-blend-mode: difference; }
```

It reads as white on dark and near-black on light. Keep the nav's own background transparent; a fill
would blend too. Check that the CTA inside it still reads; give it its own non-blended layer if not.

## The serif word

In a sans headline, the one word doing the work goes in an italic serif, at the same size, often in
the accent colour or a softer tint of the text colour:

```html
<h1>Technology crafted for all.<br />Not <em class="serif">machines</em>.</h1>
```

```css
.serif { font-family: 'Instrument Serif', serif; font-style: italic; font-weight: 400; letter-spacing: -0.01em; }
```

One word per headline. Two and it stops being emphasis.
