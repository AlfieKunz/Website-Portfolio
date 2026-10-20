# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>


from . import ADDON_NAME as _ADDON_NAME

_reviewer_hook_registered = False


import typing
if typing.TYPE_CHECKING:
    from aqt import QMenu

#MARK: on_streak_popup
def on_streak_popup(*args, **kwargs):
    try:
        from .achiev_v2_main import make_achievement_widget
        make_achievement_widget(is_check_streak=False)

    except Exception as e:
        print(f"[{_ADDON_NAME}] Error: {e}")


#MARK: add_menu_achiev_popup
def add_menu_achiev_popup(qt_menu:"QMenu"):
    try:
        from aqt import mw
        from aqt.qt import QAction, qconnect
        achiev_action = QAction(f"Streak Pop-up", mw)
        qconnect(achiev_action.triggered, on_streak_popup)
        qt_menu.addAction(achiev_action)

    except Exception as e:
        print(f"[{_ADDON_NAME}] Error: {e} ")


#MARK: on_streak_auto_popup
def on_streak_auto_popup(*args, **kwargs):
    try:
        from .achiev_v2_main import make_achievement_widget
        make_achievement_widget(is_check_streak=True)

    except Exception as e:
        print(f"[{_ADDON_NAME}] Error: {e}")

#MARK: on_reviewer_will_end
def on_reviewer_will_end(*args, **kwargs):
    try:
        from aqt.qt import QTimer
        QTimer.singleShot(0, on_streak_auto_popup)
    except Exception as e:
        print(f"[{_ADDON_NAME}] Error: {e} ") 


#MARK: setup_achiev_gui_hooks
def setup_achiev_gui_hooks():
    global _reviewer_hook_registered

    try:
        from aqt import gui_hooks
        if _reviewer_hook_registered:
            return

        gui_hooks.reviewer_will_end.append(on_reviewer_will_end)
        _reviewer_hook_registered = True

    except Exception as e:
        print(f"[{_ADDON_NAME}] Error: {e} ")


#MARK: entry_point
def entry_point(qt_menu):
    try:
        from .check_addon_enable import check_addon
        if check_addon():
            # streak pop-up duplicate, skip
            return

        add_menu_achiev_popup(qt_menu)
        setup_achiev_gui_hooks()

    except Exception as e:
        print(f"[{_ADDON_NAME}] Error: {e} ")

