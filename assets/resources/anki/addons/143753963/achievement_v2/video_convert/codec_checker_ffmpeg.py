# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

import platform
import subprocess

from .ffmpeg_path import get_ffmpeg_exe_path

MP4_ENCODERS = {
    "h264": "libx264",
    "hevc": "libx265",
}

def _get_ffmpeg_encoder_output(ffmpeg_path):
    if not ffmpeg_path:
        return False, ""

    try:
        creationflags = 0
        if platform.system() == "Windows":
            creationflags = subprocess.CREATE_NO_WINDOW

        result = subprocess.run(
            [ffmpeg_path, "-encoders"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=creationflags,
        )
    except (OSError, subprocess.SubprocessError):
        return False, ""

    return result.returncode == 0, result.stdout or ""


def get_ffmpeg_codec_info(ffmpeg_path=None):
    if ffmpeg_path is None:
        ffmpeg_path = get_ffmpeg_exe_path()

    executable_available, output = _get_ffmpeg_encoder_output(ffmpeg_path)
    codec_support = {
        codec: executable_available and encoder in output
        for codec, encoder in MP4_ENCODERS.items()
    }
    return executable_available, codec_support
