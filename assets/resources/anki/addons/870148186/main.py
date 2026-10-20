from aqt import gui_hooks, mw
from aqt.deckbrowser import DeckBrowser, DeckBrowserContent
from anki.decks import DeckNameId
import json
from aqt.webview import WebContent
from typing import Final, Dict, TypedDict, Any

mw.addonManager.setWebExports(__name__, r"web/.*(css|js)")

MATURE_QUERY: Final[str] = (
    """("is:review" -"is:learn") AND "prop:ivl>=21"AND -("is:buried" OR "is:suspended")"""
)
YOUNG_QUERY: Final[str] = (
    """ ("is:review" AND -"is:learn") AND "prop:ivl<21"AND -("is:buried" OR "is:suspended")"""
)
SUSPENDED_QUERY: Final[str] = """ is:suspended """


class DeckStats(TypedDict):
    mature: int
    young: int
    suspended: int
    learning: int
    new: int
    all: int


def find_num_of_cards(deck: DeckNameId, query: str) -> int:
    return len(mw.col.find_cards(f'"deck:{deck.name}" {query}'))


def get_deck_stats() -> Dict[int, DeckStats]:
    col = mw.col
    stats: Dict[int, DeckStats] = {}
    for deck in col.decks.all_names_and_ids():
        deck_stats: DeckStats = {
            "mature": find_num_of_cards(deck, MATURE_QUERY),
            "young": find_num_of_cards(deck, YOUNG_QUERY),
            "suspended": find_num_of_cards(deck, SUSPENDED_QUERY),
            "learning": find_num_of_cards(deck, "is:learn"),
            "new": find_num_of_cards(deck, "is:new"),
            "all": find_num_of_cards(deck, ""),
        }
        stats[deck.id] = deck_stats
    return stats


def inject_deck_stats(browser: DeckBrowser, content: DeckBrowserContent) -> None:
    """Injects the deck stats so JS can read them."""
    stats = get_deck_stats()
    stats_json = json.dumps(stats)
    content.tree += f"<script>window.deckStats={stats_json};</script>"


def append_web(web_content: WebContent, context: Any) -> None:
    """Append javascript and css to the deck browser webview"""
    if not isinstance(context, DeckBrowser):
        return
    addon_id = mw.addonManager.addonFromModule(__name__)
    js_url = f"/_addons/{addon_id}/web/inject_column.js"
    css_url = f"/_addons/{addon_id}/web/style.css"
    web_content.js.append(js_url)
    web_content.css.append(css_url)


def main() -> None:
    gui_hooks.webview_will_set_content.append(append_web)
    gui_hooks.deck_browser_will_render_content.append(inject_deck_stats)
