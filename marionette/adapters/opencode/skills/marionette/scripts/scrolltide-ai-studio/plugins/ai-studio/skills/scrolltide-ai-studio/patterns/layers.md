# The layered stage

Depth without a film or WebGL: **one render cut into layers**, stacked and pinned, each moved at its
own rate by the scroll. SELENE's hero is six layers (sky, Earth, moonscape, crater rim, astronaut,
ground) over 440svh: the Earth climbs out from behind the horizon while the foreground rises past it.

## 1. Cut the layers from one picture

- Start from **one** wide render (SELENE's is 2688×1520). Every layer is that same canvas size, with
  everything except its own element transparent. Because they share one frame, they stay registered
  at every viewport.
- Order far to near: backdrop, subject, middle ground, frame or foreground, figure, ground.
- Make a portrait set (`m/`) from a portrait render or a recomposed crop, and a landscape set (`d/`).
- WebP with alpha. The far layer can be lossy and small; near layers carry the detail.

## 2. Stack them with one shared crop

```html
<section class="stage" id="rise" style="height: 440svh">
  <div class="stage__pin">
    <div class="layer" data-layer="sky"><picture>
      <source media="(max-width: 767px)" srcset="/layers/m/sky.webp" />
      <img src="/layers/d/sky.webp" alt="" aria-hidden="true" fetchpriority="high" decoding="async" />
    </picture></div>
    <div class="layer" data-layer="subject">…</div>
    <div class="layer" data-layer="midground">…</div>

    <h1 class="stage-title">Watch the Earth rise</h1> <!-- sits between mid and near layers -->

    <div class="layer" data-layer="foreground">…</div>
    <div class="layer" data-layer="ground">…<div class="apron"></div></div>
  </div>
</section>
```

```css
.layer { position: absolute; inset: 0; will-change: transform; }
/* One crop for every layer, or they drift apart at some viewport. */
.layer img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 58% 50%; }
@media (min-width: 768px) { .layer img { object-position: center; } }
/* The ground carries a block of the next section's colour, so when it climbs it fills the
   screen and hands straight over to the page below. */
.apron { position: absolute; left: 0; right: 0; top: 100%; height: 110vh; background: var(--ground); }
```

Place the title **in the stack**, between the middle and near layers, so the foreground passes in
front of it. That one choice is most of what makes the scene read as space instead of a picture.

## 3. Move far slowly, near fast

```js
import { drive } from './scroll-engine.js';
import { clamp, easeOutCubic, lerp, range } from './scroll-math.js';

const stage = document.querySelector('#rise');
const L = Object.fromEntries([...stage.querySelectorAll('[data-layer]')].map((el) => [el.dataset.layer, el]));
const title = stage.querySelector('.stage-title');

const set = (name, y, scale = 1, opacity = 1) => {
  const el = L[name];
  el.style.transform = `translate3d(0, ${y}vh, 0) scale(${scale})`;
  el.style.opacity = String(opacity);
};

drive(stage, (p) => {
  const settle = easeOutCubic(range(p, 0, 0.5));
  const exit = range(p, 0.7, 1);

  set('sky', lerp(0, -6, p), lerp(1.14, 1, settle));                 // barely moves, settles from 1.14
  const rise = easeOutCubic(range(p, 0.04, 0.5));
  set('subject', lerp(34, 0, rise) - exit * 12, lerp(0.92, 1, rise)); // climbs into place
  set('midground', lerp(9, 0, settle) - exit * 26);
  const rim = easeOutCubic(range(p, 0.28, 0.58));
  set('foreground', -exit * 44, lerp(1.6, 1, rim), rim);              // closes in around the view
  const up = easeOutCubic(range(p, 0.34, 0.6));
  set('ground', lerp(36, 0, up) - exit * 78);                         // nearest, fastest on the exit

  const tIn = easeOutCubic(range(p, 0.08, 0.24));
  title.style.opacity = String(tIn * (1 - range(p, 0.42, 0.52)));
  title.style.letterSpacing = `${lerp(0.6, 0.24, tIn)}em`;            // tracking closes as it resolves
  title.style.filter = tIn < 0.99 ? `blur(${(1 - tIn) * 10}px)` : '';
});
```

The exit multipliers grow from far to near (12, 26, 44, 78): on the way out, near layers leave
fastest, so the scene tilts away rather than sliding off as one sheet.

## Notes

- Units are `vh` so the motion scales with the screen. Keep each layer's travel under its own
  transparent margin, or its edge shows.
- `will-change: transform` on the layers only, never on the section.
- Reduced motion: keep the mapping (it's driven by the scrollbar) but skip any ambient drift, such as
  dust or a slow float, that would run on its own.
- Decorative layers get `alt=""` and `aria-hidden="true"`; the section gets an `aria-label`.
