#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 -m py_compile __init__.py main.py

python3 - <<'PY'
import json
from pathlib import Path

manifest = json.loads(Path("manifest.json").read_text())
meta = json.loads(Path("meta.json").read_text())
addon = json.loads(Path("addon.json").read_text())

errors = []

def expect_same(key: str) -> None:
    if manifest.get(key) != meta.get(key):
        errors.append(f"{key} mismatch: manifest={manifest.get(key)!r} meta={meta.get(key)!r}")

expect_same("name")
expect_same("human_version")
expect_same("homepage")

if manifest.get("name") != addon.get("name"):
    errors.append("name mismatch between manifest.json and addon.json")
if manifest.get("homepage") != addon.get("homepage"):
    errors.append("homepage mismatch between manifest.json and addon.json")

if errors:
    raise SystemExit("\n".join(errors))
PY

echo "check.sh: OK"
