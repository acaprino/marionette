# The scroll film

A film the visitor plays with the scrollbar: a camera move, a product turning, a reveal. It's
NAÏADE's whole page, and 62 of the library's builds use a frame sequence.

**Frames, not `<video>`.** Scrubbing a video means writing `currentTime` on every tick, and the
browser answers with asynchronous seeks that drop or bunch up under fast scrolling. A decoded frame
is an array index and one `drawImage`. Re-encode the frames as a video and the scrub turns to mush.

## 1. Make the frames

Start from one continuous shot (generated or filmed): no cuts, a slow move, the subject held in
frame. 12–20 seconds at 24 fps gives 290–480 frames, which is the range the library ships.

```bash
mkdir -p public/frames/d public/frames/m

# d = landscape cut, 1600 wide
ffmpeg -i film.mp4 -vf "fps=24,scale=1600:-2" \
  -c:v libwebp -quality 72 -compression_level 6 -f image2 public/frames/d/f%03d.webp

# m = portrait cut for phones: a 9:16 window around the subject (0.5 = centred), 720 wide
ffmpeg -i film.mp4 -vf "fps=24,crop=ih*9/16:ih:(iw-ih*9/16)*0.5:0,scale=720:-2" \
  -c:v libwebp -quality 70 -compression_level 6 -f image2 public/frames/m/f%03d.webp
```

Aim for 15–40 KB a frame. If the portrait crop loses the subject partway through, cut `m` with a
moving crop, or render the film twice, once at each aspect.

## 2. Load coarse to fine

Load the resting frames first, then every 32nd frame, every 16th, and so on, six at a time, so a
fast scroller always has a neighbour on screen. Keep `HTMLImageElement`s, not `ImageBitmap`s: a
bitmap pins its decoded pixels (about 5.7 MB at 1600×900), and 480 of them will crash a phone.

```js
// frames.js
export const FPS = 24;

export function frameUrl(set, i) {
  return `/frames/${set}/f${String(i + 1).padStart(3, '0')}.webp`;
}

function loadOrder(count, priority) {
  const seen = new Set();
  const order = [];
  const push = (i) => {
    if (i < 0 || i >= count || seen.has(i)) return;
    seen.add(i);
    order.push(i);
  };
  priority.forEach(push);
  for (let stride = 32; stride >= 1; stride /= 2) for (let i = 0; i < count; i += stride) push(i);
  push(count - 1);
  return order;
}

function loadOne(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.decoding = 'async';
    img.onerror = () => reject(new Error(`Failed to load ${src}`));
    img.src = src;
    img.decode().then(() => resolve(img), () => (img.complete ? resolve(img) : (img.onload = () => resolve(img))));
  });
}

/** Streams the set coarse-to-fine. onFrame(i, img) fires as each lands. Returns cancel(). */
export function loadFrames(set, count, priority, onFrame) {
  const queue = loadOrder(count, priority);
  let cancelled = false;
  const worker = async () => {
    while (!cancelled && queue.length) {
      const i = queue.shift();
      try {
        const img = await loadOne(frameUrl(set, i));
        if (!cancelled) onFrame(i, img);
      } catch {
        // A missing frame just means its neighbour gets painted instead.
      }
    }
  };
  // The first frame alone, so it paints before anything competes with it.
  const first = queue.shift();
  loadOne(frameUrl(set, first))
    .then((img) => !cancelled && onFrame(first, img))
    .catch(() => {})
    .finally(() => {
      for (let k = 0; k < 6; k++) worker();
    });
  return () => (cancelled = true);
}
```

## 3. Paint the nearest frame, cropped around the subject

```js
// film.js
import { clamp } from './scroll-math.js';

export function nearest(frames, i) {
  if (frames[i]) return frames[i];
  for (let d = 1; d < frames.length; d++) {
    if (frames[i - d]) return frames[i - d];
    if (frames[i + d]) return frames[i + d];
  }
  return null;
}

/** object-fit: cover, but with the focal point (fx, fy as 0–1 of the image) kept in view. */
export function drawCover(ctx, img, w, h, fx = 0.5, fy = 0.5) {
  const s = Math.max(w / img.naturalWidth, h / img.naturalHeight);
  const dw = img.naturalWidth * s;
  const dh = img.naturalHeight * s;
  const dx = clamp(w / 2 - fx * dw, w - dw, 0);
  const dy = clamp(h / 2 - fy * dh, h - dh, 0);
  ctx.drawImage(img, dx, dy, dw, dh);
}

export function sizeCanvas(canvas) {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = Math.round(canvas.clientWidth * dpr);
  canvas.height = Math.round(canvas.clientHeight * dpr);
}
```

## 4. Map scroll to film time, with speed ramps

