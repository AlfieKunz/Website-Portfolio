# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

import struct
from os.path import join

from aqt.qt import QImage, QPainter # PyQt6.QtGui
from aqt.qt import QFileDialog # PyQt6.QtWidgets
from aqt.qt import ( # PyQt6.QtCore
    QObject, QSize, QStandardPaths, Qt, QThread, QTimer, pyqtSignal,
    )


GIF_SECONDS = 3
GIF_FRAMES_PER_SECOND = 10
GIF_DELAY_CENTISECONDS = 100 // GIF_FRAMES_PER_SECOND
GIF_CAPTURE_INTERVAL_MILLISECONDS = 1000 // GIF_FRAMES_PER_SECOND
GIF_MAXIMUM_WIDTH_PIXELS = 320


import typing
if typing.TYPE_CHECKING:
    from .achiev_v2_main import AchievementWidget

# AchievementDialog -> save Gif (beta)


#MARK: GifEncoder
class GifEncoder:

    def __init__(self, images:list[QImage], delay_centiseconds):

        self.images = images
        self.delay_centiseconds = delay_centiseconds
        self.width = images[0].width()
        self.height = images[0].height()

    #MARK: build
    def build(self):

        palette = self.shared_palette()

        # b"GIF89a" -> GIF
        gif_header = b"GIF89a"
        gif_data = bytearray(gif_header)

        # 
        packed_fields = 0x87
        background_color_index = 0
        pixel_aspect_ratio = 0
        screen_descriptor_format = "<HHBBB"
        screen_descriptor = struct.pack(
            screen_descriptor_format,
            self.width,
            self.height,
            packed_fields,
            background_color_index,
            pixel_aspect_ratio,
        )
        gif_data += screen_descriptor

        color_table_data = self._color_table_bytes(palette)
        gif_data += color_table_data

        loop_extension = b"\x21\xFF\x0BNETSCAPE2.0\x03\x01\x00\x00\x00"
        gif_data += loop_extension

        for frame_image in self.images:
            indexed_image = frame_image.convertToFormat(
                QImage.Format.Format_Indexed8, palette, Qt.ImageConversionFlag.AutoColor
            )

            graphic_control_extension_header = b"\x21\xF9\x04\x04"
            frame_delay_format = "<H"
            frame_delay_bytes = struct.pack(frame_delay_format, self.delay_centiseconds)
            transparent_color_index = b"\x00"
            block_terminator = b"\x00"
            graphic_control_extension = (
                graphic_control_extension_header
                + frame_delay_bytes
                + transparent_color_index
                + block_terminator
            )
            gif_data += graphic_control_extension

            image_separator = b"\x2C"
            image_left = 0
            image_top = 0
            image_descriptor_format = "<HHHH"
            image_position_and_size = struct.pack(
                image_descriptor_format,
                image_left,
                image_top,
                self.width,
                self.height,
            )
            image_descriptor_packed_fields = b"\x00"
            image_descriptor = (
                image_separator
                + image_position_and_size
                + image_descriptor_packed_fields
            )
            gif_data += image_descriptor

            minimum_code_size_byte = b"\x08"
            gif_data += minimum_code_size_byte

            index_bytes = self._image_to_index_bytes(indexed_image)
            compressed_data = self._lzw_encode(index_bytes)
            for block_start in range(0, len(compressed_data), 255):
                sub_block_data = compressed_data[block_start:block_start + 255]
                sub_block_size = len(sub_block_data)
                gif_data.append(sub_block_size)
                gif_data += sub_block_data
            gif_data.append(0)

        gif_trailer = b"\x3B"
        gif_data += gif_trailer
        return bytes(gif_data)

    #MARK: shared_palette
    def shared_palette(self):

        image_count = len(self.images)
        sample_indices = (0, image_count // 3, (2 * image_count) // 3, image_count - 1)

        montage = QImage(self.width * 2, self.height * 2, QImage.Format.Format_RGB32)
        painter = QPainter(montage)
        for position, sample_index in enumerate(sample_indices):
            sample_image = self.images[sample_index]
            column = position % 2
            row = position // 2
            x_position = column * self.width
            y_position = row * self.height
            painter.drawImage(x_position, y_position, sample_image)
        painter.end()

        indexed_montage = montage.convertToFormat(QImage.Format.Format_Indexed8)
        color_table = indexed_montage.colorTable()
        return color_table

    #MARK: _lzw_encode
    def _lzw_encode(self, indices, minimum_code_size=8):

        clear_code = 1 << minimum_code_size
        end_code = clear_code + 1

        output_data = bytearray()
        bit_buffer = 0
        bit_count = 0
        code_size = minimum_code_size + 1
        next_code = end_code + 1
        code_table = {}

        def emit_code(code):
            nonlocal bit_buffer, bit_count
            bit_buffer |= code << bit_count
            bit_count += code_size
            while bit_count >= 8:
                output_byte = bit_buffer & 0xFF
                output_data.append(output_byte)
                bit_buffer >>= 8
                bit_count -= 8

        emit_code(clear_code)
        prefix_code = indices[0]
        for pixel_index in indices[1:]:
            table_key = (prefix_code << 8) | pixel_index
            existing_code = code_table.get(table_key)
            if existing_code is not None:
                prefix_code = existing_code
                continue

            emit_code(prefix_code)
            if next_code < 4096:
                code_table[table_key] = next_code
                next_code += 1
                if next_code == (1 << code_size) + 1 and code_size < 12:
                    code_size += 1
            else:
                emit_code(clear_code)
                code_table.clear()
                next_code = end_code + 1
                code_size = minimum_code_size + 1
            prefix_code = pixel_index

        emit_code(prefix_code)
        emit_code(end_code)
        if bit_count > 0:
            final_byte = bit_buffer & 0xFF
            output_data.append(final_byte)
        return bytes(output_data)

    #MARK: _image_to_index_bytes
    def _image_to_index_bytes(self, image:QImage):

        pointer = image.constBits()
        data_size = image.sizeInBytes()
        try:
            all_bytes = pointer.asstring(data_size)
        except AttributeError:
            pointer.setsize(data_size)
            all_bytes = bytes(pointer)
        if isinstance(all_bytes, str):
            all_bytes = all_bytes.encode("latin-1")

        width = image.width()
        height = image.height()
        bytes_per_line = image.bytesPerLine()
        if bytes_per_line == width:
            return all_bytes

        index_bytes = bytearray()
        for row_index in range(height):
            row_start = row_index * bytes_per_line
            row_data = all_bytes[row_start:row_start + width]
            index_bytes += row_data
        return bytes(index_bytes)

    #MARK: _color_table_bytes
    def _color_table_bytes(self, colors):

        color_table_data = bytearray()
        for color in colors[:256]:
            red = (color >> 16) & 0xFF
            green = (color >> 8) & 0xFF
            blue = color & 0xFF
            rgb_color_format = "<BBB"
            rgb_bytes = struct.pack(rgb_color_format, red, green, blue)
            color_table_data += rgb_bytes

        if len(color_table_data) < 768:
            padding_size = 768 - len(color_table_data)
            color_table_data += bytes(padding_size)
        return bytes(color_table_data)


#MARK: GifEncodeWorker
class GifEncodeWorker(QObject):

    saved = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(self, frames, output_path):
        super().__init__()

        self.frames = frames
        self.output_path = output_path

    #MARK: run
    def run(self):
        error_message = ""
        try:
            encoder = GifEncoder(self.frames, GIF_DELAY_CENTISECONDS)
            gif_data = encoder.build()
            with open(self.output_path, "wb") as output_file:
                output_file.write(gif_data)
        except Exception as error:
            error_message = str(error)

        self.frames = []
        if error_message:
            self.failed.emit(error_message)
        else:
            self.saved.emit(self.output_path)


#MARK: GifRecorder
class GifRecorder(QObject):

    recording_started = pyqtSignal()
    converting_started = pyqtSignal()
    saved = pyqtSignal(str)
    failed = pyqtSignal(str)
    aborted = pyqtSignal()

    def __init__(self, widget:"AchievementWidget", file_name="anki_leaderboard.gif"):
        super().__init__(widget)

        self.widget = widget
        self.file_name = file_name
        self.frames = []
        self.area = None
        self.file_path = ""
        self.conversion_thread = None
        self.conversion_worker = None
        self.capture_timer = QTimer(self)
        self.capture_timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.capture_timer.setInterval(GIF_CAPTURE_INTERVAL_MILLISECONDS)
        self.capture_timer.timeout.connect(self.capture_frame)

    #MARK: start
    def start(self, area):

        pictures_directory = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.PicturesLocation
        )
        if pictures_directory:
            default_path = join(pictures_directory, self.file_name)
        else:
            default_path = self.file_name

        file_path, _ = QFileDialog.getSaveFileName(
                                            self.widget,
                                            "Save GIF",
                                            default_path,
                                            "GIF Image (*.gif)")
        if not file_path:
            return
        if not file_path.lower().endswith(".gif"):
            file_path += ".gif"

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

        source_width = rgb_image.width()
        if source_width > GIF_MAXIMUM_WIDTH_PIXELS:
            scale_ratio = GIF_MAXIMUM_WIDTH_PIXELS / source_width
            scaled_height = round(rgb_image.height() * scale_ratio)
            target_size = QSize(GIF_MAXIMUM_WIDTH_PIXELS, scaled_height)
            rgb_image = rgb_image.scaled(
                target_size,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

        self.frames.append(rgb_image)

        required_frame_count = GIF_SECONDS * GIF_FRAMES_PER_SECOND
        if len(self.frames) >= required_frame_count:
            self.capture_timer.stop()
            self.start_conversion()

    #MARK: start_conversion
    def start_conversion(self):
        frames = self.frames
        self.frames = []

        self.conversion_worker = GifEncodeWorker(
                                    frames=frames,
                                    output_path=self.file_path)

        self.conversion_thread = QThread(self)
        self.conversion_worker.moveToThread(self.conversion_thread)

        self.conversion_thread.started.connect(self.conversion_worker.run)
        self.conversion_worker.saved.connect(self.saved.emit)
        self.conversion_worker.failed.connect(self.failed.emit)
        self.conversion_worker.saved.connect(self.conversion_thread.quit)
        self.conversion_worker.failed.connect(self.conversion_thread.quit)
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
        conversion_thread = self.conversion_thread
        if conversion_thread is not None and conversion_thread.isRunning():
            conversion_thread.quit()
            conversion_thread.wait(5000)
