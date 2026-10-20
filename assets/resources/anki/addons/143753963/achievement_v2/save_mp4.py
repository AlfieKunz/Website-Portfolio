# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

import os
import shutil
import tempfile
import threading
from os.path import join

from aqt.qt import QImage # PyQt6.QtGui
from aqt.qt import QFileDialog # PyQt6.QtWidgets
from aqt.qt import ( # PyQt6.QtCore
    QObject, QSize, QStandardPaths, Qt, QThread, QTimer, pyqtSignal,
    )

from .video_convert.ajt_utils_find_executable import find_executable
from .video_convert.codec_checker_ffmpeg import get_ffmpeg_codec_info
from .video_convert.codec_checker_mpv import get_mpv_codec_info
from .video_convert.ffmpeg_path import get_ffmpeg_exe_path
from .video_convert.ffmpeg_mp4_converter import (
    convert_to_mp4_with_ffmpeg,
    resolve_mp4_codec,
)
from .video_convert.mpv_get_exe_path import get_mpv_path
from .video_convert.mpv_mp4_converter import convert_to_mp4_with_mpv
from .video_convert.mpv_hardware_encoder import (
    convert_to_mp4_with_mpv_hardware,
    get_mpv_hardware_encoder,
)

import typing
if typing.TYPE_CHECKING:
    from .achiev_v2_main import AchievementWidget

# AchievementDialog -> save MP4


MP4_SECONDS = 3
MP4_FRAMES_PER_SECOND = 30
MP4_CAPTURE_INTERVAL_MILLISECONDS = 1000 // MP4_FRAMES_PER_SECOND
MP4_MAXIMUM_WIDTH_PIXELS = 1000
FRAME_FILE_NAME_FORMAT = "frame_%04d.png"
TEMP_DIRECTORY_PREFIX = "anki_leaderboard_mp4_"

# for debugging: "ffmpeg" or "mpv" forces one encoder, None = auto
FORCE_ENCODER_TOOL = None # "mpv"

NEED_FFMPEG_MESSAGE = "MP4 export requires ffmpeg. Please install ffmpeg on your PC."


#MARK: resolve_ffmpeg_encoder
def resolve_ffmpeg_encoder():
    ffmpeg_path = get_ffmpeg_exe_path()
    if not ffmpeg_path:
        return None

    executable_available, codec_support = get_ffmpeg_codec_info(ffmpeg_path)
    if not executable_available:
        return None

    codec = resolve_mp4_codec("auto", codec_support)
    if codec is None:
        return None
    return ("ffmpeg", ffmpeg_path, codec)


#MARK: resolve_mpv_encoder
def resolve_mpv_encoder():
    mpv_candidates = []
    for mpv_path in (find_executable("mpv"), get_mpv_path()):
        if mpv_path and mpv_path not in mpv_candidates:
            mpv_candidates.append(mpv_path)

    for mpv_path in mpv_candidates:
        mp4_muxer_available, codec_support = get_mpv_codec_info(mpv_path)
        if not mp4_muxer_available:
            continue
        codec = resolve_mp4_codec("auto", codec_support)
        if codec is None:
            hardware_encoder = get_mpv_hardware_encoder(mpv_path)
            if hardware_encoder is None:
                continue
            return ("mpv-hardware", mpv_path, hardware_encoder)
        return ("mpv", mpv_path, codec)
    return None


#MARK: resolve_mp4_encoder
def resolve_mp4_encoder():
    if FORCE_ENCODER_TOOL == "mpv":
        return resolve_mpv_encoder()

    encoder = resolve_ffmpeg_encoder()
    if encoder is not None:
        return encoder

    if FORCE_ENCODER_TOOL == "ffmpeg":
        return None

    return resolve_mpv_encoder()


