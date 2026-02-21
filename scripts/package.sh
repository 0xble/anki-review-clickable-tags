#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

read -r package version < <(python3 - <<'PY'
import json
from pathlib import Path

manifest = json.loads(Path("manifest.json").read_text())
print(manifest["package"], manifest["human_version"])
PY
)

mkdir -p dist
artifact="dist/${package}-${version}.ankiaddon"
rm -f "$artifact"

zip -r -q "$artifact" \
  __init__.py \
  main.py \
  config.json \
  config.md \
  manifest.json \
  meta.json \
  addon.json \
  web

echo "$artifact"
