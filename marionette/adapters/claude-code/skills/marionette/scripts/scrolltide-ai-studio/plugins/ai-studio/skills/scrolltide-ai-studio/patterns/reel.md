# The sideways reel

Vertical scrolling slides a row of frames sideways while the section is pinned. The frame nearest a
focus line is sharp and full size; the rest dim and shrink by distance; each picture drifts against
its frame as it passes. SELENE's mission log runs four stills over 340svh.

## Markup

```html
<section class="stage" id="log" style="height: 340svh" aria-labelledby="log-title">
  <div class="stage__pin reel">
    <div class="reel__intro">
      <p class="eyebrow">Mission log</p>
      <h2 id="log-title">Four days in four frames</h2>
      <p class="reel__count" aria-hidden="true"><span class="now">01</span> / 04 <span class="bar"><span></span></span></p>
    </div>
    <ol class="reel__track">
      <li class="reel__card">
        <figure>
          <div class="reel__frame"><img src="/media/launch.webp" alt="Launch: the stack clears the tower." width="840" height="1120" loading="lazy" decoding="async" /></div>
          <figcaption>01 · Launch</figcaption>
        </figure>
      </li>
      <!-- … -->
    </ol>
  </div>
</section>
```

```css
.reel { display: flex; align-items: center; }
.reel__intro { flex: none; width: 32vw; padding-left: 6vw; padding-right: 2.5rem; position: relative; z-index: 1; }
.reel__track { display: flex; gap: 1.75rem; will-change: transform; list-style: none; margin: 0; padding: 0; }
.reel__card { flex: none; width: clamp(16rem, 24vw, 23rem); transform-origin: bottom; }
.reel__frame { aspect-ratio: 3 / 4; overflow: hidden; border-radius: 6px; }
.reel__frame img { width: 100%; height: 100%; object-fit: cover; will-change: transform; }
.bar { display: inline-block; position: relative; width: 8rem; height: 1px; background: rgb(255 255 255 / 0.15); vertical-align: middle; }
.bar > span { position: absolute; inset: 0; background: var(--accent); transform-origin: left; transform: scaleX(0); }
@media (max-width: 767px) {
  .reel { flex-direction: column; align-items: stretch; justify-content: center; }
  .reel__intro { width: auto; padding: 0 1rem; }
  .reel__track { margin-top: 2rem; padding-left: 1rem; gap: 1.25rem; }
  .reel__card { width: 70vw; }
}
```

## Drive it

```js
import { drive } from './scroll-engine.js';
import { clamp, range } from './scroll-math.js';

const stage = document.querySelector('#log');
const track = stage.querySelector('.reel__track');
const cards = [...stage.querySelectorAll('.reel__card')];
const imgs = cards.map((c) => c.querySelector('img'));
const bar = stage.querySelector('.bar > span');
const now = stage.querySelector('.now');
const FOCUS = 0.62; // focus line, as a fraction of the viewport width (right of centre)

drive(stage, (p) => {
  const vw = innerWidth;
  const k = range(p, 0.04, 0.96);
  // offsetLeft is the untransformed layout position, so it stays stable while the track moves.
  const travel = Math.max(0, track.offsetLeft + track.scrollWidth - vw * 0.94);
  track.style.transform = `translate3d(${-k * travel}px, 0, 0)`;

  let nearest = 0;
  let best = Infinity;
  const rects = cards.map((c) => c.getBoundingClientRect()); // read everything, then write
  rects.forEach((r, i) => {
    const off = (r.left + r.width / 2 - vw * FOCUS) / vw;
    const a = clamp(Math.abs(off) * 1.6);
    cards[i].style.opacity = String(1 - a * 0.55);
    cards[i].style.transform = `scale(${1 - a * 0.07})`;
    imgs[i].style.transform = `translate3d(${off * -60}px, 0, 0) scale(1.15)`; // picture drifts in its frame
    if (Math.abs(off) < best) {
      best = Math.abs(off);
      nearest = i;
    }
  });
  bar.style.transform = `scaleX(${k})`;
  now.textContent = String(nearest + 1).padStart(2, '0');
});
```

## Notes

- Section length decides speed: about 80–90svh of scroll per card feels unhurried. Four cards at
  340svh is SELENE's pace.
- The `scale(1.15)` on each picture gives it room to drift without showing an edge.
- Real `alt` text on each still: these are content, not decoration.
- Reduced motion: the slide stays (it's the scrollbar), the inner drift can go.
- Keyboard and screen-reader users get a normal ordered list; nothing in the reel needs a pointer.
