# The drawn path

A route, a timeline or a diagram that **inks itself as the visitor scrolls**, with a marker riding the
line and a number counting up beside it. SELENE's trajectory pins for 380svh while four legs of the
Earth-to-Moon flight draw one after another and the distance ticks up to 384,400 km.

## Markup

Draw each leg as its own path, with `pathLength="1"` so every leg is dashed in the same 0–1 units no
matter how long it really is. A faint dashed ghost of the whole route sits underneath.

```html
<section class="stage" id="route" style="height: 380svh" aria-labelledby="route-title">
  <div class="stage__pin">
    <h2 id="route-title">Four days, one line</h2>
    <p class="readout" aria-live="off">Distance flown <span class="km">0</span> km</p>

    <svg viewBox="0 0 1200 600" role="img" aria-label="The flight path, drawn in four legs.">
      <g class="ghost" fill="none" stroke="#fff" stroke-opacity="0.08" stroke-width="1.5" stroke-dasharray="3 6">
        <path d="M230 192 a128 128 0 1 1 -0.1 0" />
        <path d="M336 249 C 520 40, 820 70, 965 216" />
      </g>
      <g class="legs" fill="none" stroke-width="2" stroke-linecap="round">
        <path pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" stroke="var(--line)" d="M230 192 a128 128 0 1 1 -0.1 0" />
        <path pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" stroke="var(--accent)" d="M336 249 C 520 40, 820 70, 965 216" />
      </g>
      <g class="rider"><circle r="11" fill="var(--accent)" opacity="0.25" /><circle r="4.5" fill="#fff" /></g>
    </svg>

    <div class="step" aria-live="polite"><h3 class="step-title"></h3><p class="step-body"></p></div>
  </div>
</section>
```

## Drive it

```js
import { drive } from './scroll-engine.js';
import { clamp, easeOutCubic, range } from './scroll-math.js';

const STEPS = [
  { title: 'Parking orbit', body: 'A lap and a bit around the Earth.' },
  { title: 'The coast', body: 'Three days across the dark.' },
];
const WINDOW = [0.06, 0.92];   // leave a little scroll at each end to arrive and leave
const DISTANCE = 384400;

const stage = document.querySelector('#route');
const legs = [...stage.querySelectorAll('.legs path')];
const rider = stage.querySelector('.rider');
const km = stage.querySelector('.km');
const stepTitle = stage.querySelector('.step-title');
const stepBody = stage.querySelector('.step-body');
let current = -1;

drive(stage, (p) => {
  const u = range(p, ...WINDOW) * legs.length;          // 0 → number of legs
  const active = clamp(Math.floor(u), 0, legs.length - 1);

  legs.forEach((path, i) => {
    const k = easeOutCubic(clamp(u - i));               // each leg draws in its own slice
    path.style.strokeDashoffset = String(1 - k);
    if (i === active) {
      // getTotalLength() is the real length, whatever pathLength says.
      const pt = path.getPointAtLength(path.getTotalLength() * k);
      rider.setAttribute('transform', `translate(${pt.x} ${pt.y})`);
    }
  });

  km.textContent = Math.round(easeOutCubic(clamp(u - 1)) * DISTANCE).toLocaleString('en-US');

  if (active !== current) {
    current = active;
    stepTitle.textContent = STEPS[active].title;
    stepBody.textContent = STEPS[active].body;
  }
});
```

```css
.readout { font-family: var(--font-mono); text-transform: uppercase; letter-spacing: 0.14em; }
.km { font-variant-numeric: tabular-nums; }
```

## Notes

- The counter tracks the leg it belongs to (`u - 1` is the coast), so the number and the line always agree.
- Give the counter `aria-live="off"` (it changes every frame) and the step caption `aria-live="polite"`
  (it changes a few times).
- A step indicator (a row of short bars, filled up to the active leg) gives the visitor a sense of how
  much is left. Colour it with the page's one accent.
- The same pattern draws a process timeline, a supply route, a signature or a floor plan: anything
  with a path and an order.
