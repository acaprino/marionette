# Marionette 0.8.0

Marionette absorbs the MIT-licensed part of scrolltide/ai-studio-skill (v1.0.0, verified via ADR-0038 `license_section`; the nine proprietary `library/*.md` builds are excluded and declared in `omissions`) as two new on-demand capabilities:

- `scroll-storytelling` (in `marionette-web-design`, absorbing `scrolltide-ai-studio`): builds scroll-driven storytelling pages, cinematic heroes and pinned scroll stages around one scroll moment using Lenis + single rAF loop, `patterns/**` and `house-style.md` (or a connected remote Scrolltide MCP), or generates full-source builder handoff prompts (`handoff.md`). Conflicts with `aesthetic-direction`, `gsap-scrolltrigger` and `css-scroll`; reads `offer`, `page_outline`, `design_file` and `motion-spec` so `visual-direction` (`ui.landing-strategy`) can precede it.
- `scroll-checkpoint-audit` (in `marionette-motion`, no conflicts): runs engine-agnostic Playwright QA via `checks.md` and `scripts/scrollshot.mjs` at 0–100% scroll checkpoints on desktop, phone and `prefers-reduced-motion`, working downstream of GSAP, CSS scroll or `visual-direction` without overwriting confirmed `DESIGN.md` or recorded systems.

Also includes the Muro 0.11.5+ rebuild (auto-injected Muro system section with trivial-edit exception, Windows PowerShell launcher allowlist, full composed system prompt in `GUIDE.html`), the Ponytail-to-design boundary in session policy, refined `interaction-motion` exclusion, and re-pinning `charles-skills` to head `a24c5f2c` (`skills/drops/charles-ux-animation` moved to `skills/design/charles-ux-animation` and updated to six questions: ease-out on exits too, press scale `0.97`, 40–70ms copy stagger, 2px blur icon swaps, warm tooltip groups).

The catalog grows from 43 to 45 capabilities and from 18 to 19 sources; nothing new acts in every session beyond the Ponytail-to-design boundary line, and no hook or MCP server is registered.

Not executed: no live host session was run on the 0.8.0 build with `scrolltide-ai-studio`, and no routing eval was scored against a model.

- Adds the input scrolltide-ai-studio (v1.0.0).
- Moves charles-skills from commit 83de509 to commit a24c5f2.
- New capabilities: scroll-checkpoint-audit, scroll-storytelling.
- The catalog is 45 capabilities from 19 inputs.

Released from `marionette.mp` (SHA-256 `e1ad2f236cf98f12a33d0c3d59fd5cdacc879f062adca891ef744d3407484efc`) as pushed to acaprino/marionette at commit `3da45d8a1c5ce3b0afaa19b1806923323558b351`; the store was written by Muro at commit `c1d40338fd0d48010366381d1263779033ddb547`.
