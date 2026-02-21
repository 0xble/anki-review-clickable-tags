from __future__ import annotations

import html
import json
from typing import Any, TypedDict, cast

from anki import hooks
from anki.template import TemplateRenderContext
from aqt import dialogs, gui_hooks, mw
from aqt.browser.previewer import Previewer
from aqt.qt import Qt
from aqt.reviewer import Reviewer
from aqt.webview import WebContent

MESSAGE_PREFIX = "review_clickable_tags:"
SUPPORTED_SCOPES = {"all", "current_deck", "none"}


class AddonConfig(TypedDict, total=False):
    single_click_scope: str
    double_click_scope: str
    visible_tag_levels: int
    show_hash_prefix: bool
    sort_tags: bool


DEFAULT_CONFIG: AddonConfig = {
    "single_click_scope": "all",
    "double_click_scope": "current_deck",
    "visible_tag_levels": 0,
    "show_hash_prefix": False,
    "sort_tags": True,
}

_initialized = False


def init() -> None:
    global _initialized
    if _initialized:
        return

    addon_package = mw.addonManager.addonFromModule(__name__)
    mw.addonManager.setWebExports(addon_package, r"web/.*\.(css|js)")

    hooks.field_filter.append(_on_field_filter)
    gui_hooks.webview_will_set_content.append(_on_webview_will_set_content)
    gui_hooks.webview_did_receive_js_message.append(_on_js_message)
    _initialized = True


def _on_webview_will_set_content(web_content: WebContent, context: object | None) -> None:
    if not isinstance(context, Reviewer) and not isinstance(context, Previewer):
        return

    addon_package = mw.addonManager.addonFromModule(__name__)
    css_path = f"/_addons/{addon_package}/web/clickable_tags.css"
    js_path = f"/_addons/{addon_package}/web/clickable_tags.js"

    if css_path not in web_content.css:
        web_content.css.append(css_path)
    if js_path not in web_content.js:
        web_content.js.append(js_path)


def _on_js_message(
    handled: tuple[bool, Any], message: str, context: object
) -> tuple[bool, Any]:
    if not isinstance(context, Reviewer) and not isinstance(context, Previewer):
        return handled
    if not message.startswith(MESSAGE_PREFIX):
        return handled

    payload_raw = message.removeprefix(MESSAGE_PREFIX)
    try:
        payload = cast(dict[str, Any], json.loads(payload_raw))
    except Exception:
        return handled

    tag = _as_str(payload.get("tag"))
    deck = _as_str(payload.get("deck"))
    action = _as_str(payload.get("action"))
    if not tag or action not in {"click", "dblclick"}:
        return handled

    query = _build_search_query(tag=tag, deck=deck, action=action)
    if not query:
        return (True, None)

    browser = dialogs.open("Browser", mw)
    browser.search_for(query)
    browser.setWindowState(
        browser.windowState()
        & ~Qt.WindowState.WindowMinimized
        | Qt.WindowState.WindowActive
    )
    return (True, None)


def _on_field_filter(
    text: str, field_name: str, filter_name: str, context: TemplateRenderContext
) -> str:
    if filter_name != "clickable" or field_name != "Tags":
        return text

    note = context.note()
    tags = list(note.tags)
    if not tags:
        return ""

    config = _get_config()
    if config["sort_tags"]:
        tags.sort(key=str.casefold)

    deck_name = context.col().decks.name(context.card().current_deck_id())
    parts = [
        _render_tag_button(tag=tag, deck_name=deck_name, config=config)
        for tag in tags
    ]
    return '<span class="rct-tags">' + "".join(parts) + "</span>"


def _render_tag_button(tag: str, deck_name: str, config: AddonConfig) -> str:
    visible_levels = int(config["visible_tag_levels"])
    display_tag = _truncate_tag(tag, visible_levels)
    if config["show_hash_prefix"]:
        display_tag = f"#{display_tag}"

    escaped_tag = html.escape(tag, quote=True)
    escaped_deck = html.escape(deck_name, quote=True)
    escaped_display = html.escape(display_tag)
    return (
        '<button class="rct-tag" type="button" '
        f'data-rct-tag="{escaped_tag}" '
        f'data-rct-deck="{escaped_deck}">{escaped_display}</button>'
    )


def _truncate_tag(tag: str, visible_levels: int) -> str:
    if visible_levels <= 0:
        return tag
    parts = tag.split("::")
    if visible_levels >= len(parts):
        return tag
    return "::".join(parts[-visible_levels:])


def _build_search_query(tag: str, deck: str, action: str) -> str | None:
    config = _get_config()
    if action == "click":
        scope = config["single_click_scope"]
    else:
        scope = config["double_click_scope"]

    if scope == "none":
        return None

    tag_term = _quote_search_term("tag", tag)
    if scope == "current_deck" and deck:
        deck_term = _quote_search_term("deck", deck)
        return f"{tag_term} {deck_term}"
    return tag_term


def _quote_search_term(prefix: str, value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{prefix}:{escaped}"'


def _get_config() -> AddonConfig:
    cfg_raw = mw.addonManager.getConfig(__name__) or {}
    cfg = {**DEFAULT_CONFIG}

    if isinstance(cfg_raw, dict):
        for key, value in cfg_raw.items():
            if key in cfg:
                cfg[key] = value

    single_click_scope = _as_str(cfg.get("single_click_scope")) or DEFAULT_CONFIG[
        "single_click_scope"
    ]
    if single_click_scope not in SUPPORTED_SCOPES:
        single_click_scope = DEFAULT_CONFIG["single_click_scope"]

    double_click_scope = _as_str(cfg.get("double_click_scope")) or DEFAULT_CONFIG[
        "double_click_scope"
    ]
    if double_click_scope not in SUPPORTED_SCOPES:
        double_click_scope = DEFAULT_CONFIG["double_click_scope"]

    visible_tag_levels = _as_int(cfg.get("visible_tag_levels"), default=0)
    if visible_tag_levels < 0:
        visible_tag_levels = 0

    return {
        "single_click_scope": single_click_scope,
        "double_click_scope": double_click_scope,
        "visible_tag_levels": visible_tag_levels,
        "show_hash_prefix": bool(cfg.get("show_hash_prefix")),
        "sort_tags": bool(cfg.get("sort_tags", True)),
    }


def _as_str(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _as_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
