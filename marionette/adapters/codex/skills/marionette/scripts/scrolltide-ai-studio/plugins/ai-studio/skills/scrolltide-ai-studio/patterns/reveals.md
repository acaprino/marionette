# Reveals

The quiet entrance for everything below and between the pinned stages. Mark an element with
`data-reveal`; the first time it's seen it gets `.is-in`, and CSS does the rest.

## Visible without JavaScript

Hide reveal targets only once script has run. Put this first in `<head>`, before any stylesheet:

```html
<script>document.documentElement.classList.add('js')</script>
```

```css
.js [data-reveal] {
  opacity: 0;
  transform: translate3d(0, 24px, 0);
  transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  transition-delay: calc(var(--i, 0) * 70ms);
}
.js [data-reveal].is-in { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) {
  .js [data-reveal] { opacity: 1; transform: none; transition: none; }
}
```

Stagger siblings with an index: `<li data-reveal style="--i: 2">`.

## The observer

```js
/** Watches [data-reveal] inside root, including elements added later. Returns stop(). */
export function watchReveals(root = document) {
  if (!('IntersectionObserver' in window)) {
    // No observer, no hiding: show everything at once.
    root.querySelectorAll('[data-reveal]').forEach((el) => el.classList.add('is-in'));
    return () => {};
  }
  const io = new IntersectionObserver(
    (entries) => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        e.target.classList.add('is-in');
        io.unobserve(e.target); // once; never replays on the way back up
      }
    },
    { rootMargin: '0px 0px -10% 0px' },
  );
  const watch = () => root.querySelectorAll('[data-reveal]:not(.is-in)').forEach((el) => io.observe(el));
  watch();
  // Pick up anything rendered later (client routing, lazy sections, hot reload).
  const mo = new MutationObserver(watch);
  mo.observe(root === document ? document.body : root, { childList: true, subtree: true });
  return () => {
    mo.disconnect();
    io.disconnect();
  };
}
```

In React, give each section its own `watchReveals(ref.current)` in a `useEffect`, so a section that
mounts late is never left hidden.

## Notes

- Release the transform when the entrance ends if the element also has a hover transform: the
  `.is-in` rule sets `transform: none`, so hover rules on the element itself still apply.
- Elements inside a pinned stage don't use reveals; the stage's own progress drives them.
- If script fails before `watchReveals` runs, the `js` class is still set and targets stay hidden.
  Load the reveal code early, or add a 2-second fallback that marks every target `.is-in`.
