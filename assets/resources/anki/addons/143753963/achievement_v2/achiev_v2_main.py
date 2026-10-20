# Anki Leaderboard
# Copyright (C) 2020 - 2024 Thore Tyborski <https://github.com/ThoreBor>
# Copyright (C) 2024 Shigeyuki <http://patreon.com/Shigeyuki>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import os
from html import escape
import datetime

from aqt import mw
from aqt.utils import tooltip, openLink

from aqt.qt import ( # PyQt6.QtCore
    QSize, Qt, QUrl
)
from aqt.qt import ( # PyQt6.QtGui
    QAction, QColor, QDesktopServices, QFontDatabase, QIcon, QMovie, QPixmap
)
from aqt.qt import ( # PyQt6.QtWidgets
    QCheckBox, QFrame, QGraphicsDropShadowEffect, QGridLayout, QHBoxLayout, QLabel,
    QInputDialog, QMenu, QPushButton, QSizePolicy, QVBoxLayout, QWidget,
)

from .save_jpeg import save_jpeg_image
from .config_local import get_local_config, save_local_config
from .rate_limit_timer import rate_limiter
from . import ADDON_NAME, PATREON_URL, RATE_THIS_URL, WINDOW_TITLE

ACHIEV_DIR = os.path.dirname(os.path.realpath(__file__))

CONFETTI_PATH = os.path.join(ACHIEV_DIR, "gifs", "confetti.gif")

HAPPY_ANKI_TAN_PATH = os.path.join(ACHIEV_DIR, "gifs", "happy-happy-anki-tan.gif")
NOT_FOUND_ANKI_TAN_PATH = os.path.join(ACHIEV_DIR, "gifs", "not-found-anki-tan.gif")
FONT_PATH = os.path.join(ACHIEV_DIR, "font", "CherryBombOne-Regular.ttf")

WINDOW_ICON_PATH = os.path.join(ACHIEV_DIR, "icons", "shige_icon.png")
PR_TEXT_CLOSE_ICON_PATH = os.path.join(ACHIEV_DIR, "icons", "close.svg")
DIALOG_SIZE = 400
CONTENT_SIZE = DIALOG_SIZE - 18
IMAGE_AREA_SIZE = 360
CONTROL_HEIGHT = 50


FONT_FAMILY = None
TEXT_OFFSET_PX = 100

USER_NAME = "USER_NAME"
STREAK_COUNT = 365

PR_TEXT = (
            f"Did you like the {ADDON_NAME}? "
            f"Please support the development by rating the add-on or donating via Patreon!")

ANKITAN_WIKI_URL = "https://shigeyukey.github.io/shige-addons-wiki/Anki-tan.html"


#MARK: load_font
def load_font():
    global FONT_FAMILY

    if FONT_FAMILY is None:
        font_id = QFontDatabase.addApplicationFont(FONT_PATH)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                FONT_FAMILY = font_families[0]

    return FONT_FAMILY


#MARK: mini_button_v3
def mini_button_v3(button:QPushButton):
    button.setStyleSheet("QPushButton { padding: 2px 8px; }")
    button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
    button.setFocusPolicy(Qt.FocusPolicy.NoFocus)


#MARK: update_lo_config
def update_lo_config(key_name, new_value):
    try:
        lo_config = get_local_config()
        lo_config[key_name] = bool(new_value)
        save_local_config(lo_config)
    except Exception as e:
        print(f"[{ADDON_NAME}] Error: {e} ")


