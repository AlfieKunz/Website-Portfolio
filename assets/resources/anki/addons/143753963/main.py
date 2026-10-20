# Copyright (C) lovac42 2021 <https://github.com/lovac42> SpellingPolice <https://github.com/lovac42/SpellingPolice>
# Copyright (C) Valentin 2023 <https://github.com/ValentinSchmitz> Spell Checker <https://github.com/ValentinSchmitz/spell-checker>
# Copyright (C) Shigeyuki 2025 <http://patreon.com/Shigeyuki>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
from functools import partial

from aqt import editor, QMenu
from aqt import gui_hooks
from aqt import mw
from aqt.editor import Editor
from aqt.qt import QWebEngineProfile
from aqt.utils import tooltip

from .dict_dialog import DictionaryManager
from .convert_manager import (
    compile_personal,
    get_dictionaries,
    get_user_data,
    retry_pending_bdic_copies,
    save_write_unique,
    set_user_data,
)
from .const import ADDON_PATH, PERSONAL_PATH

from .path_manager import ADDON_NAME, SHORT_ADDON_NAME
from .shige_config.add_menu_actions import open_popup_url
from .shige_config.support_old_anki import get_ankiwebview_page


dictMan = DictionaryManager()

# def addToDictionary(word):
#     # https://ankiweb.net/shared/info/369581638#:~:text=on%20Windows%2011.-,on%202025%2D03%2D05,-Awesome%2C%20just%20some
#     page = get_ankiwebview_page(mw.web)
#     saveWrite(PERSONAL_PATH, f"{word}\n", "a+")
#     compilePersonal()

def add_to_dict(word, editor_webview: editor.EditorWebView):
    # https://ankiweb.net/shared/info/369581638#:~:text=on%20Windows%2011.-,on%202025%2D03%2D05,-Awesome%2C%20just%20some
    added = save_write_unique(PERSONAL_PATH, f"{word}\n", "a+")
    if added:
        page = get_ankiwebview_page(editor_webview)

        #MARK: spell check Enabled
        page.profile().setSpellCheckEnabled(False)
        page.profile().setSpellCheckLanguages({})

        compile_personal()

        page.profile().setSpellCheckLanguages(get_dictionaries())
        page.profile().setSpellCheckEnabled(get_user_data("status", default=True))

    else:
        tooltip("Error: Maybe this word is duplicated? :-/")


def need_compile_Anki_start_up(*args, **kwargs):
    config = mw.addonManager.getConfig(__name__)
    if config.get("compile_is_needed", False):
        compile_personal()
        config["compile_is_needed"] = False
        mw.addonManager.writeConfig(__name__, config)


#MARK: set_spell_check_status
def set_spell_check_status(editor_webview: editor.EditorWebView, enabled: bool):
    set_user_data("status", enabled)
    page = get_ankiwebview_page(editor_webview)
    page.profile().setSpellCheckEnabled(enabled)


#MARK: on_context_menu_event
def on_context_menu_event(editor_webview: editor.EditorWebView, menu: QMenu):
    # page = editor_webview._page
    page = get_ankiwebview_page(editor_webview)

    base_action = menu.actions()[0]

    data = editor_webview.lastContextMenuRequest()

    menu.insertSeparator(base_action)

    submenu = QMenu(f"{SHORT_ADDON_NAME}", menu)

    enable_action = submenu.addAction("Enable Spell Checker")
    enable_action.setCheckable(True)
    enable_action.setChecked(get_user_data("status", default=True))
    enable_action.triggered.connect(partial(set_spell_check_status, editor_webview))

    option_action = submenu.addAction("⚙️Option")
    option_action.triggered.connect(dictMan.showConfig)

    rate_action = submenu.addAction("👍️Rate this")
    rate_action.triggered.connect(partial(open_popup_url, "rate"))

    report_action = submenu.addAction("🚨Report")
    report_action.triggered.connect(partial(open_popup_url, "report"))

    patron_action = submenu.addAction("💖Become a Patron")
    patron_action.triggered.connect(partial(open_popup_url, "patreon"))

    menu.insertMenu(base_action, submenu)

    if data.misspelledWord():
        add = menu.addAction("📥️Add to Dictionary")
        menu.insertAction(base_action, add)
        add.triggered.connect(partial(add_to_dict, data.misspelledWord(), editor_webview))

    if data.spellCheckerSuggestions():
        spell_suggest = menu.addAction("🔍️Spell Suggestions:")
        spell_suggest.setEnabled(False)
        menu.insertAction(base_action, spell_suggest)

        for word in data.spellCheckerSuggestions():
            recommendation = menu.addAction(word)
            menu.insertAction(base_action, recommendation)
            recommendation.triggered.connect(partial(page.replaceMisspelledWord, word))

    menu.insertSeparator(base_action)

#MARK: setup_BDIC
def setup_BDIC(editor_webview: editor.EditorWebView):
    retry_pending_bdic_copies()

    # page = editor_webview._page
    page = get_ankiwebview_page(editor_webview)

    profile: QWebEngineProfile = page.profile()
    status = get_user_data("status", default=True)
    profile.setSpellCheckEnabled(status)
    profile.setSpellCheckLanguages(get_dictionaries())

    print(os.environ.get("QTWEBENGINE_DICTIONARIES_PATH"))


#MARK: on_setup_editor_buttons
def on_setup_editor_buttons(buttons:list[str], editor:Editor):
    icon = os.path.join(ADDON_PATH, "icon.svg")

    def toggleSpellChecker(editor: Editor):
        is_new = not get_user_data("status", default=True)
        set_spell_check_status(editor.web, is_new)
        if is_new:
            tooltip("Spell Checker Enabled! :-)")
        else:
            tooltip("Spell Checker Disabled :-(")

    button = editor.addButton(
        icon,
        "SC",
        toggleSpellChecker,
        tip="✅Toggle Spell Checker\n(fixed by Shigeඞ)"
    )
    buttons.append(button)
    return buttons


#MARK: on_main_window_did_init
def on_main_window_did_init():
    try:
        global dictMan
        dictMan.setupMenu()

    except Exception as e:
        print(f"[{ADDON_NAME}] Error: {e} ")

def setup_hooks():
    gui_hooks.editor_did_init_buttons.append(on_setup_editor_buttons)
    gui_hooks.editor_will_show_context_menu.append(on_context_menu_event)
    gui_hooks.editor_web_view_did_init.append(setup_BDIC)
    gui_hooks.main_window_did_init.append(need_compile_Anki_start_up)
    mw.addonManager.setConfigAction(__name__, dictMan.showConfig)

    gui_hooks.main_window_did_init.append(on_main_window_did_init)
