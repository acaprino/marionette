"""The tests run on the project file, unpacked, against a checkout of the Muro factory.

MURO_PROJECT is the folder `muro project unpack marionette.mp` wrote (`project_dir.py`), and MURO_ROOT a checkout
of Muro. The factory (`muro`, `muro_build`), its prompts and its test helpers (`routing_helpers`, and the
functions some modules import from Muro's own test modules) are imported from the checkout; nothing of Muro is
copied here. The store workflow sets both when the file is pushed.
"""
import os
import sys
from pathlib import Path

import pytest

MURO_ROOT = os.environ.get("MURO_ROOT")
MURO_PROJECT = os.environ.get("MURO_PROJECT")
if MURO_ROOT and MURO_PROJECT:
    root = Path(MURO_ROOT).resolve()
    if not ((root / "muro" / "__init__.py").is_file() and (root / "tests" / "routing_helpers.py").is_file()):
        raise pytest.UsageError(f"MURO_ROOT={MURO_ROOT} is not a checkout of Muro (https://github.com/acaprino/muro).")
    if not (Path(MURO_PROJECT) / "sources.json").is_file():
        raise pytest.UsageError(f"MURO_PROJECT={MURO_PROJECT} is not an unpacked project (muro project unpack marionette.mp).")
    # First on the path, so an installed `muro` never stands in for the checkout.
    sys.path[:0] = [str(root), str(root / "tests")]
else:
    # The modules import the factory and read the project at load: without both nothing is collected.
    collect_ignore_glob = ["test_*.py"]


def pytest_terminal_summary(terminalreporter):
    if not (MURO_ROOT and MURO_PROJECT):
        terminalreporter.write_line(
            "No test was collected: set MURO_ROOT to the path of a checkout of Muro "
            "(https://github.com/acaprino/muro) and MURO_PROJECT to the folder that "
            "`muro project unpack marionette.mp` wrote.", yellow=True)
