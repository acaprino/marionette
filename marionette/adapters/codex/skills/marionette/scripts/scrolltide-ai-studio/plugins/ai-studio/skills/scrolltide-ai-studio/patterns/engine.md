# The scroll engine

Every other pattern in this folder sits on this one. It is how SELENE and NAÏADE run: **one
`requestAnimationFrame` loop for the whole page**. Lenis advances first, then each scroll-driven
section reads its own position and writes styles straight onto its elements. Nothing goes through
framework state while scrolling, so the page never re-renders mid-scroll.

## Helpers

```js
// scroll-math.js
export const clamp = (v, min = 0, max = 1) => Math.min(max, Math.max(min, v));
export const lerp = (a, b, t) => a + (b - a) * t;
/** Where v sits between a and b, clamped to 0–1. The unit every beat is written in. */
export const range = (v, a, b) => clamp((v - a) / (b - a));
export const smoothstep = (t) => t * t * (3 - 2 * t);
export const easeOutCubic = (t) => 1 - (1 - t) ** 3;

/**
 * Progress through a tall section whose child is position: sticky.
 * 0 when the section's top meets the viewport top, 1 when the pinned child is about to unpin.
 */
export function pinProgress(el) {
  const rect = el.getBoundingClientRect();
  const vh = window.innerHeight;
  return { p: clamp(-rect.top / Math.max(1, rect.height - vh)), rect, vh };
}
```

## The loop

```js
// scroll-engine.js
import Lenis from 'lenis'; // npm i lenis
import { pinProgress } from './scroll-math.js';

const subscribers = new Set();
let lenis = null;

/** Start once, at app start. Returns a stop function. */
export function startScroll() {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Smoothing is the only change to how the page scrolls, and reduced motion turns it off.
  if (!reduced) lenis = new Lenis({ lerp: 0.09, smoothWheel: true, wheelMultiplier: 0.9 });

  let raf = 0;
  const loop = (time) => {
    lenis?.raf(time);
    subscribers.forEach((fn) => fn(time));
    raf = requestAnimationFrame(loop);
  };
  raf = requestAnimationFrame(loop);
  return () => {
    cancelAnimationFrame(raf);
    lenis?.destroy();
    lenis = null;
  };
}

export function onFrame(fn) {
  subscribers.add(fn);
  return () => subscribers.delete(fn);
}

/**
 * Run render(p) for one pinned section, only while it's on screen and only when its
 * progress actually moved. This guard is what keeps a long page cheap.
 */
export function drive(section, render) {
  let last = -1;
  return onFrame(() => {
    const { p, rect, vh } = pinProgress(section);
    if (rect.bottom < 0 || rect.top > vh) return;
    if (Math.abs(p - last) < 0.00005) return;
    last = p;
    render(p, rect, vh);
  });
}

/** In-page links go through Lenis so they glide instead of jumping. */
export function scrollToTarget(hashOrY) {
  const target = typeof hashOrY === 'number' ? hashOrY : document.querySelector(hashOrY);
  if (target == null) return;
  if (lenis) lenis.scrollTo(target, { duration: 1.6 });
  else if (typeof target === 'number') window.scrollTo({ top: target });
  else target.scrollIntoView();
}
```

No build step? Load Lenis from a pinned CDN build and use `window.Lenis`:
`<script src="https://unpkg.com/lenis@1.3.11/dist/lenis.min.js"></script>`, plus its stylesheet
`https://unpkg.com/lenis@1.3.11/dist/lenis.css`.

## A pinned stage

```html
<section class="stage" id="earthrise" style="height: 440svh">
  <div class="stage__pin">
    <!-- layers, canvas, copy: everything the scroll moves -->
  </div>
</section>
```

```css
.stage { position: relative; }
.stage__pin { position: sticky; top: 0; height: 100svh; overflow: hidden; }
```

```js
import { drive } from './scroll-engine.js';
import { easeOutCubic, lerp, range } from './scroll-math.js';

const stage = document.querySelector('#earthrise');
const title = stage.querySelector('.title');

drive(stage, (p) => {
  const tIn = easeOutCubic(range(p, 0.08, 0.24));
  const tOut = range(p, 0.42, 0.52);
  title.style.opacity = String(tIn * (1 - tOut));
  title.style.transform = `translate3d(0, ${-p * 6}vh, 0)`;
});
```

## Write beats as windows

A section's choreography is a list of **windows of progress**, written once at the top of the file
with a comment per beat. Change a window and you know exactly which beat moved.

```js
// 0.00–0.18  dust clears off the lens
// 0.04–0.50  the subject climbs into frame
// 0.10–0.50  the title resolves
// 0.70–1.00  everything lifts away; the ground's apron fills the screen
const BEATS = { dust: [0, 0.18], rise: [0.04, 0.5], title: [0.1, 0.5], exit: [0.7, 1] };
```

Inside a window, ease with `easeOutCubic` (arrives and settles) or `smoothstep` (eases both ends).
Never add a CSS `transition` to a property the loop writes: the two fight and the motion lags.

## Discrete changes

When scroll crosses into a new step (a new leg, a new chapter label), update the DOM **only when the
index changes**, not every frame:

```js
let current = -1;
drive(section, (p) => {
  const step = Math.min(STEPS.length - 1, Math.floor(range(p, 0.06, 0.92) * STEPS.length));
  if (step !== current) {
    current = step;
    label.textContent = STEPS[step].title;
  }
});
```

## In React and Next.js

- Call `startScroll()` once in a top-level `useEffect` and return its stop function.
- Each section subscribes in its own `useEffect` with `drive(ref.current, …)` and returns the
  unsubscribe. Elements are reached through refs; styles are written to `ref.current.style`.
- `useState` only for discrete steps, set only when the index changes (as above).
- Next.js App Router: the engine and every scroll section are client components (`'use client'`).
  Start the loop in a client component mounted once in the root layout.

## Pitfalls

- **Sticky dies under `overflow: hidden`.** Any ancestor with `overflow: hidden | auto | scroll`
  becomes the scroll container and the pin stops pinning. To stop sideways scroll, put
  `overflow-x: clip` on `html, body`: it clips without creating a scroll container.
- **A `transform` on an ancestor** also changes what `position: sticky` and `fixed` attach to.
- **Use `svh` for stage heights** (`440svh`), not `vh`, so mobile browser bars don't change the
  stage length mid-scroll. The pinned child uses `100svh`.
- **Don't read layout inside a write.** Read every rect first, then write every style, within a frame.
- **Reduced motion keeps the mapping.** The page still moves with the scrollbar (the visitor is
  driving it), but without Lenis smoothing, and any ambient drift stops.
