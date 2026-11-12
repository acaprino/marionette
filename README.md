# Marionette

Marionette is one multidomain skill package built with
[Muro](https://github.com/acaprino/muro), as an example of what Muro produces.
This repository only publishes its builds: each release carries
`marionette-<version>.zip` with one native adapter per host under
`marionette/adapters/` (Claude Code, Codex, OpenCode, Pi, Hermes). Install
steps for each host are in that adapter's `INSTALL.md`.

The source manifest lives in Muro at `examples/marionette/sources.json`.
Upstream works and their licences are listed in [NOTICE.md](NOTICE.md) and
[LICENSES](LICENSES).

Shinatama follows the latest release of this repository and loads Marionette
into every Claude Code, Codex, Pi and OpenCode session it starts.
