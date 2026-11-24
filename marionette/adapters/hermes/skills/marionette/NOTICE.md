Marionette v0.6.0 — Aggregated NOTICE

The following upstream works are adapted and merged into Marionette:

- motion-design — MIT (see LICENSES/motion-design.txt)
  Copyright (c) 2025 LottieFiles
  Modified and merged into Marionette.

- gsap-scrolltrigger — MIT (see LICENSES/gsap-scrolltrigger.txt)
  Copyright (c) 2026 GreenSock
  Modified and merged into Marionette.

- wayfinder — MIT (see LICENSES/wayfinder.txt)
  Copyright (c) 2026 Matt Pocock
  Modified and merged into Marionette.

- ai-design-skills — MIT (see LICENSES/ai-design-skills.txt)
  Copyright (c) 2026 Elaya
  Modified and merged into Marionette.

- ui-ux-pro-max — MIT (see LICENSES/ui-ux-pro-max.txt)
  Copyright (c) 2024 Next Level Builder
  Modified and merged into Marionette.

- genoffice — Apache-2.0 (see LICENSES/genoffice.txt)
  Copyright 2026 Mainfunc, Inc.
  Modified and merged into Marionette.
GenOffice
Copyright 2026 Mainfunc, Inc.

This product includes software developed at Mainfunc, Inc.

Bundled third-party components are listed in THIRD-PARTY-NOTICES.txt, which
tools/gen-third-party-notices.mjs generates at packaging time. It is not
checked into this repository; in a release build it ships inside the
application bundle (Contents/Resources on macOS, resources/ on Windows).
Run `node tools/gen-third-party-notices.mjs` to produce it from a source
checkout.

Bundled fonts and their licenses are documented in
apps/docs/src/renderer/fonts/README.md.

Downloadable fonts

Any app can offer additional font families, at the reader's request, from the
build-injected font mirror. Those families are not in the bundle and so are not
in that README; the catalogue is
packages/electron-utils/src/font-catalog.ts, and every family there carries its
SPDX licence id in a `license` field, checked against a permissive allowlist by
packages/electron-utils/tests/font-store.test.ts.

All of them are licensed under the SIL Open Font License, Version 1.1
(https://openfontlicense.org), which permits the bundling and redistribution
this application performs. The families are: Open Sans, Roboto, Lato,
Montserrat, Poppins, Inter, Source Sans 3, Oswald, Raleway, Nunito,
Merriweather, Playfair Display, Work Sans, Rubik, Noto Sans JP, Noto Sans KR,
Noto Sans SC, Noto Sans TC, Nanum Gothic, Noto Serif SC, Noto Serif TC,
Noto Serif JP, Noto Serif KR, Nanum Myeongjo.

Each downloaded file is verified against the sha256 recorded in the catalogue
before it is installed, and the catalogue states each family's size so an app
can ask before fetching tens of megabytes.

Unicode Character Database

apps/pdf/src/shared/radicals.ts contains a generated mapping derived from
Unicode Character Database 17.0.0, EquivalentUnifiedIdeograph.txt
(2025-08-01):
https://www.unicode.org/Public/17.0.0/ucd/EquivalentUnifiedIdeograph.txt

Copyright © 1991-2026 Unicode, Inc. This data is distributed under Unicode
License v3. The complete copyright and permission notice is reproduced in
LICENSE-UNICODE.txt.

Office Open XML schemas

tools/ooxml-validate/schemas contains the ISO/IEC 29500-4:2016 (ECMA-376
Part 4, Transitional) XML Schema files for PresentationML and DrawingML, as
distributed in the python-docx repository (ref/xsd), with one marked local
amendment (see tools/ooxml-validate/README.md). They are used only by tests
and development tooling and are not shipped in the application.


- explain-this — MIT (see LICENSES/explain-this.txt)
  Copyright (c) 2026 analyticalmonk
  Modified and merged into Marionette.

- open-paper-skills — MIT (see LICENSES/open-paper-skills.txt)
  Copyright (c) 2026 pengqianhan
  Modified and merged into Marionette.

- tokeneconomizer — Apache-2.0 (see LICENSES/tokeneconomizer.txt)
  Modified and merged into Marionette.

- claude-design-system-prompt — MIT (see LICENSES/claude-design-system-prompt.txt)
  Copyright (c) 2026 Trystan Sarrade
  Modified and merged into Marionette.

- ponytail — MIT (see LICENSES/ponytail.txt)
  Copyright (c) 2026 DietrichGebert
  Modified and merged into Marionette.

- i-have-adhd — MIT (see LICENSES/i-have-adhd.txt)
  Copyright (c) 2026 Ayoub Ghriss
  Modified and merged into Marionette.

- egm — Apache-2.0 (see LICENSES/egm.txt)
  Modified and merged into Marionette.

- superpowers — MIT (see LICENSES/superpowers.txt)
  Copyright (c) 2025 Jesse Vincent
  Modified and merged into Marionette.

- zero-slop-design — MIT (see LICENSES/zero-slop-design.txt)
  Copyright (c) 2026 zero-slop-design contributors
  Modified and merged into Marionette.
  Third-party notices for material included in this source: scripts/zero-slop-design/THIRD_PARTY_NOTICES.md

- text-humanizer — MIT (see LICENSES/text-humanizer.txt)
  Copyright (c) 2025 Alfio
  Modified and merged into Marionette.
  Third-party notices for material included in this source: scripts/text-humanizer/skills/humanize/references/upstream-license.txt

- better-layout — MIT (see LICENSES/better-layout.txt)
  Copyright (c) 2026 Jakub Krehel
  Modified and merged into Marionette.

Runtime Dependencies (Not Bundled):
  - gsap (3): GSAP Standard License (target project dependency, not bundled by Muro)
  - A design tool integration of the host: Figma MCP with figma-use, FigCraft's MCP server, or another canvas editor's (): External host integration, not bundled by Muro
  - Python 3.10+ (standard library) (): PSF runtime prerequisite, not bundled by Muro
  - GenOffice desktop app with its genoffice command line (>=0.9.0): Apache-2.0 (external application, not bundled by Muro; installed at runtime from the official releases when missing)
  - uv, or Python 3.11+ (standard library; optional truststore) (): External runtime, not bundled by Muro; installed at runtime from astral.sh when missing and wanted
  - Python 3.10+ (standard library) (): PSF runtime prerequisite, not bundled by Muro
  - The user's own agent command line (claude, codex, copilot or pi) for the loop guard's judge and the fact proposer (): External host application, not bundled by Muro; called only by hooks the user registered
