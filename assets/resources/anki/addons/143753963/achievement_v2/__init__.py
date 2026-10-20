# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

from ..path_manager import ADDON_PATH
from ..shige_config.popup_config import RATE_THIS_URL, PATREON_URL

# ADDON_PATH = os.path.dirname(os.path.abspath(__file__))

#MARK:🟢
WINDOW_TITLE = "Spell Checker(by Shigeඞ) Streak-Popup"
ADDON_NAME = "Spell Checker"
LIST_ACHIEV_ADDONS = [
    # "999999999", # test
    "175794613",
    "1468920185",
    "1708250053",
    "1959668791",
    "1677779223",
    "1562475180",
    "1370336700",
    "1923741581",

]


#MARK: entry_point
from .setup_achiev import entry_point

# e.g.
# try:
#     from ..achievement_v2 import entry_point
#     entry_point(addon_menu)
# except Exception as e:
#     print(f"[{ADDON_NAME}] Error: {e} ")


#🟢 user_files