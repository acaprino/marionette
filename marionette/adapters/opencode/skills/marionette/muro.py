from pathlib import Path
import sys
package = Path(__file__).resolve().parent
if not (package / "ROUTER.md").is_file() and package.name in {"claude-code", "codex", "pi", "opencode", "hermes"} and (package.parent.parent / "ROUTER.md").is_file():
    package = package.parent.parent
sys.path.insert(0, str(package))
from muro.runtime import runtime_main
raise SystemExit(runtime_main(["--package", str(package), *sys.argv[1:]]))
