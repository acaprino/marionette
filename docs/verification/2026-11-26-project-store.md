# Marionette became a plugin store, released from `marionette.mp` (2026-11-26)

The owner asked that a Muro project be one file and that its repository be a plugin store built from it
(Muro's ADR-0034): "è da un muro project che nasce tutto", "non repository aperte o scompattate". This
repository held the package unpacked in `source/` and three workflows of its own. Factory: Muro `muro-v0.10.0`
(`5871ee2`).

## What was done

| Step | Result |
| --- | --- |
| The project file | `marionette.mp` 0.7.1, 18,653,876 bytes, SHA-256 `5271ec43f4f2035bca015d0989ee2ea7a4b889b3357abf07c5ecbb48661807e7` |
| The move | commit `38f4f45`: `source/`, `package.yml`, `prepare-release.yml`, `release_version.py`, `MURO_REF` and `test_release_workflow.py` removed; `release.yml` is the ten lines that call Muro's store workflow at `muro-v0.10.0`; the tests read `MURO_PROJECT` |
| The release | `muro project release marionette.mp --expect-digest ...` pushed commit `86e4035`; the store workflow (run 45784256406) wrote commit `3f71735` and the tag `marionette-v0.7.1` |

The version is 0.7.1 because 0.7.0 was already published from the folder, and a store refuses a published
version from another file. Nothing changed in the catalog, the session policy or the pinned sources.

## How the file was made

On a Linux runner, not on the owner's Windows computer: a project file written on Windows carries no executable
permission (a file packed there on 2026-11-25 had 0 executable members under `release/`, where the build of 0.7.0
in this repository has 126). A one-off workflow on the branch `mp-bootstrap`, deleted afterwards, ran
`muro project pack` on `source/` at `c111cdb` (with `builtin` set to `false` in `project.json`: Muro ships no
project) and `muro project commit --step patch --summary` on its unpack (run 45783409343).

The same job rehearsed what the store's gate runs, on the new file:

- `--validate`, `--check-sources` and `--build`: passed.
- The tests of this repository, with `MURO_PROJECT`: 309 passed. In the first run one failed
  (`test_project_files.py`: it held that the runs of `history.json` are stored newest first; `muro project
  commit` appends a run and Muro's app orders them by time). The rule was this repository's own and was dropped.
- The plugin the file carries, beside `marionette/` of 0.7.0: 2,632 files against 2,620, 126 executable on both
  sides. The 12 new files are two modules of the factory's runtime (`muro/project_release.py`,
  `muro/project_store.py`) in the package and in each adapter. The files whose content differs are the runtime
  (`muro/__init__.py`, `cli.py`, `delivery.py`, `sources.py`), `sources.json`, the plugin manifests, `NOTICE.md`
  and `GUIDE.html`. No capability and no absorbed file differs.

## The release run

`gate` and `publish` passed at the first run. The generated commit changed no file mode (126 executable files
in `marionette/` before and after) and touched only `marionette/`, the two marketplaces and
`releases/marionette-v0.7.1.md`. The release has `marionette.mp`, `marionette-0.7.1.zip` and the `.sha256` of
each; the SHA-256 of the released `marionette.mp` is the one above.

## Not run

- No installation and no host session on the 0.7.1 build.
- A second release from the file: the next version, pushed over the store this run wrote.
- A release of a file written on Windows. Until Muro keeps the executable permission there, a `marionette.mp`
  changed and packed on Windows would publish the scripts of the absorbed sources without it.
