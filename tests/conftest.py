"""The tests run against a checkout of the Muro factory: set MURO_ROOT to its path.

The package under test is this repository's `source/`. The factory (`muro`, `muro_build`), its prompts and
its test helpers (`routing_helpers`, and the functions some modules import from Muro's own test modules)
are imported from the checkout; nothing of Muro is copied here.
"""
import os
import sys
from pathlib import Path

import pytest

MURO_ROOT = os.environ.get("MURO_ROOT")
if MURO_ROOT:
    root = Path(MURO_ROOT).resolve()
    if not ((root / "muro" / "__init__.py").is_file() and (root / "tests" / "routing_helpers.py").is_file()):
        raise pytest.UsageError(f"MURO_ROOT={MURO_ROOT} is not a checkout of Muro (https://github.com/acaprino/muro).")
    # First on the path, so an installed `muro` never stands in for the checkout.
    sys.path[:0] = [str(root), str(root / "tests")]
else:
    # The modules import the factory at load: without a checkout nothing is collected.
    collect_ignore_glob = ["test_*.py"]


def pytest_terminal_summary(terminalreporter):
    if not MURO_ROOT:
        terminalreporter.write_line(
            "No test was collected: MURO_ROOT is not set. Set it to the path of a checkout of Muro "
            "(https://github.com/acaprino/muro), at the ref named in the file MURO_REF.", yellow=True)
