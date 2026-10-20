# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>

from os.path import join

from aqt.utils import tooltip

from aqt.qt import QDesktopServices, QImage, QSize, QStandardPaths, Qt, QUrl
from aqt.qt import QFileDialog

import typing
if typing.TYPE_CHECKING:
    from .achiev_v2_main import AchievementWidget

JPEG_MAXIMUM_WIDTH_PIXELS = 1000


#MARK: save_jpeg_image
def save_jpeg_image(widget:"AchievementWidget", area, value):
    pictures_directory = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.PicturesLocation
    )
    default_path = join(
        pictures_directory,
        f"anki_leaderboard_{value}days.jpg",
    ) if pictures_directory else f"anki_leaderboard_{value}days.jpg"

    file_path, _ = QFileDialog.getSaveFileName(
        widget,
        "Save JPEG",
        default_path,
        "JPEG Image (*.jpg *.jpeg)",
    )
    if not file_path:
        return
    if not file_path.lower().endswith((".jpg", ".jpeg")):
        file_path += ".jpg"

    image = widget.grab(area).toImage()
    image = image.convertToFormat(QImage.Format.Format_RGB32)
    source_width = image.width()
    if source_width > JPEG_MAXIMUM_WIDTH_PIXELS:
        scale_ratio = JPEG_MAXIMUM_WIDTH_PIXELS / source_width
        scaled_height = round(image.height() * scale_ratio)
        image = image.scaled(
            QSize(JPEG_MAXIMUM_WIDTH_PIXELS, scaled_height),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    if image.save(file_path, "JPEG", 95):
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
        tooltip(msg=f"Saved: \n{file_path}", parent=widget)
    else:
        tooltip(msg=f"Error: Failed to save JPEG", parent=widget)
