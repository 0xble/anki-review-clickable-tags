# Changelog

All notable changes to Clickable Tags v3.0 are documented here.

## [Unreleased]

## [3.0.1] - 2026-03-09

### Fixed

- Resolve the reviewer/previewer JS bridge at click time so tag clicks work on
  current Anki 25.x webviews.
- Build valid browser queries for tag and deck searches, including quoted names.

## [3.0.0] - 2026-02-21

### Added

- Publish-prep scripts and CI/release workflow scaffolding.

- Modernized clickable tag rendering for current Anki builds.
- JS bridge using `webview_did_receive_js_message`.
- Configurable click scope and tag display behavior.
- Source-controlled custom add-on workspace integration.
