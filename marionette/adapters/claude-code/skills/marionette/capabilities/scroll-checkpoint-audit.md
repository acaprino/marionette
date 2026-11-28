---
id: scroll-checkpoint-audit
role: scroll-verification
when: —
after: []
outputs: ["scroll_checkpoints", "scroll_audit_report"]
checks: ["checkpoints_captured_or_disclosed", "blocking_defects_resolved_or_reported", "scroll_progression_verified", "reduced_motion_pass_checked", "recorded_system_respected", "reshot_after_fixes"]
check_conditions: {"checkpoints_captured_or_disclosed": "Playwright and a Chromium-family browser are available; if unavailable, static checks run and visual capture is recorded as not-tested with the reason.", "reshot_after_fixes": "One or more defects were edited in place and a browser was available to capture the page."}
intents: [{"id":"ui.scroll-checkpoint-audit","description":"Verify an existing scroll-driven web page, landing page or scroll animation (whether built with Lenis, GSAP ScrollTrigger, pure CSS scroll timelines or custom code) all the way down the scroll using Playwright checkpoint screenshots (desktop 1440px, phone 390px, first paint and prefers-reduced-motion) and Scrolltide's scroll QA checks: catch script/console/HTTP errors, broken images, unplayable video, sideways overflow, missing h1 webfont, white first-paint flash, hotlinked foreign media and pinned stages stuck between checkpoints; fix blocking scroll defects and re-shoot, or report findings without overriding a recorded design system.","excludes":["Building a new scroll storytelling page from scratch belongs to scroll storytelling; building a standard landing page belongs to visual direction.","Implementing GSAP ScrollTrigger or CSS scroll-timeline code belongs to scroll code (this audit can follow them in the same plan).","Full WCAG AA accessibility auditing and keyboard/focus/state audits belong to design review; frame-by-frame micro-interaction scoring and craft climbs belong to interface polish.","Layout code restructuring for 320px, 200% zoom, RTL and translation growth belongs to layout structure."]}]
tools: [{"name":"file-access","purpose":"Read the built page/code, inspect `report.json` and fix blocking scroll defects in place when edits are requested.","required":true},{"name":"shell","purpose":"Run `<package_root>/scripts/scrolltide-ai-studio/plugins/ai-studio/skills/scrolltide-ai-studio/scripts/scrollshot.mjs` against a dev server URL, single HTML file or build output folder (`dist/`), and install Playwright into the project when missing. `scrollshot.mjs` starts a local 127.0.0.1 HTTP server for files/folders, writes PNG screenshots and `report.json` into the chosen output folder, and loads whatever external URLs the target page itself references; it sends nothing else off the machine.","required":false},{"name":"image-inspection","purpose":"Open and visually inspect every captured desktop, mobile, first-paint and reduced-motion checkpoint PNG.","required":false}]
hooks: []
conflicts: []
reads: ["scroll_page", "page", "code-patch", "scroll-verified", "motion-spec", "reduced-motion", "design_file", "palette", "typography", "constraints"]
---
<!-- Modified by Muro; see LICENSES and NOTICE.md. -->
<!-- Modified by Muro; see LICENSES and NOTICE.md. -->

# Scroll Checkpoint Audit (desktop, mobile and reduced-motion scroll QA)

Checks any scroll-driven page where it actually changes — at checkpoints from 0% to 100% on desktop (1440×900), phone (390×844) and `prefers-reduced-motion: reduce` — using Scrolltide's `checks.md` procedure and Playwright script `scrollshot.mjs`. `<SS>` below stands for `<package_root>/scripts/scrolltide-ai-studio/plugins/ai-studio/skills/scrolltide-ai-studio`.

## Behavior

`<SS>/checks.md` and `<SS>/scripts/scrollshot.mjs` are the full version of this method. Open `<SS>/checks.md` before auditing and `<SS>/house-style.md` only when checking house-style breaks on a page not already governed by another recorded design system. The original wins where this body differs, except for the changes listed under Sources.

