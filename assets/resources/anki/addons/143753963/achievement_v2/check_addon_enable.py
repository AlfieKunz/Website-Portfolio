# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

import json
import os

from . import ADDON_PATH, LIST_ACHIEV_ADDONS

_SCRIPT_NAME = "AchevCheck"

IF_ERROR = True # もしｴﾗｰで検出失敗したらadd-onが有効とみなす

#MARK: check_addon_by_manually
def check_addon_by_manually():
    try:
        addons_directory = os.path.dirname(ADDON_PATH)

        for addon_id in LIST_ACHIEV_ADDONS:
            addon_directory = os.path.join(addons_directory, addon_id)
            init_path = os.path.join(addon_directory, "__init__.py")
            meta_path = os.path.join(addon_directory, "meta.json")

            if not os.path.isfile(init_path):
                continue

            dict_addon_meta = {}
            try:
                with open(meta_path, "r", encoding="utf-8") as meta_file:
                    dict_addon_meta = json.load(meta_file)
            except (OSError, ValueError):
                continue

            if not isinstance(dict_addon_meta, dict):
                continue

            if not dict_addon_meta.get("disabled", False):
                return True

        return False

    except Exception as e:
        print(f"[{_SCRIPT_NAME}] Error: {e}")
        return None

#MARK: check_addon_by_mw_manager
def check_addon_by_mw_manager():
    try:
        from aqt import mw
        installed_addons = mw.addonManager.allAddons()

        for addon_id in LIST_ACHIEV_ADDONS:
            if addon_id in installed_addons:
                if mw.addonManager.isEnabled(addon_id):
                    return True

        return False
    except Exception as e:
        print(f"[{_SCRIPT_NAME}] Error: {e}")
        return None


#MARK: check_addon
def check_addon():
    try:
        # mw.addonManager
        enable_result = check_addon_by_mw_manager()
        

        if enable_result is None:
            # try manually
            enable_result = check_addon_by_manually()

        if enable_result is None:
            # error
            enable_result = IF_ERROR

        return enable_result

    except Exception as e:
        print(f"[{_SCRIPT_NAME}] Error: {e}")
        return IF_ERROR