A straight line from progress to frame makes every part of the film take the same scroll. A film
reads better when it **holds** on the beats that matter and **travels** between them. Write the beats
as `[progress, film seconds]` pairs and interpolate them with a monotone cubic, which eases every
ramp and can never run the film backwards while the visitor scrolls forwards.

```js
// time-remap.js: monotone cubic (Fritsch–Carlson) through [u, seconds] beats
export function createRemap(beats) {
  const n = beats.length;
  const xs = beats.map((b) => b[0]);
  const ys = beats.map((b) => b[1]);
  const d = [];
  for (let i = 0; i < n - 1; i++) d.push((ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]));
  const m = new Array(n);
  m[0] = d[0];
  m[n - 1] = d[n - 2];
  for (let i = 1; i < n - 1; i++) m[i] = d[i - 1] * d[i] <= 0 ? 0 : (d[i - 1] + d[i]) / 2;
  for (let i = 0; i < n - 1; i++) {
    if (d[i] === 0) {
      m[i] = m[i + 1] = 0;
      continue;
    }
    const a = m[i] / d[i];
    const b = m[i + 1] / d[i];
    const s = a * a + b * b;
    if (s > 9) {
      const t = 3 / Math.sqrt(s);
      m[i] = t * a * d[i];
      m[i + 1] = t * b * d[i];
    }
  }
  return (u) => {
    const x = Math.min(xs[n - 1], Math.max(xs[0], u));
    let i = 0;
    while (i < n - 2 && x > xs[i + 1]) i++;
    const h = xs[i + 1] - xs[i];
    const t = (x - xs[i]) / h;
    const t2 = t * t;
    const t3 = t2 * t;
    return (2 * t3 - 3 * t2 + 1) * ys[i] + (t3 - 2 * t2 + t) * h * m[i] + (-2 * t3 + 3 * t2) * ys[i + 1] + (t3 - t2) * h * m[i + 1];
  };
}
```

A flat pair (`[0.39, 10]` after `[0.25, 10]`) is a hold: the film stops on second 10 while the
visitor scrolls from 0.25 to 0.39. That's where a product card or a line of copy sits.

## 5. Wire it up

```html
<section class="stage" id="film" style="height: 600svh">
  <div class="stage__pin">
    <canvas class="film" aria-hidden="true"></canvas>
    <!-- copy and cards that arrive on the holds -->
  </div>
</section>
```

```css
.film { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
```

```js
import { drive } from './scroll-engine.js';
import { FPS, loadFrames } from './frames.js';
import { drawCover, nearest, sizeCanvas } from './film.js';
import { createRemap } from './time-remap.js';

const COUNT = 481;
const BEATS = [
  [0, 0],
  [0.06, 0],   // hero holds while its copy leaves
  [0.17, 5],   // travel
  [0.25, 10],  // fast push in
  [0.39, 10],  // hold: card 01
  [0.73, 20],  // travel
  [0.87, 20],  // hold: card 02
  [1, 20],
];
const at = createRemap(BEATS);

const stage = document.querySelector('#film');
const canvas = stage.querySelector('.film');
const ctx = canvas.getContext('2d');
const set = innerWidth / innerHeight < 0.8 ? 'm' : 'd';
const frames = new Array(COUNT);
let lastIndex = -1;

const paint = (i) => {
  const img = nearest(frames, i);
  if (!img) return;
  drawCover(ctx, img, canvas.width, canvas.height);
};

sizeCanvas(canvas);
new ResizeObserver(() => {
  sizeCanvas(canvas);
  paint(Math.max(0, lastIndex));
}).observe(canvas);

loadFrames(set, COUNT, [0], (i, img) => {
  frames[i] = img;
  if (i === lastIndex || lastIndex === -1) paint(Math.max(0, lastIndex));
});

drive(stage, (p) => {
  lastIndex = Math.min(COUNT - 1, Math.round(at(p) * FPS));
  paint(lastIndex);
});
```

## 6. Hold the page until the film can scrub

Lift the preloader once a **spread** of frames has decoded (every 16th, say, so about 30 frames
across the whole film), not the whole sequence, and give up after 6 seconds rather than hold a slow
connection hostage. Keep the first frame painted behind the preloader so lifting it reveals a picture.

## Keep the subject in view

When copy or a card takes part of the screen, track where the subject sits in the frame over time as
`[seconds, fx, fy]` keyframes, interpolate them, and pass them to `drawCover`. On phones the same
track steers the portrait crop. That is how NAÏADE keeps the jewel visible beside each product card.

## Checks

- Scroll fast from top to bottom: no blank frames, no flashes of the wrong frame.
- Scroll slowly through each hold: the film stops while the copy is up.
- Throttle the network to Fast 3G: the preloader lifts within 6 seconds and the scrub still works.
- On a phone, the `m` set loads, not `d`.