#MARK: prepare_frame
def prepare_frame(image:QImage):
    source_width = image.width()
    if source_width > MP4_MAXIMUM_WIDTH_PIXELS:
        scale_ratio = MP4_MAXIMUM_WIDTH_PIXELS / source_width
        scaled_height = round(image.height() * scale_ratio)
        image = image.scaled(
            QSize(MP4_MAXIMUM_WIDTH_PIXELS, scaled_height),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    # yuv420p (used by H.264 / HEVC) requires even dimensions
    even_width = image.width() - (image.width() % 2)
    even_height = image.height() - (image.height() % 2)
    if even_width != image.width() or even_height != image.height():
        image = image.scaled(
            QSize(even_width, even_height),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.FastTransformation,
        )
    return image


#MARK: Mp4EncodeWorker
class Mp4EncodeWorker(QObject):

    saved = pyqtSignal(str)
    failed = pyqtSignal(str)
    aborted = pyqtSignal()

    def __init__(self, frames, output_path, tool, exe_path, codec):
        super().__init__()

        self.frames = frames
        self.output_path = output_path
        self.tool = tool
        self.exe_path = exe_path
        self.codec = codec
        self.stop_event = threading.Event()
        self.process_holder = {}

    #MARK: request_stop
    def request_stop(self):
        self.stop_event.set()
        process = self.process_holder.get("process")
        if process is not None:
            try:
                process.terminate()
            except Exception as e:
                print(f"Error: {e} ")

    #MARK: write_frames
    def write_frames(self, temp_directory):
        for frame_index, frame_image in enumerate(self.frames):
            frame_path = os.path.join(
                temp_directory, FRAME_FILE_NAME_FORMAT % frame_index)
            if not frame_image.save(frame_path, "PNG"):
                raise RuntimeError(f"failed to save frame: {frame_index}")
        return os.path.join(temp_directory, FRAME_FILE_NAME_FORMAT)

    #MARK: run
    def run(self):
        error_message = ""
        temp_directory = ""
        try:
            temp_directory = tempfile.mkdtemp(prefix=TEMP_DIRECTORY_PREFIX)
            frames_path = self.write_frames(temp_directory)

            if self.stop_event.is_set():
                self.aborted.emit()
                return

            if self.tool == "ffmpeg":
                output_path = convert_to_mp4_with_ffmpeg(
                                            input_path=frames_path,
                                            output_path=self.output_path,
                                            input_frame_rate=MP4_FRAMES_PER_SECOND,
                                            codec_mode=self.codec,
                                            ffmpeg_path=self.exe_path,
                                            stop_event=self.stop_event,
                                            process_holder=self.process_holder,
                                            )
            elif self.tool == "mpv-hardware":
                output_path = convert_to_mp4_with_mpv_hardware(
                                            input_path=frames_path,
                                            output_path=self.output_path,
                                            input_frame_rate=MP4_FRAMES_PER_SECOND,
                                            encoder=self.codec,
                                            mpv_path=self.exe_path,
                                            stop_event=self.stop_event,
                                            process_holder=self.process_holder,
                                            )
            else:
                output_path = convert_to_mp4_with_mpv(
                                            input_path=frames_path,
                                            output_path=self.output_path,
                                            input_frame_rate=MP4_FRAMES_PER_SECOND,
                                            codec_mode=self.codec,
                                            mpv_path=self.exe_path,
                                            stop_event=self.stop_event,
                                            process_holder=self.process_holder,
                                            )

            if self.stop_event.is_set():
                self.aborted.emit()
                return

            if output_path is None:
                error_message = f"failed to convert with {self.tool}."
        except Exception as error:
            error_message = str(error)
        finally:
            self.frames = []
            if temp_directory:
                shutil.rmtree(temp_directory, ignore_errors=True)

        if error_message:
            self.failed.emit(f"Error: save MP4:\n{error_message}")
        else:
            self.saved.emit(self.output_path)


#MARK: Mp4Recorder
class Mp4Recorder(QObject):

    recording_started = pyqtSignal()
    converting_started = pyqtSignal()
    saved = pyqtSignal(str)
    failed = pyqtSignal(str)
    aborted = pyqtSignal()

    def __init__(self, widget:"AchievementWidget", file_name="anki_leaderboard.mp4"):
        super().__init__(widget)

        self.widget = widget
        self.file_name = file_name
        self.frames = []
        self.area = None
        self.file_path = ""
        self.encoder = None
        self.conversion_thread = None
        self.conversion_worker = None
        self.capture_timer = QTimer(self)
        self.capture_timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.capture_timer.setInterval(MP4_CAPTURE_INTERVAL_MILLISECONDS)
        self.capture_timer.timeout.connect(self.capture_frame)

    #MARK: start
    def start(self, area):
        self.encoder = resolve_mp4_encoder()
        if self.encoder is None:
            self.failed.emit(NEED_FFMPEG_MESSAGE)
            return

        pictures_directory = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.PicturesLocation
        )
        if pictures_directory:
            default_path = join(pictures_directory, self.file_name)
        else:
            default_path = self.file_name

        file_path, _ = QFileDialog.getSaveFileName(
                                            self.widget,
                                            "Save MP4",
                                            default_path,
                                            "MP4 Video (*.mp4)")
        if not file_path:
            return
        if not file_path.lower().endswith(".mp4"):
            file_path += ".mp4"

        self.file_path = file_path
        self.area = area
        self.frames = []
        self.recording_started.emit()
        self.capture_frame()
        self.capture_timer.start()

    #MARK: capture_frame
    def capture_frame(self):
        if not self.widget.isVisible():
            self.capture_timer.stop()
            self.aborted.emit()
            return

        frame_image = self.widget.grab(self.area).toImage()
        rgb_image = frame_image.convertToFormat(QImage.Format.Format_RGB32)
        self.frames.append(prepare_frame(rgb_image))

        required_frame_count = MP4_SECONDS * MP4_FRAMES_PER_SECOND
        if len(self.frames) >= required_frame_count:
            self.capture_timer.stop()
            self.start_conversion()

    #MARK: start_conversion
    def start_conversion(self):
        frames = self.frames
        self.frames = []

        tool, exe_path, codec = self.encoder
        self.conversion_worker = Mp4EncodeWorker(
                                    frames=frames,
                                    output_path=self.file_path,
                                    tool=tool,
                                    exe_path=exe_path,
                                    codec=codec)

        self.conversion_thread = QThread(self)
        self.conversion_worker.moveToThread(self.conversion_thread)

        self.conversion_thread.started.connect(self.conversion_worker.run)
        self.conversion_worker.saved.connect(self.saved.emit)
        self.conversion_worker.failed.connect(self.failed.emit)
        self.conversion_worker.aborted.connect(self.aborted.emit)
        self.conversion_worker.saved.connect(self.conversion_thread.quit)
        self.conversion_worker.failed.connect(self.conversion_thread.quit)
        self.conversion_worker.aborted.connect(self.conversion_thread.quit)
        self.conversion_thread.finished.connect(self.conversion_worker.deleteLater)
        self.conversion_thread.finished.connect(self.conversion_thread.deleteLater)
        self.conversion_thread.finished.connect(self.on_conversion_finished)

        self.converting_started.emit()
        self.conversion_thread.start()

    #MARK: on_conversion_finished
    def on_conversion_finished(self):
        finished_thread = self.sender()
        if self.conversion_thread is not finished_thread:
            return
        self.conversion_worker = None
        self.conversion_thread = None

    #MARK: stop
    def stop(self):
        self.capture_timer.stop()

        conversion_worker = self.conversion_worker
        if conversion_worker is not None:
            conversion_worker.request_stop()

        conversion_thread = self.conversion_thread
        if conversion_thread is not None and conversion_thread.isRunning():
            conversion_thread.quit()
            conversion_thread.wait(5000)
