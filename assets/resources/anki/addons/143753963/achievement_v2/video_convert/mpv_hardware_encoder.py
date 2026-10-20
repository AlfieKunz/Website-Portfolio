# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

import os
import platform
import subprocess
import time

from .codec_checker_mpv import (
    _run_mpv_help_command,
    get_mpv_mp4_muxer_support,
)
from .ffmpeg_mp4_converter import print_conversion_details


MPV_HARDWARE_ENCODERS = {
    "h264_videotoolbox": ("h264", "b=5M"),
    "hevc_videotoolbox": ("hevc", "b=5M"),
    "h264_mf": ("h264", "b=5M"),
    "hevc_mf": ("hevc", "b=5M"),
}

HARDWARE_CODEC_PREFERENCE = (
    "h264_videotoolbox",
    "hevc_videotoolbox",
    "h264_mf",
    "hevc_mf",
)


def _emit_log(log_callback, text):
    if log_callback is not None:
        log_callback(text)


def get_mpv_hardware_encoder(mpv_path):
    mp4_muxer_available = get_mpv_mp4_muxer_support(mpv_path)
    if not mp4_muxer_available:
        return None

    executable_available, output = _run_mpv_help_command(
        mpv_path,
        "--ovc=help",
    )
    if not executable_available:
        return None

    for encoder in HARDWARE_CODEC_PREFERENCE:
        encoder_position = output.find(encoder)
        if encoder_position >= 0:
            return encoder
    return None


def _get_hardware_encoder_options(encoder):
    encoder_info = MPV_HARDWARE_ENCODERS.get(encoder)
    if encoder_info is None:
        return None
    return encoder_info[1]


def convert_to_mp4_with_mpv_hardware(
                            input_path,
                            output_path,
                            input_frame_rate=None,
                            encoder=None,
                            mpv_path=None,
                            stop_event=None,
                            process_holder=None,
                            log_callback=None,
                            ):
    if mpv_path is None:
        _emit_log(log_callback, "Error: mpv_path is None")
        return None

    if encoder is None:
        _emit_log(log_callback, "Error: hardware encoder is None")
        return None

    ovc_options = _get_hardware_encoder_options(encoder)
    if ovc_options is None:
        _emit_log(log_callback, f"Error: hardware encoder is not available: {encoder}")
        return None

    command_working_directory = None
    if input_frame_rate is not None:
        command_working_directory = os.path.dirname(input_path)
        input_path = "mf://" + os.path.basename(input_path)

    cmd = [
        mpv_path,
        input_path,
        f"--o={output_path}",
        "--of=mp4",
        f"--ovc={encoder}",
        f"--ovcopts={ovc_options}",
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
    codec_info = MPV_HARDWARE_ENCODERS.get(encoder)
    codec_mode = encoder
    if codec_info is not None:
        codec_mode = codec_info[0]
    print_conversion_details(
        output_path=output_path,
        process_returncode=process.returncode,
        elapsed_time=elapsed_time,
        conversion_mode="mpv-hardware",
        codec_mode=codec_mode,
        input_frame_rate=input_frame_rate,
        log_callback=log_callback,
    )

    if process.returncode != 0 or not os.path.isfile(output_path):
        return None
    return output_path
