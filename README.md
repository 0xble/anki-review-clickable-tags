# Clickable Tags v3.0

Modernized fork of Clickable Tags for current Anki (`25.x`).

## Status

- Maintained in source control as a custom add-on.
- Publish-ready packaging via local scripts and CI.

## Compatibility

- Tested target: Anki `25.09.x`
- Expected compatibility: modern `25.x` desktop builds

## Features

- Render tags as clickable pills in reviewer/previewer via `{{clickable:Tags}}`
- Single-click: search by tag
- Double-click: search by tag scoped to current deck (default)
- Configurable scope behavior and display options

## Installation

### Option 1: install from release package (`.ankiaddon`)

1. Download the latest `.ankiaddon` from this repository's GitHub Releases.
2. In Anki, go to `Tools -> Add-ons -> Install from file...`.
3. Select the `.ankiaddon` file and restart Anki.

### Option 2: development install (link a local checkout)

1. Clone this repo to any local path.
2. Link the repo folder into your Anki `addons21` directory as `review_clickable_tags`.
3. Restart Anki.

Typical `addons21` paths:

- macOS: `~/Library/Application Support/Anki2/addons21/`
- Linux: `~/.local/share/Anki2/addons21/`
- Windows: `%APPDATA%\\Anki2\\addons21\\`

Create the link on macOS/Linux:

```bash
ln -sfn /path/to/review_clickable_tags \
  /path/to/Anki2/addons21/review_clickable_tags
```

Create the link in PowerShell (Windows):

```powershell
New-Item -ItemType SymbolicLink `
  -Path "$env:APPDATA\\Anki2\\addons21\\review_clickable_tags" `
  -Target "C:\\path\\to\\review_clickable_tags"
```

### Manual package install (`.ankiaddon`)

1. Build package:

```bash
./scripts/package.sh
```

2. Double-click the generated file in `dist/` to install.

## Template usage

Add this to the card template where tags should appear:

```html
{{clickable:Tags}}
```

Behavior defaults:

- Single-click tag: search all decks by tag
- Double-click tag: search tag inside current deck

## Data-safety model

- This add-on does not auto-edit note types, notes, or collection data.
- It only renders/intercepts `{{clickable:Tags}}` at runtime in reviewer/previewer.

## Optional bulk setup (outside this add-on)

If you want to roll this out across all note types:

1. Back up note type templates first.
2. Use AnkiConnect to update templates to include `{{clickable:Tags}}` on front/back.
3. Sync AnkiWeb.
4. Repeat sync on other devices.

Keep this as a one-time external migration step, not add-on startup logic.

## Configuration

This add-on ships:

- `config.json` defaults
- `config.md` docs for Anki's config editor

## Development

### Validate + package locally

```bash
./scripts/check.sh
./scripts/package.sh
```

## Support

- Issues: `https://github.com/0xble/anki-review-clickable-tags/issues`

## License

AGPL-3.0-or-later. See `LICENSE`.
