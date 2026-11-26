"""Where the project under test is: this repository's project file, `marionette.mp`, unpacked.

The store workflow unpacks the pushed file and names the folder in MURO_PROJECT (`muro project unpack` does the
same on a computer). It holds the package (`sources.json`, `capabilities/`, ...), the project's own files
(`project.json`, `records.json`, `history.json`, `CHANGELOG.md`), `inputs/` and `release/marionette/`.
"""
import os
from pathlib import Path

PACKAGE = Path(os.environ["MURO_PROJECT"]).resolve()
