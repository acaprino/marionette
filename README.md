# Marionette

Marionette is one multidomain skill package built with
[Muro](https://github.com/acaprino/muro), as an example of what Muro produces.
This repository holds its source and publishes its builds. `source/` is the
package directory that Muro reads; `marionette/` is the build of the latest
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

## Working on the package

- `source/` is the package directory: the manifest `sources.json` with the
  pinned sources, `capabilities/`, `ROUTER.md`, `entries.json`,
  `delivery.json`, `guide-examples.json`, `eval-cases.json` and the owner's
  `custom-instructions/`. A change to the package is a change there.
- `tests/` holds the package's tests and `docs/releases/` the notes of each
  version.
- `MURO_REF` names the commit or tag of Muro that the workflows build with. It
  is the one place where that ref is kept.

Muro is not copied here. With a checkout of Muro at that ref (`MURO` below is
its path):

```sh
MURO_ROOT=$MURO python -m pytest -q tests
python $MURO/muro_build.py --manifest source/sources.json --validate
python $MURO/muro_build.py --manifest source/sources.json --check-sources
python $MURO/muro_build.py --manifest source/sources.json --build --out <scratch>
```

The tests import the factory, its prompts and its test helpers from
`MURO_ROOT`; without it none is collected. Some of them, and `--check-sources`,
read the pinned sources from their Git remotes. Every push and pull request
that touches the source, the tests or `MURO_REF` runs the same four commands
([package.yml](.github/workflows/package.yml)). Muro's rules for a package
apply (its `AGENTS.md`): intake and harmonization are done by the host LLM, and
Muro only prepares and validates.

## How a release arrives

1. Change `plugin.version` in `source/sources.json` and write the notes in
   `docs/releases/marionette-v<version>.md`. Without that file the notes carry
   only the version and the commits the build was made from.
2. When that change reaches `main`,
   [prepare-release.yml](.github/workflows/prepare-release.yml) runs the tests,
   validates the manifest, checks the sources and builds the package with the
   pinned Muro. It pushes the build as `marionette/`, with the root
   marketplaces and the notes in `releases/marionette-v<version>.md`, to the
   branch `release/marionette-v<version>` and opens the pull request into
   `main`. A new build of the same version refreshes it. The workflow can also
   be started by hand on `main`.
3. Merging it publishes the tag `marionette-v<version>` and the release with
   the zip of `marionette/` and its SHA-256
   ([release.yml](.github/workflows/release.yml)). A published release is never
   replaced: a new build needs a new version.

Do not edit `marionette/`, `releases/` or the root marketplaces by hand: the
next build replaces them. Some paths of `marionette/` are longer than Windows
allows by default: clone with `git clone -c core.longpaths=true`.

Marionette 0.2.0 to 0.4.0 were published among
[Muro's releases](https://github.com/acaprino/muro/releases); `v0.1.0` here is
the first build.
