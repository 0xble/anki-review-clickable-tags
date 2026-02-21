# Releasing

This project supports two stages:

1. **Preparation** (local/CI package creation)
2. **Publish** (GitHub release + optional AnkiWeb upload)

## Prep Checklist

1. Verify add-on in Anki desktop.
2. Run checks:

```bash
./scripts/check.sh
./scripts/package.sh
```

3. Update:

- `CHANGELOG.md`
- `manifest.json` / `meta.json` `human_version` and `mod`

## GitHub Release (when ready)

1. Create and push a tag:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

2. Workflow builds `.ankiaddon` and drafts release assets.

## AnkiWeb Upload (manual, optional)

After GitHub release is validated, upload the artifact to AnkiWeb from the maintainers account.

This repository intentionally separates build/release prep from AnkiWeb upload.