1. **Capture the scroll checkpoints.** Run `scrollshot.mjs` from the target project folder against a running dev server URL, a build output folder (`dist/`, `build/`, `out/`) or a single HTML file:
   `node <SS>/scripts/scrollshot.mjs <url | page.html | folder> <out-dir> --reduced`
   For long scroll films or fine beat windows, pass denser stops (`--stops 0,10,20,30,40,50,60,70,80,90,100` or `--stops 30,33,36`). Exit code `1` means `scrollshot.mjs` flagged blocking defects; exit code `2` means Playwright or Chromium is missing (install in the project with `npm i -D playwright && npx playwright install chromium` when permitted, or report clearly that no browser was available and complete static code checks without claiming visual verification).
2. **Resolve blocking defects** (`<SS>/checks.md`, `## 1. Blocking: fix all of these`): script errors, console errors, failed/HTTP >=400 requests, broken images, unplayable `<video>` (`readyState < 2` or error), sideways scroll at desktop or phone width (using the script's culprit list), `<h1>` falling back to a system font because its declared webfont failed to load, white first-paint flash on a dark page (transparent `html`/`body`), failing `npm run build`/`lint`, placeholder or leftover brand copy, and hotlinked foreign media URLs.
3. **Inspect every checkpoint visually** (`<SS>/checks.md`, `## 2. The scroll: look at every checkpoint`): open every PNG in order (desktop, mobile, first paint, reduced motion) and verify:
   - **Progression**: check `sameAsPrevious` in `report.json` — identical neighbouring shots inside a pinned stage mean the stage is stuck (not pinning, loop stopped, or frames missing).
   - **Framing**: subject stays in frame on phone (`m/` portrait cut, focal point, `object-position`).
   - **Readability**: every visible line reads cleanly over film or layers at both widths, with nothing clipped by the viewport or pinned box.
   - **Holds and handoffs**: beat cards/copy land fully in at least one checkpoint (add stops inside the beat window if missed), and after a pinned section ends there is no blank band, seam or colour jump (apron matches the next section).
   - **Reduced motion**: in `reduced-*.png`, every block that should be visible is visible and nothing is stuck waiting on a disabled entrance.
4. **Optional house-style pass** (`<SS>/checks.md`, `## 3. The house style: fix the three worst`): only when the page has no other recorded design system (see Specifics), check against `<SS>/house-style.md` and fix the three worst breaks (multiple accents or coloured card glows, undersized/loose display type, pure `#000`/`#fff` ground where tinted ink/paper fits, competing motion in one viewport, default `ease`/`linear` entrances, vague copy). When another recorded system governs the page, report differences without overwriting them.
5. **Re-shoot and report** (`<SS>/checks.md`, `## 4. Shoot once more` and `## What to report`): if fixes were made and a browser is available, run `scrollshot.mjs` one more time and inspect the new shots. If a blocking defect persists after one fix round (e.g. missing media or unlicensed font), state exactly what and why instead of looping. Record `scroll_checkpoints` (checkpoints inspected, output folder and best desktop/mobile shots, or `not-tested` with reason) and `scroll_audit_report` (script findings, fixes applied, items reported instead of changed, and anything unchecked).

## Output handoff

Resolve `<package_root>` with the `package_root` returned beside these instructions, never against the consumer project. Return both output keys as JSON strings. For a mapped step, submit them through the coordinator's `record` command with the step's `map_id` and `capability`. Read earlier outputs from the step's `recorded_outputs` or `<state_dir>/map.md` only. Do not edit `<state_dir>/map.md` or `<state_dir>/state.json`; the coordinator is their only writer.

## Specifics

- **Respect recorded design systems and review-only requests.** Values tracing to a confirmed project `DESIGN.md` (`design_file`), recorded `palette`, `typography`, `constraints`, `motion-spec` or the client's brand are never overwritten by `house-style.md` step 4: report any conflict instead (one owner per output). If the user explicitly asks for an audit/report without edits, stop after reporting findings and change no files.
- **Engine-agnostic verification.** `scrollshot.mjs` scrolls smoothly in half-screen increments (`requestAnimationFrame` steps) and works on any scroll implementation: Lenis + rAF (`scroll-storytelling`), GSAP ScrollTrigger (`gsap-scrolltrigger`), CSS `animation-timeline` (`css-scroll`), or plain pages (`visual-direction`).
- **What the script needs.** Node.js 18+ and `playwright` (or `playwright-core` with Chrome or Edge installed). Runs locally against `127.0.0.1` for files/folders; does not require `scrolltide-mcp` or any API key.

## Checks

- **checkpoints_captured_or_disclosed**: `scrollshot.mjs` ran across desktop (1440px) and mobile (390px) stops and every shot was inspected, or the report states plainly why no browser capture ran.
- **blocking_defects_resolved_or_reported**: every blocking item in `report.json` (errors, broken images/video, sideways scroll, failed `<h1>` webfont, first-paint flash, hotlinked foreign media) was fixed or explicitly reported with its cause.
- **scroll_progression_verified**: neighbouring checkpoints were checked for `sameAsPrevious` stuck stages, framing, readability, beat holds and section handoffs.
- **reduced_motion_pass_checked**: `--reduced` checkpoints (or static reduced-motion rules when no browser ran) verified that all content remains visible with no blocked entrances.
- **recorded_system_respected**: no confirmed project `DESIGN.md`, recorded `palette`, `typography`, `motion-spec` or `constraints` was overwritten by `house-style.md` fixes.
- **reshot_after_fixes**: after code fixes were applied, `scrollshot.mjs` was re-run and the updated checkpoints were inspected.

## Sources

- AI intent mapping: scrolltide-ai-studio (`checks.md` + `scripts/scrollshot.mjs`) → `ui.scroll-checkpoint-audit`. Separated from `scroll-storytelling` so any scroll-driven page (including GSAP ScrollTrigger and CSS scroll pages) can run multi-checkpoint Playwright scroll verification in the same plan without triggering scroll-engine conflicts.
- Source: scrolltide-ai-studio (scrolltide/ai-studio-skill@5662f4f2, release `v1.0.0`, commit `5662f4f20de1398b1b2c6818b4a64d407662d9e2`, pin `release`; MIT section of root dual `LICENSE`, Copyright (c) 2026 Scrolltide, verified via `license_section`). Packaged under `<package_root>/scripts/scrolltide-ai-studio/plugins/ai-studio/skills/scrolltide-ai-studio/`: `checks.md`, `house-style.md`, `SKILL.source.md` and `scripts/scrollshot.mjs`.
- Relations:
  - `scroll-storytelling` (same-source sibling): `scroll-storytelling` runs `checks.md` + `scrollshot.mjs` inside its own build flow; this capability exposes the same verification standalone for existing pages and other scroll stacks.
  - `gsap-scrolltrigger` and `css-scroll` (complementary downstream): `scroll-checkpoint-audit` reads `code-patch` and `scroll-verified` and verifies desktop/mobile/reduced-motion scroll checkpoints and stuck pins after either scroll-code step. Order: `gsap-scrolltrigger` or `css-scroll` → `scroll-checkpoint-audit`.
  - `visual-direction` (complementary downstream): reads `page`, `palette`, `typography`, `constraints` to run multi-checkpoint scroll QA on built marketing pages while preserving `visual-direction`'s visual system.
  - `design-review` and `interface-polish` (complementary beside): `design-review` owns WCAG AA / keyboard / interaction-state audits; `interface-polish` owns frame-by-frame micro-interaction craft and score climbs; `scroll-checkpoint-audit` owns full-scroll progression, stuck-pin detection, sideways overflow and first-paint/media checks across scroll stops.
  - `design-file` (authority upstream via `reads: ["design_file"]`): confirmed `DESIGN.md` tokens are respected and never overwritten by `house-style.md` fixes.
- Changes for coexistence (ADR-0017):
  - `checks.md` step 3 ("fix the three worst breaks from `house-style.md`") is scoped so it never overwrites a confirmed project `DESIGN.md` or another capability's recorded `palette`, `typography`, `motion-spec` or `constraints` (one owner per output; package look-authority rule of 2026-11-17): conflicts are reported instead.
  - Report-only requests are supported by stopping before edits, matching the package's audit/fix distinction.
  - Output keys (`scroll_checkpoints`, `scroll_audit_report`) and `check_conditions` are this package's evidence contract.
- Runtime dependencies: Node.js 18+ and Playwright (`npm i -D playwright && npx playwright install chromium`, or `playwright-core` + Chrome/Edge). No API key and no `scrolltide-mcp` needed.
- Hooks: none in the selected files.
- Harmonized by: prompts/harmonizer.md (2026-11-28 intake of scrolltide-ai-studio v1.0.0, MIT part).
