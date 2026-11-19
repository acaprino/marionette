# Marionette

Marionette is one multidomain skill package built with
[Muro](https://github.com/acaprino/muro), as an example of what Muro produces.
This repository publishes its builds. `marionette/` is the build of the latest
merged release: one native adapter per host under `marionette/adapters/`
(Claude Code, Codex, OpenCode, Pi, Hermes), the offline guide
`marionette/GUIDE.html`, and the upstream works and their licences in
`marionette/NOTICE.md` and `marionette/LICENSES/`.

## Install

Download `marionette-<version>.zip` and its `.sha256` from the
[releases](https://github.com/acaprino/marionette/releases), tagged
`marionette-v<version>`. Unzip it and follow `INSTALL.md` in the adapter folder
of your harness. For Claude Code:

```sh
claude plugin marketplace add <unzipped folder>/marionette/adapters/claude-code
claude plugin install marionette@marionette
```

## How a release arrives

1. Muro's `Release Marionette` workflow builds the package from
   `examples/marionette/sources.json` and pushes the build as `marionette/`,
   with its notes in `releases/marionette-v<version>.md`, to the branch
   `release/marionette-v<version>`.
2. This repository opens the pull request into `main`
   ([pull-request.yml](.github/workflows/pull-request.yml)). A new build of the
   same version refreshes it.
3. Merging it publishes the tag `marionette-v<version>` and the release with
   the zip of `marionette/` and its SHA-256
   ([release.yml](.github/workflows/release.yml)). A published release is never
   replaced: a new build needs a new version.

The source manifest, the capabilities and their decisions live in Muro at
[`examples/marionette/`](https://github.com/acaprino/muro/tree/main/examples/marionette).
Do not edit `marionette/` here: the next build replaces it. Some of its paths
are longer than Windows allows by default: clone with
`git clone -c core.longpaths=true`.

Marionette 0.2.0 to 0.4.0 were published among
[Muro's releases](https://github.com/acaprino/muro/releases); `v0.1.0` here is
the first build.
