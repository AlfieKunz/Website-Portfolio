# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

try:
    from PyQt6.QtGui import QAction
    from PyQt6.QtWidgets import QMenu
except Exception as e:
    print(f"Error: {e}")
    from aqt.qt import QAction
    from aqt.qt import QMenu

from aqt import mw

from ..path_manager import ADDON_NAME

#MARK:open url
def open_popup_url(key):
    try:
        from .popup_config import REPORT_URL, PATREON_URL, RATE_THIS_URL
        from aqt.utils import openLink
        url_map = {
            "rate": RATE_THIS_URL,
            "patreon": PATREON_URL,
            "report": REPORT_URL,
        }
        openLink(url_map[key])
    except Exception as e:
        print(f"[{ADDON_NAME}] Error: {e}")

#MARK:add_menu
def add_menu(qt_menu:QMenu):

    qt_menu.addSeparator()

    rate_this_action = QAction('👍️RateThis', mw)
    rate_this_action.triggered.connect(lambda: open_popup_url("rate"))
    qt_menu.addAction(rate_this_action)

    patreon_action = QAction("💖Become a Patron", mw)
    patreon_action.triggered.connect(lambda: open_popup_url("patreon"))
    qt_menu.addAction(patreon_action)

