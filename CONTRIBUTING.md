# Contributing

## Development Setup

1. Clone repo.
2. Link your checkout into Anki's `addons21` directory as `review_clickable_tags`
   (see OS-specific paths and commands in `README.md`).
3. Restart Anki.

## Local Checks

```bash
./scripts/check.sh
./scripts/package.sh
```

## Style Notes

- Keep `__init__.py` minimal.
- Use `aqt.gui_hooks` over broad monkey-patching.
- Keep user-modifiable/persistent state under `user_files/` only.

## Pull Requests

- Keep PRs narrowly scoped.
- Update `CHANGELOG.md` for user-visible behavior changes.
- Include compatibility notes if Anki version support changes.
