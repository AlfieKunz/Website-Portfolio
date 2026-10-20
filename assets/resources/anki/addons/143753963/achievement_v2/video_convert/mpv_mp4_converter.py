# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

# NOTE: Rewritten from the WebM converter. MP4 only (H.264 / HEVC).

import os
import time
import platform
import subprocess

from .codec_checker_mpv import get_mpv_codec_info
from .ffmpeg_mp4_converter import (
    CODEC_DEFAULT_CRFS,
    MP4_ENCODERS,
    _emit_log,
    print_conversion_details,
    resolve_mp4_codec,
)


#MARK: convert_to_mp4_with_mpv
def convert_to_mp4_with_mpv(
                            input_path,
                            output_path,
                            input_frame_rate=None,
                            codec_mode="auto",
                            crf=None,
                            mpv_path=None,
                            stop_event=None,
                            process_holder=None,
                            log_callback=None,
                            mpv_codec_info=None,
                            ):
    # input_path = a video file, or an image sequence pattern (e.g. frame_%04d.png).
    # set input_frame_rate when an image sequence is used.

    if mpv_path is None:
        _emit_log(log_callback, "Error: mpv_path is None")
        return None

    if mpv_codec_info is None and codec_mode == "auto":
        mpv_codec_info = get_mpv_codec_info(mpv_path)

    if mpv_codec_info is not None:
        mp4_muxer_available, codec_support = mpv_codec_info
        if not mp4_muxer_available:
            _emit_log(log_callback, "Error: mpv can not output mp4")
            return None
        if codec_mode == "auto":
            codec_mode = resolve_mp4_codec(codec_mode, codec_support)

    encoder = MP4_ENCODERS.get(codec_mode) if codec_mode else None
    if encoder is None:
        _emit_log(log_callback, f"Error: codec is not available: {codec_mode}")
        return None

    if crf is None:
        crf_value = CODEC_DEFAULT_CRFS.get(codec_mode, 23)
    else:
        crf_value = crf

    command_working_directory = None
    if input_frame_rate is not None:
        # image sequence input: pass the pattern as a relative mf:// url
        command_working_directory = os.path.dirname(input_path)
        input_path = "mf://" + os.path.basename(input_path)

    cmd = [
        mpv_path,
        input_path,
        f"--o={output_path}",
        "--of=mp4",
        f"--ovc={encoder}",
        f"--ovcopts=crf={crf_value}",
        "--aid=no",
        "--no-config",
        "--vf=lavfi=[format=yuv420p]",
        "--terminal=no",
        "--msg-level=all=v",
    ]
    if input_frame_rate is not None:
        cmd.append(f"--mf-fps={input_frame_rate}")

    creationflags = 0
    if platform.system() == "Windows":
        creationflags = subprocess.CREATE_NO_WINDOW

    start_time = time.perf_counter()
    try:
        process = subprocess.Popen(
            cmd,
            cwd=command_working_directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=creationflags,
        )
    except OSError as error:
        _emit_log(log_callback, f"Error: {error}")
        return None

    if process_holder is not None:
        process_holder["process"] = process

    for line in process.stdout:
        _emit_log(log_callback, line)
        if stop_event is not None and stop_event.is_set():
            process.terminate()
            break

    process.wait()
    if process_holder is not None:
        process_holder.pop("process", None)

    elapsed_time = time.perf_counter() - start_time
    print_conversion_details(
        output_path=output_path,
        process_returncode=process.returncode,
        elapsed_time=elapsed_time,
        conversion_mode="mpv",
        codec_mode=codec_mode,
        input_frame_rate=input_frame_rate,
        log_callback=log_callback,
    )

    if process.returncode != 0 or not os.path.isfile(output_path):
        return None
    return output_path
