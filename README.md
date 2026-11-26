# Marionette

Marionette is one multidomain skill package built with
[Muro](https://github.com/acaprino/muro), as an example of what Muro produces.

This repository is a plugin store. Its only source is one file, **`marionette.mp`**,
Marionette's Muro project: the package, its inputs at their pinned commits, the
records, the history and the built plugin. Everything else here is generated from
that file at each release:

- `marionette/` is the plugin as the file carries it: one native adapter per host
  under `marionette/adapters/` (Claude Code, Codex, OpenCode, Pi, Hermes), the
  offline guide `marionette/GUIDE.html`, and the upstream works and their licences
  in `marionette/NOTICE.md` and `marionette/LICENSES/`.
- `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json` are the
  marketplaces of this repository for Claude Code and Codex.
- `releases/` holds the notes of each release.

## Install

Download `marionette-<version>.zip` and its `.sha256` from the
[releases](https://github.com/acaprino/marionette/releases), tagged
`marionette-v<version>`. Unzip it and follow `INSTALL.md` in the adapter folder
of your harness. For Claude Code:

```sh
claude plugin marketplace add <unzipped folder>/marionette/adapters/claude-code
claude plugin install marionette@marionette
```

Each release from 0.7.1 also carries `marionette.mp` and its `.sha256`: open it
in Muro to see or change the project.

## Changing Marionette

Nothing of the package lives unpacked here. To change it, open `marionette.mp`
in Muro, change the project there, and release it: **Release…** in the app, or

```sh
muro project release marionette.mp
```

which pushes the file to this repository. The push is the release:
[release.yml](.github/workflows/release.yml) calls Muro's store workflow at the
tag it names, which validates the package, checks every source at its pin,
builds it and runs `tests/` on the file, then writes `marionette/`, the
marketplaces and the notes from it and publishes the tag `marionette-v<version>`
with `marionette.mp`, `marionette-<version>.zip` and the SHA-256 of each. A
version is released once: another file under a published version is refused.
Muro's [project-store.md](https://github.com/acaprino/muro/blob/main/docs/project-store.md)
describes the workflow and its rules.

Do not edit `marionette/`, `releases/` or the marketplaces by hand: the next
release replaces them.

## The tests

`tests/` holds this repository's own tests of the package. They run on the
unpacked file, against a checkout of Muro (`MURO` below is its path):

```sh
PYTHONPATH=$MURO python -m muro project unpack marionette.mp --out <folder>
MURO_ROOT=$MURO MURO_PROJECT=<folder> python -m pytest -q tests
```

Without both variables none is collected. Some of them read the pinned sources
from their Git remotes.

Some paths of `marionette/` are longer than Windows allows by default: clone
with `git clone -c core.longpaths=true`.

## Earlier releases

`docs/releases/` holds the notes of the versions up to 0.7.0, which were built
from a package folder kept in this repository (`source/`, removed with 0.7.1).
Marionette 0.2.0 to 0.4.0 were published among
[Muro's releases](https://github.com/acaprino/muro/releases); `v0.1.0` here is
the first build.
