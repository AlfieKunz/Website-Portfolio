# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

import os
import sys

is_mac = sys.platform == "darwin"
is_win = sys.platform == "win32"

def get_mpv_path():
    if is_win or is_mac:
        try:
            import anki_audio #type: ignore
            audio_pkg_path = os.path.dirname(anki_audio.__file__)

            if is_win:
                packaged_path = os.path.join(audio_pkg_path, "mpv" + ".exe")
            else:  # is_mac
                packaged_path = os.path.join(audio_pkg_path, "mpv")

            if os.path.exists(packaged_path):
                return packaged_path

        except ImportError:
            return None
    else:
        packaged_path = os.path.join(sys.prefix, "mpv")
        if os.path.exists(packaged_path):
            return packaged_path
    
    return None