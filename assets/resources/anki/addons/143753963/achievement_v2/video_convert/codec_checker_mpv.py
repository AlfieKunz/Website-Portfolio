# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

import os
import platform
import subprocess

MP4_ENCODERS = {
    "h264": "libx264",
    "hevc": "libx265",
}

def _run_mpv_help_command(mpv_path, option):
    if not mpv_path or not os.path.isfile(mpv_path):
        return False, ""

    try:
        creationflags = 0
        if platform.system() == "Windows":
            creationflags = subprocess.CREATE_NO_WINDOW

        result = subprocess.run(
            [mpv_path, option, "--no-config"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=creationflags,
        )
    except (OSError, subprocess.SubprocessError):
        return False, ""

    return True, result.stdout or ""


def get_mpv_mp4_muxer_support(mpv_path):
    executable_available, output = _run_mpv_help_command(mpv_path, "--of=help")
    if not executable_available:
        return False

    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.find("--of=mp4") == 0:
            return True
    return False


def get_mpv_codec_info(mpv_path):

    executable_available, output = _run_mpv_help_command(mpv_path, "--ovc=help")
    codec_support = {}
    for codec, encoder in MP4_ENCODERS.items():
        codec_support[codec] = False
        if executable_available:
            encoder_position = output.find(encoder)
            if encoder_position >= 0:
                codec_support[codec] = True

    return executable_available, codec_support
