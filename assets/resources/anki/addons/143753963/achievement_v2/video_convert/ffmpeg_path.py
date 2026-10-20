# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

from .ajt_utils_find_executable import find_executable
from .. import ADDON_NAME


def get_ffmpeg_exe_path():

    # if FFmpeg is already installed on the user's PC use it
    if ffmpeg_exe_path := find_executable("ffmpeg"):
        print(f"[{ADDON_NAME}] use find_executable")
        return ffmpeg_exe_path

    try: # use imageio_ffmpeg path
        from imageio_ffmpeg import get_ffmpeg_exe  # type: ignore
        ffmpeg_exe_path = get_ffmpeg_exe()
        print(f"[{ADDON_NAME}] use imageio_ffmpeg")
        return ffmpeg_exe_path

    except Exception as e:
        print(f" >> imageio_ffmpeg Error: {e}")
        return None

