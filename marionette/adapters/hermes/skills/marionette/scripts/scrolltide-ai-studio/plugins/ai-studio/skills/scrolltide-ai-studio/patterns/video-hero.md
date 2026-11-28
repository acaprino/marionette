# The looping video hero

The simplest page in the library: one full-bleed looping film behind a hero, copy anchored to a
calm part of the frame, a staggered entrance. Aurora, Monsoon, Glacier and Fluxora are this shape
(Fluxora does its entrance in plain CSS, as below); Visor holds its film in a rounded 16:9 frame
instead. Use it when the page is a single screen, or when the film is ambient rather than something
the visitor drives (for a film the visitor drives, see `film.md`).

## Markup

```html
<section class="hero">
  <video class="hero__film" autoplay muted loop playsinline preload="auto" poster="/media/hero-poster.webp" aria-hidden="true">
    <source src="/media/hero.webm" type="video/webm" />
    <source src="/media/hero.mp4" type="video/mp4" />
  </video>
  <div class="hero__copy">
    <p class="hero__note rise" style="--d: 0.1s">Two commissions open this winter</p>
    <h1 class="hero__title rise" style="--d: 0.2s">Technology crafted for all.<br />Not <em class="serif">machines</em>.</h1>
    <p class="hero__sub rise" style="--d: 0.35s">…</p>
    <div class="hero__cta rise" style="--d: 0.5s"><a class="btn" href="#contact">Book a call</a></div>
  </div>
</section>
```

## The film fades in once it can play

Start the video invisible over the ground colour and fade it in when it can actually play, so the
first paint is never a black box or a half-loaded frame.

```css
.hero { position: relative; min-height: 100svh; overflow: clip; background: var(--ground); }
.hero__film { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; transition: opacity 0.9s cubic-bezier(0.16, 1, 0.3, 1); }
.hero__film.is-ready { opacity: 1; }
.hero__copy { position: relative; z-index: 1; }
```

```js
const film = document.querySelector('.hero__film');
const ready = () => film.classList.add('is-ready');
if (film.readyState >= 3) ready();
else film.addEventListener('canplay', ready, { once: true });
```

## The entrance

One keyframe, staggered by a delay per block. No animation library.

```css
@keyframes rise {
  from { opacity: 0; transform: translate3d(0, 18px, 0); }
  to { opacity: 1; transform: none; }
}
.rise { animation: rise 0.8s cubic-bezier(0.16, 1, 0.3, 1) both; animation-delay: var(--d, 0s); }
@media (prefers-reduced-motion: reduce) {
  .rise { animation: none; }
  .hero__film { transition: none; }
}
```

## Encode the loop

```bash
# H.264, no audio, fast start, 1080p
ffmpeg -i in.mp4 -an -vf "scale=1920:-2" -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p -movflags +faststart public/media/hero.mp4
# VP9 WebM, usually smaller
ffmpeg -i in.mp4 -an -vf "scale=1920:-2" -c:v libvpx-vp9 -b:v 0 -crf 34 -row-mt 1 public/media/hero.webm
# Poster from the first frame
ffmpeg -i public/media/hero.mp4 -frames:v 1 -c:v libwebp -quality 80 public/media/hero-poster.webp
```

Keep a hero loop under about 6 MB. If the first and last frames don't match, cut the loop where they
do, or play the clip forward then reversed and encode that.

## Readability over the film

Choose or generate a film with a calm area where the copy sits for the whole loop, and anchor the
copy there. Move the film (`object-position`) before you dim it. If text still fights the picture, use
a soft text shadow (`0 2px 18px rgb(0 0 0 / 0.4)`) or a gradient only under the copy, never a flat
dark wash over the whole film.