#MARK: AchievementWidget
class AchievementWidget(QWidget):

    def __init__(self, value, user_name, parent):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.setWindowFlags(Qt.WindowType.Tool)

        self.is_zero_streak = (value == 0)

        self.setWindowTitle(WINDOW_TITLE)
        # self.setFixedSize(DIALOG_SIZE, DIALOG_SIZE + CONTROL_HEIGHT)

        lo_config = get_local_config()
        achiev_streak_popup = lo_config.get("achiev_streak_popup", True)
        achiev_anki_tan = lo_config.get("achiev_anki_tan", True)
        self.achiev_anki_tan = achiev_anki_tan
        self.pr_text_dismissed = bool(
            lo_config.get("achiev_pr_text_hidden", False))

        self.confetti = QLabel(self)

        self.confetti.setStyleSheet("background: lightblue")
        # self.confetti.setStyleSheet("background: #222222")
        self.confetti.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message = QLabel(self)
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.text_offset_px = 0
        if self.achiev_anki_tan:
            self.text_offset_px = TEXT_OFFSET_PX

        message_style = (
            "font-size: 20pt; font-weight: bold; color: white; "
            f"padding-bottom: {self.text_offset_px}px")

        font_family = load_font()
        if font_family:
            message_style = f'font-family: "{font_family}"; {message_style}'
        self.message.setStyleSheet(message_style)

        ADDON_PACKAGE = mw.addonManager.addonFromModule(__name__)
        self.title = QLabel(f" {ADDON_NAME} {ADDON_PACKAGE}", self)

        title_style = (
            "font-size: 12pt; color: white; background: transparent; "
            "font-weight: bold;")

        if font_family:
            title_style = f'font-family: "{font_family}"; {title_style}'

        self.title.setStyleSheet(title_style)
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.title.setVisible(self.achiev_anki_tan)

        self.add_outline(self.title)
        self.add_outline(self.message)

        self.qlabel_anki_tan = QLabel(self)
        self.qlabel_anki_tan.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.qlabel_anki_tan.setVisible(self.achiev_anki_tan)
        # streak 0 shows the "not found" Anki-tan instead
        anki_tan_path = HAPPY_ANKI_TAN_PATH
        if self.is_zero_streak:
            anki_tan_path = NOT_FOUND_ANKI_TAN_PATH

        self.anki_tan_movie = QMovie(anki_tan_path, parent=self)
        self.qlabel_anki_tan.setMovie(self.anki_tan_movie)
        self.anki_tan_movie.start()

        self.image_widget = QWidget(self)
        self.image_widget.setFixedSize(QSize(IMAGE_AREA_SIZE, IMAGE_AREA_SIZE))

        image_layout = QGridLayout(self.image_widget)
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.addWidget(self.confetti, 0, 0)
        image_layout.addWidget(
            self.qlabel_anki_tan,
            0,
            0,
            alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,)
        image_layout.addWidget(self.message, 0, 0)
        image_layout.addWidget(
            self.title,
            0,
            0,
            alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,)

        checkbox_layout = QHBoxLayout()

        self.checkbox = QCheckBox("Enable-Auto-Popup")
        self.checkbox.setChecked(achiev_streak_popup)
        self.checkbox.setToolTip(
                            " Auto pop up this window \n"
                            " when you achieve Streak ")
        self.checkbox.clicked.connect(self.toggle_streak_popup)

        self.checkbox_02 = QCheckBox("Anki-tan")
        self.checkbox_02.setChecked(achiev_anki_tan)
        
        self.checkbox_02.setToolTip(
                            " Anki-tan is the unofficial mascot character, \n"
                            " her birthday is April 1. ")
        
        self.checkbox_02.clicked.connect(self.toggle_anki_tan)

        checkbox_layout.addStretch()
        checkbox_layout.addWidget(self.checkbox)
        checkbox_layout.addWidget(self.checkbox_02)


        #MARK: Context menu
        self.save_gif_action = QAction("Save GIF", self)
        self.save_gif_action.triggered.connect(self.save_gif)

        self.save_jpeg_action = QAction("Save JPEG", self)
        self.save_jpeg_action.triggered.connect(self.save_jpeg)

        self.save_mp4_action = QAction("Save MP4", self)
        self.save_mp4_action.triggered.connect(self.save_mp4)
        
        self.open_ankitan_wiki = QAction("📖Anki-tan Wiki")
        self.open_ankitan_wiki.triggered.connect(lambda:openLink(ANKITAN_WIKI_URL))

        self.set_user_name_action = QAction("Set User Name", self)
        self.set_user_name_action.triggered.connect(self.edit_user_name)


        #MARK: buttons


        button_layout = QHBoxLayout()

        self.button_one = QPushButton("👍️Rate This")
        self.button_one.setToolTip(
                    f" Did you like the Leaderboard? \n"
                    f" Please rate the add-on!")

        mini_button_v3(self.button_one)
        self.button_one.clicked.connect(
            lambda checked=False: openLink(RATE_THIS_URL))

        self.button_three = QPushButton("💖Become Patron")
        mini_button_v3(self.button_three)
        self.button_three.setToolTip(
                                f" If you support me on Patreon you'll \n"
                                f" get access to exclusive add-ons!"
                                )
        self.button_three.clicked.connect(
            lambda checked=False: openLink(PATREON_URL)
        )

        close_button = QPushButton("OK (close)")
        close_button.setFixedWidth(120)
        close_button.clicked.connect(self.close)

        button_layout.addWidget(close_button)

        button_layout.addStretch()
        button_layout.addWidget(self.button_one)
        button_layout.addWidget(self.button_three)
        # button_layout.addWidget(button_two)

        self.setup_pr_text_widget()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(9, 9, 9, 9)
        layout.addWidget(self.image_widget, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(checkbox_layout)
        layout.addWidget(self.pr_text_frame)
        layout.addLayout(button_layout)

        self.message.raise_()

        self.value = value
        self.user_name = user_name

        # lazy load: created when the context menu is used
        self.gif_recorder = None
        self.mp4_recorder = None

        self.button_one.setVisible(self.achiev_anki_tan)
        self.button_three.setVisible(self.achiev_anki_tan)
        self.update_pr_text_visibility()

        self.setupUI()


    # MARK: setup_pr_text_widget
    def setup_pr_text_widget(self):
        self.pr_text_frame = QFrame(self)
        self.pr_text_frame.setObjectName("pr_text_frame")
        self.pr_text_frame.setStyleSheet(
            "QFrame#pr_text_frame { border: 1px solid #808080; border-radius: 6px; }"
        )

        pr_text_layout = QHBoxLayout(self.pr_text_frame)
        pr_text_layout.setContentsMargins(8, 4, 8, 6)
        pr_text_layout.setSpacing(8)

        self.pr_text_close_button = QPushButton("x", self.pr_text_frame)
        self.pr_text_close_button.setFixedSize(16, 16)
        self.pr_text_close_button.setFlat(True)
        self.pr_text_close_button.setText("")
        self.pr_text_close_button.setIcon(QIcon(PR_TEXT_CLOSE_ICON_PATH))
        self.pr_text_close_button.setIconSize(QSize(16, 16))
        self.pr_text_close_button.setStyleSheet(
            "QPushButton { border: none; padding: 0; }"
        )
        self.pr_text_close_button.clicked.connect(self.dismiss_pr_text)

        self.pr_text_label = QLabel(PR_TEXT, self.pr_text_frame)
        self.pr_text_label.setWordWrap(True)
        self.pr_text_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.pr_text_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        pr_text_layout.addWidget(self.pr_text_label, 1, Qt.AlignmentFlag.AlignTop)
        pr_text_layout.addWidget(
            self.pr_text_close_button,
            0,
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop,
        )


    #MARK: toggle_streak_popup
    def toggle_streak_popup(self, checked):
        update_lo_config("achiev_streak_popup", checked)
        if checked:
            tooltip(" When you achieve a streak\nthis window will pop up! :-) ", parent=self)
        else:
            tooltip(" Hide this window :-( ", parent=self)


    #MARK: toggle_anki_tan
    def toggle_anki_tan(self, checked):
        update_lo_config("achiev_anki_tan", checked)
        self.achiev_anki_tan = checked
        self.text_offset_px = 0
        if self.achiev_anki_tan:
            self.text_offset_px = TEXT_OFFSET_PX
        self.qlabel_anki_tan.setVisible(self.achiev_anki_tan)
        self.title.setVisible(self.achiev_anki_tan)
        self.button_one.setVisible(self.achiev_anki_tan)
        self.button_three.setVisible(self.achiev_anki_tan)
        self.update_pr_text_visibility()
        self.update_message_style()
        self.update_message()
        self.adjustSize()


    # MARK: update_pr_text_visibility
    def update_pr_text_visibility(self):
        should_show = self.achiev_anki_tan and not self.pr_text_dismissed
        self.pr_text_frame.setVisible(should_show)


    # MARK: dismiss_pr_text
    def dismiss_pr_text(self, checked=False):
        self.pr_text_dismissed = True
        update_lo_config("achiev_pr_text_hidden", True)
        self.update_pr_text_visibility()
        self.adjustSize()


    #MARK: setupUI
    def setupUI(self):
        if self.is_zero_streak:
            # no confetti for a 0 day streak
            self.gif = None
        else:
            self.gif = QMovie(CONFETTI_PATH, parent=self)
            self.gif.jumpToFrame(0)
            original_size = self.gif.frameRect().size()

            if not original_size.isEmpty():
                scaled_size = original_size.scaled(
                    QSize(CONTENT_SIZE, CONTENT_SIZE),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,)
                self.gif.setScaledSize(scaled_size)

            self.confetti.setMovie(self.gif)
            self.gif.start()

        icon = QIcon()
        icon.addPixmap(QPixmap(WINDOW_ICON_PATH), QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(icon)

        self.update_message()


    # MARK: showEvent
    def showEvent(self, event):
        super().showEvent(event)

        try:
            self.adjustSize()

            parent_widget = self.parentWidget()
            if parent_widget is None:
                return

            frame_geometry = self.frameGeometry()
            frame_geometry.moveCenter(parent_widget.frameGeometry().center())
            self.move(frame_geometry.topLeft())

        except Exception as e:
            print(f"[{ADDON_NAME}] Error: {e} ")
            return

    #MARK: update_message_style
    def update_message_style(self):
        message_style = (
            "font-size: 20pt; font-weight: bold; color: white; "
            f"padding-bottom: {self.text_offset_px}px")

        font_family = load_font()
        if font_family:
            message_style = f'font-family: "{font_family}"; {message_style}'
        self.message.setStyleSheet(message_style)

    #MARK: update_message
    def update_message(self):
        user_name = self.sanitize_user_name(self.user_name)
        name_message = ""
        if self.achiev_anki_tan:
            if user_name:
                name_message_02 = f"<br>{user_name}!"
            else:
                name_message_02 = ""

            if self.is_zero_streak:
                name_message = f"Hello,{name_message_02}<br>"
            else:
                name_message = f"Congratz,{name_message_02}<br>"

        if self.is_zero_streak:
            message = f"{name_message}Streak not found?"
        else:
            message = f"{name_message}{self.value} day streak!"

            if (isinstance(self.value, int)
                and self.value % 365 == 0):
                years = self.value // 365
                if years == 1:
                    year_text = "year"
                else:
                    year_text = "years"
                message += f"<br>That's {years} {year_text}!"

        self.message.setText(message)

    #MARK: add_outline
    def add_outline(self, widget:"QLabel"):
        outline = QGraphicsDropShadowEffect(widget)
        outline.setBlurRadius(5)
        outline.setColor(QColor("black"))
        outline.setOffset(0, 0)
        widget.setGraphicsEffect(outline)


    #MARK: sanitize_user_name
    def sanitize_user_name(self, user_name):
        if user_name is None:
            return None
        user_name = re.sub(r"[\x00-\x1f\x7f]", "", str(user_name))
        return escape(user_name, quote=True)

    #MARK: edit_user_name
    def edit_user_name(self, checked=False):
        current_user_name = self.user_name
        if current_user_name is None:
            current_user_name = ""

        entered_user_name, accepted = QInputDialog.getText(
            self,
            "Set User Name",
            "Enter your name:",
            text=current_user_name,)

        if not accepted:
            return

        safe_user_name = re.sub(r"[\x00-\x1f\x7f]", "", entered_user_name).strip()
        if not safe_user_name:
            safe_user_name = None

        try:
            lo_config = get_local_config()
            lo_config["achiev_user_name"] = safe_user_name
            save_local_config(lo_config)
        except Exception as e:
            print(f"[{ADDON_NAME}] Error: {e} ")
            return

        self.user_name = safe_user_name
        self.update_message()


    #MARK: contextMenuEvent
    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        context_menu.addAction(self.save_jpeg_action)
        context_menu.addAction(self.save_gif_action)
        context_menu.addAction(self.save_mp4_action)
        context_menu.addAction(self.open_ankitan_wiki)
        context_menu.addAction(self.set_user_name_action)
        

        context_menu.exec(event.globalPos())

    #MARK: get_gif_recorder
    def get_gif_recorder(self):
        if self.gif_recorder is None:
            try:
                from .save_gif import GifRecorder

                self.gif_recorder = GifRecorder(
                    self, file_name=f"anki_leaderboard_{self.value}days.gif")

                self.gif_recorder.recording_started.connect(self.on_gif_recording_started)
                self.gif_recorder.converting_started.connect(self.on_gif_converting_started)
                self.gif_recorder.saved.connect(self.on_gif_saved)
                self.gif_recorder.failed.connect(self.on_gif_failed)
                self.gif_recorder.aborted.connect(self.reset_save_gif_action)
            except Exception as e:
                print(f"[{ADDON_NAME}] Error: {e} ")
                tooltip(msg=f"Error: save GIF:\n{e}", parent=self)
                self.gif_recorder = None
        return self.gif_recorder


    #MARK: save_gif
    def save_gif(self):
        tooltip(msg="now loading...", parent=self)
        gif_recorder = self.get_gif_recorder()
        if gif_recorder is None:
            return
        gif_recorder.start(self.image_widget.geometry())


    #MARK: save_jpeg
    def save_jpeg(self):
        save_jpeg_image(self, self.image_widget.geometry(), self.value)


    #MARK: get_mp4_recorder
    def get_mp4_recorder(self):
        if self.mp4_recorder is None:
            try:
                from .save_mp4 import Mp4Recorder

                self.mp4_recorder = Mp4Recorder(
                    self, file_name=f"anki_leaderboard_{self.value}days.mp4")

                self.mp4_recorder.recording_started.connect(self.on_mp4_recording_started)
                self.mp4_recorder.converting_started.connect(self.on_mp4_converting_started)
                self.mp4_recorder.saved.connect(self.on_mp4_saved)
                self.mp4_recorder.failed.connect(self.on_mp4_failed)
                self.mp4_recorder.aborted.connect(self.reset_save_mp4_action)

            except Exception as e:
                print(f"[{ADDON_NAME}] Error: {e} ")
                tooltip(msg=f"Error: save MP4:\n{e}", parent=self)
                self.mp4_recorder = None

        return self.mp4_recorder


    #MARK: save_mp4
    def save_mp4(self):
        tooltip(msg="now loading...", parent=self)
        mp4_recorder = self.get_mp4_recorder()
        if mp4_recorder is None:
            return
        mp4_recorder.start(self.image_widget.geometry())


    #MARK: gif_callbacks
    def on_gif_recording_started(self):
        self.save_gif_action.setText("Recording...")
        self.save_gif_action.setEnabled(False)


    def on_gif_converting_started(self):
        self.save_gif_action.setText("Converting...")


    def on_gif_saved(self, file_path):
        self.reset_save_gif_action()
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
        tooltip(msg=f"Saved: {file_path}", parent=self)


    def on_gif_failed(self, error_message):
        self.reset_save_gif_action()
        tooltip(msg=f"Error: save GIF:\n{error_message}", parent=self)


    #MARK: reset_save_gif_action
    def reset_save_gif_action(self):
        self.save_gif_action.setText("Save GIF")
        self.save_gif_action.setEnabled(True)


    #MARK: mp4_callbacks
    def on_mp4_recording_started(self):
        self.save_mp4_action.setText("Recording...")
        self.save_mp4_action.setEnabled(False)


    def on_mp4_converting_started(self):
        self.save_mp4_action.setText("Converting...")


    def on_mp4_saved(self, file_path):
        self.reset_save_mp4_action()
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
        tooltip(msg=f"Saved: {file_path}", parent=self)


    def on_mp4_failed(self, error_message):
        self.reset_save_mp4_action()
        tooltip(msg=error_message, parent=self)


    #MARK: reset_save_mp4_action
    def reset_save_mp4_action(self):
        self.save_mp4_action.setText("Save MP4")
        self.save_mp4_action.setEnabled(True)


    #MARK: close
    def closeEvent(self, event):
        global achievement_widget

        if self.gif_recorder is not None:
            self.gif_recorder.stop()
        if self.mp4_recorder is not None:
            self.mp4_recorder.stop()
        if self.gif is not None:
            self.gif.stop()
        self.anki_tan_movie.stop()

        if achievement_widget is self:
            achievement_widget = None

        event.accept()


#MARK: get_streak_count
def get_streak_count():
    from .stats_v2 import streak
    streak_count = streak()
    username = None
    
    return streak_count, username


#MARK: check_achievement
def check_achievement(streak):
    if streak == 0:
        return False

    def is_repeating_number(number):
        streak_string = str(number)

        if len(streak_string) < 3:
            return False

        first_character = streak_string[0]
        for character in streak_string:
            if character != first_character:
                return False
        return True

    is_hundred_days_milestone = (streak % 100 == 0)
    is_yearly_milestone = (streak % 365 == 0)
    is_fixed_days_milestone = streak in (7, 31, 60)
    is_repeating_digits_milestone = is_repeating_number(streak)

    if (is_hundred_days_milestone
        or is_yearly_milestone
        or is_fixed_days_milestone
        or is_repeating_digits_milestone):
        return True

    return False


#MARK: get_today_popup_date
def get_today_popup_date():

    from .get_rollover import get_rollover_hour
    rolloverHour = get_rollover_hour()
    int_newday = int(rolloverHour)
    
    new_day = datetime.time(int_newday, 0, 0)
    time_now = datetime.datetime.now().time()

    popup_date = datetime.date.today()
    if time_now < new_day:
        popup_date -= datetime.timedelta(days=1)

    today = popup_date.isoformat()
    return today


#MARK: check_today_popup
def check_today_popup(today):
    lo_config = get_local_config()
    achiev_last_popup = lo_config.get("achiev_last_popup")

    if achiev_last_popup == today:
        return False
    return True


#MARK: save_today_popup
def save_today_popup(today):
    lo_config = get_local_config()

    lo_config["achiev_last_popup"] = today
    save_local_config(lo_config)




#MARK: make_achievement_widget
achievement_widget = None
def make_achievement_widget(is_check_streak=False):
    global achievement_widget
    lo_config = None

    if is_check_streak:
        lo_config = get_local_config()
        achiev_streak_popup = lo_config.get("achiev_streak_popup", True)
        if not achiev_streak_popup:
            print(f"[{ADDON_NAME}] > not achiev_streak_popup") 
            return 

    if is_check_streak:
        today = get_today_popup_date()
        if not check_today_popup(today):
            print(f"[{ADDON_NAME}] > not check_today_popup") 
            return

    streak_count, username = get_streak_count()
    
    try:
        if not lo_config:
            lo_config = get_local_config()
        configured_user_name = lo_config.get("achiev_user_name")
        if isinstance(configured_user_name, str):
            username = configured_user_name
        else:
            username = None
        debug_streak_count = lo_config.get("debug_streak_count", None)
        debug_streak_username = lo_config.get("debug_streak_username", None)
        if isinstance(debug_streak_count, int):
            streak_count = debug_streak_count
        if isinstance(debug_streak_username, str):
            if debug_streak_username == "None":
                username = None
            else:
                username = debug_streak_username

    except Exception as e:
        print(f"[{ADDON_NAME}] Error: {e} ")

    if is_check_streak and not check_achievement(streak_count):
        print(f"[{ADDON_NAME}] > not check_achievement") 
        return

    if is_check_streak:
        if rate_limiter.limit("make_achievement_widget", 3600):
            return

        save_today_popup(today)

    achievement_widget = AchievementWidget(
        value=streak_count,
        user_name=username,
        parent=mw,)

    achievement_widget.show()
    achievement_widget.raise_()
    achievement_widget.activateWindow()