# A prompt for another builder

When someone wants a prompt to paste into Lovable, Bolt, v0, Cursor, Windsurf, Replit or a fresh
Claude Code session instead of code, the deliverable is a **full-source rebuild prompt with their
brand already in it**. Not a description of a page: the real files, rewritten where the brand lives,
verbatim everywhere else. A builder given exact source produces that source; a builder given a
description invents one.

## From a library build

1. Pick the build (library/INDEX.md, or the Scrolltide MCP if it's connected) and copy its prompt
   whole.
2. Rewrite these parts in place, and only these:
   - **The title line and "What this project is"**: the new brand, what the page shows, the new
     fonts and palette in words.
   - **The content file** (`## File: src/content.ts` in most builds): every word, keeping the same
     keys and shapes, because the components read them.
   - **The palette and fonts**: the `@theme` or `:root` block in the stylesheet, the font `<link>`
     in `index.html`, and the fonts line in "Tech stack". Keep them in agreement.
   - **`index.html`**: `<title>`, description, theme colour.
   - **"Assets"**, if the user has their own media: replace the download step with the exact paths,
     sizes and formats their files must have (`public/frames/d/f001.webp … f481.webp, 1600×900`).
     Otherwise keep the library download step as written.
   - **`package.json`**: the `name` field.
3. Leave everything else byte for byte: "How the page works", "Reproduce this exactly", the stack,
   every other file, the comments. Those are why it works.
4. Check the result before handing it over:
   - Search it for the old brand's names; none left.
   - Every `## File:` section still has one opening and one closing fence.
   - The content file has the same keys as before.
   - The fonts named in the stack line, the `<link>` and the stylesheet are the same fonts.

## Builder notes

| Builder | What to tell the user |
|---|---|
| Lovable | The library's stack (Vite, React, TypeScript, Tailwind v4) is Lovable's own, so the prompt pastes as is. If it tries to add shadcn or other packages, the prompt's "do not add packages" line covers it. |
| Bolt | Same stack. Browser-based builders may not be able to download the asset archive themselves: download it, unpack it, and upload the files into `public/` before the first run. |
| v0 | It tends to produce Next.js. Either ask it to keep the project as Vite, or accept a Next.js port and check the scroll engine is still one loop in a client component. |
| Cursor, Windsurf, Claude Code, Codex | Paste into an empty folder; they can run the download and `npm` themselves. |
| Replit | As Cursor. Make sure the run command is `npm run dev`. |

If a builder truncates long input, attach the prompt as a `.md` file instead of pasting it. Don't
shorten it: the full source is the point.

## From scratch

If no library build fits and the user still wants a prompt, build the page first (from the patterns
and the house style), get it running and checked, and then write the prompt **from the finished
source**, in the same order the library uses:

1. **What this project is**: one paragraph a person can picture.
2. **How the page works**: the three or four load-bearing ideas, and the checks that must pass.
3. **Reproduce this exactly**: no improving, no substituting, no extra files.
4. **Tech stack**: exact, with `package.json` inline.
5. **Assets**: what to download or provide, where it goes, never hotlinked.
6. **Steps to build**.
7. **`## File:` sections**: every file, verbatim, generated from the real files rather than retyped.
8. **Design notes**: why the unusual choices were made.
