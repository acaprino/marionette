# Scroll patterns

Working code for the scroll moments the library is built on, written from the free builds' own
source. Vanilla JavaScript, so they drop into any stack; each file notes what changes in React or
Next.js. Every pattern sits on `engine.md`. Read that one first.

| Pattern | File | Reach for it when | In the library |
|---|---|---|---|
| One loop, pinned stages, beats as windows | `engine.md` | Always, for anything the scroll drives | SELENE, NAÏADE |
| Frame-sequence film with speed ramps | `film.md` | The visitor should play a camera move, a turn or a reveal with the scrollbar | NAÏADE |
| Layered stage cut from one render | `layers.md` | You want depth from stills: a scene that parts as you scroll | SELENE hero |
| Path that draws itself, with a rider and a counter | `drawn.md` | A route, a timeline, a process with an order | SELENE trajectory |
| Sideways reel with a focus line | `reel.md` | 3–6 stills or cards to pass through in sequence | SELENE mission log |
| Fit-to-width wordmark, resolving title, live readouts, blended nav, the serif word | `type.md` | Big type, instrument-panel texture, a nav over changing backgrounds | SELENE, NAÏADE, Fluxora |
| Reveals that never leave a blank page | `reveals.md` | Every section between and below the stages | SELENE, NAÏADE |
| Looping video hero with a CSS entrance | `video-hero.md` | A single screen with an ambient film | Fluxora, Aurora, Monsoon, Glacier |

## Combining them

Build a page from **one scroll moment** (a film, a layered stage or a drawn path) plus quiet support:
reveals for the sections below, one type move, readouts if the brand suits an instrument feel. Two
heavy stages can share a page if they're separated by ordinary sections, never in the same viewport.

A typical long page, top to bottom: a layered or film stage (440–600svh), an ordinary section with
reveals, a drawn path or a reel (340–380svh), a section of cards, a closing band with a fitted wordmark.
