# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

# NOTE: Rewritten from the WebM converter. MP4 only (H.264 / HEVC).

import os
import time
import platform
import subprocess

from .codec_checker_ffmpeg import get_ffmpeg_codec_info


MP4_ENCODERS = {
    "h264": "libx264",
    "hevc": "libx265",
}
CODEC_PREFERENCE = ("h264", "hevc")
CODEC_DEFAULT_CRFS = {
    "h264": 23,
    "hevc": 28,
}


#MARK: _emit_log
def _emit_log(log_callback, text):
    if log_callback is not None:
        log_callback(text)


#MARK: resolve_mp4_codec
def resolve_mp4_codec(codec_mode, codec_support):
    codec_support = codec_support or {}

    if codec_mode != "auto":
        if codec_support.get(codec_mode):
            return codec_mode
        return None

    for codec in CODEC_PREFERENCE:
        if codec_support.get(codec):
            return codec
    return None


#MARK: print_conversion_details
def print_conversion_details(
                            output_path,
                            process_returncode,
                            elapsed_time,
                            conversion_mode,
                            codec_mode,
                            input_frame_rate,
                            log_callback=None,
                            ):
    output_exists = os.path.isfile(output_path)
    output_size = 0
    if output_exists:
        output_size = os.path.getsize(output_path)
    output_size_mb = output_size / (1024 * 1024)

    _emit_log(log_callback, "\nConversion details:")
    _emit_log(log_callback, f"  mode: {conversion_mode}")
    _emit_log(log_callback, f"  codec: {codec_mode}")
    _emit_log(log_callback, f"  input frame rate: {input_frame_rate}")
    _emit_log(log_callback, f"  output: {output_path}")
    _emit_log(log_callback, f"  output exists: {output_exists}")
    _emit_log(log_callback, f"  output size: {output_size_mb:.2f} MB")
    _emit_log(log_callback, f"  return code: {process_returncode}")
    _emit_log(log_callback, f"  elapsed time: {elapsed_time:.2f} sec")


#MARK: convert_to_mp4_with_ffmpeg
def convert_to_mp4_with_ffmpeg(
                            input_path,
                            output_path,
                            input_frame_rate=None,
                            codec_mode="auto",
                            crf=None,
                            ffmpeg_path="ffmpeg",
                            stop_event=None,
                            process_holder=None,
                            log_callback=None,
                            ffmpeg_codec_info=None,
                            ):

    if codec_mode == "auto":
        if ffmpeg_codec_info is None:
            ffmpeg_codec_info = get_ffmpeg_codec_info(ffmpeg_path)
        executable_available, codec_support = ffmpeg_codec_info
        if not executable_available:
            _emit_log(log_callback, "Error: ffmpeg is not available")
            return None
        codec_mode = resolve_mp4_codec(codec_mode, codec_support)

    encoder = MP4_ENCODERS.get(codec_mode) if codec_mode else None
    if encoder is None:
        _emit_log(log_callback, f"Error: codec is not available: {codec_mode}")
        return None

    if crf is None:
        crf_value = CODEC_DEFAULT_CRFS.get(codec_mode, 23)
    else:
        crf_value = crf

    cmd = [ffmpeg_path, "-y"]
    if input_frame_rate is not None:
        cmd += ["-framerate", str(input_frame_rate), "-start_number", "0"]
    cmd += ["-i", input_path]
    cmd += [
        "-an",
        "-c:v", encoder,
        "-crf", str(crf_value),
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_path,
    ]

    creationflags = 0
    if platform.system() == "Windows":
        creationflags = subprocess.CREATE_NO_WINDOW

    start_time = time.perf_counter()
    try:
        process = subprocess.Popen(
            cmd,
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
        conversion_mode="ffmpeg",
        codec_mode=codec_mode,
        input_frame_rate=input_frame_rate,
        log_callback=log_callback,
    )

    if process.returncode != 0 or not os.path.isfile(output_path):
        return None
    return output_path
