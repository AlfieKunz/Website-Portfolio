# Copyright (C) lovac42 2021 <https://github.com/lovac42> SpellingPolice <https://github.com/lovac42/SpellingPolice>
# Copyright (C) Valentin 2023 <https://github.com/ValentinSchmitz> Spell Checker <https://github.com/ValentinSchmitz/spell-checker>
# Copyright (C) Shigeyuki 2025 <http://patreon.com/Shigeyuki>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from aqt.qt import *

from .const import *
from .convert_manager import *
import os.path

from aqt.utils import openLink
from .shige_config.shige_addons import add_shige_addons_tab
from .shige_config.endroll.endroll import add_credit_tab
from .shige_config.button_manager import mini_button
from .shige_config.popup_config import RATE_THIS_URL, PATREON_URL, REPORT_URL
from .dict_custom import create_tab_list

from .path_manager import HUMAN_ADDON_NAME, ADDON_NAME

QCOLOR_ORANGE = QColor(255, 165, 0, 50)
QCOLOR_GREEN = QColor(0, 255, 0, 50)


QDIALOG_WIDTH = 634
QDIALOG_HIGHT = 422
# Width: 634, Height: 422


#MARK: DictionaryManager
class DictionaryManager:
    def __init__(self):
        pass
        # self.setupMenu()

    def setupMenu(self):

        qt_menu = QMenu(HUMAN_ADDON_NAME, mw)

        qt_action_01 = QAction("⚙️Options", mw)
        qt_action_01.triggered.connect(self.showConfig)

        qt_menu.addAction(qt_action_01)

        mw.form.menuTools.addMenu(qt_menu)

        try:
            from .achievement_v2 import entry_point
            entry_point(qt_menu)
        except Exception as e:
            print(f"[{ADDON_NAME}] Error: {e} ")

        try:
            from .shige_config.add_menu_actions import add_menu
            add_menu(qt_menu)

        except Exception as e:
            print(f"[{ADDON_NAME}] Error: {e} ")


    def showConfig(self):
        DictionaryDialog()
        refresh_languages()

#MARK: DictionaryDialog
class DictionaryDialog(QDialog):

    list = None

    def __init__(self, parent=mw):
        QDialog.__init__(self, parent)

        default_enabled = {}
        downloaded = {}
        for language_key in LANGUAGE_LIST:
            default_enabled[language_key] = False
            downloaded[language_key] = False

        self._enabled = get_user_data("enabled", default=default_enabled)
        self._downloaded = downloaded

        self._setup_dialog()
        self._update()
        self.exec()


    #MARK:resizeEvent
    def resizeEvent(self, event:"QResizeEvent"):
        size = event.size()
        print(f"Width: {size.width()}, Height: {size.height()}")
        super().resizeEvent(event)


    #MARK: _setup_dialog
    def _setup_dialog(self):
        self.setWindowTitle(HUMAN_ADDON_NAME)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        # self.resize(450, 350)
        self.resize(QDIALOG_WIDTH, QDIALOG_HIGHT)
        icon = os.path.join(ADDON_PATH, "icon.svg")
        self.setWindowIcon(QIcon(icon))

        layout = QHBoxLayout()
        self.list = QListWidget()
        self.list.setAlternatingRowColors(True)
        self.list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.list.itemDoubleClicked.connect(self._toggle)

        en_btn = QPushButton('Enable')
        en_btn.clicked.connect(self._enable)
        dis_btn = QPushButton('Disable')
        dis_btn.clicked.connect(self._disable)

        l1 = QLabel("Enabled")
        l1.setStyleSheet(f"background-color:rgba{QCOLOR_GREEN.getRgb()}")
        l2 = QLabel("Missing/downloading")
        l2.setStyleSheet(f"background-color:rgba{QCOLOR_ORANGE.getRgb()}")
        l3 = QLabel("Disabled")

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)

        comp_btn = QPushButton("Compile your\ndictionaries")
        comp_btn.clicked.connect(compile_user_dicts)

        open_pdics_btn = QPushButton("Open personal\ndictionary folder")
        open_pdics_btn.clicked.connect((partial(open_path, USER_DICT_PATH)))

        open_dics_btn = QPushButton("Open .bdic folder")
        open_dics_btn.clicked.connect((partial(open_path, DICT_DIR)))

        control_box = QVBoxLayout()
        control_box.alignment()
        control_box.addWidget(en_btn)
        control_box.addWidget(dis_btn)
        control_box.addWidget(l1)
        control_box.addWidget(l2)
        control_box.addWidget(l3)
        control_box.addWidget(line)
        control_box.addWidget(comp_btn)
        control_box.addWidget(open_pdics_btn)
        control_box.addWidget(open_dics_btn)

        conversion_label = QLabel("[ Compile mode ]")
        conversion_combo = QComboBox()
        conversion_combo.addItem("wasm-mode", "wasm")
        conversion_combo.addItem("binary-mode", "legacy")
        current_mode_index = conversion_combo.findData(get_conversion_mode())
        if current_mode_index != -1:
            conversion_combo.setCurrentIndex(current_mode_index)
        conversion_combo.currentIndexChanged.connect(self._on_conversion_mode_changed)
        self._conversion_combo = conversion_combo
        control_box.addWidget(conversion_label)
        control_box.addWidget(conversion_combo)

        tabWidget = QTabWidget()
        
        # tab_01 = QWidget()
        tab_01 = create_tab_list(self)
        
        tab_02 = QWidget()
        tab1Layout = QHBoxLayout(tab_02)
        tab1Layout.addWidget(self.list)
        tab1Layout.addLayout(control_box)

        tabWidget.addTab(tab_01, "Dict")
        tabWidget.addTab(tab_02, "Advanced")

        add_shige_addons_tab(self, tabWidget)
        add_credit_tab(self, tabWidget)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)

        ### ShigeButtons ###
        custom_buttons = QHBoxLayout()
        rate_btn = QPushButton("👍️RateThis")
        mini_button(rate_btn)
        rate_btn.clicked.connect(lambda: openLink(RATE_THIS_URL))
        patreon_btn = QPushButton("💖Become a Patron")
        mini_button(patreon_btn)
        patreon_btn.clicked.connect(lambda: openLink(PATREON_URL))
        report_btn = QPushButton("🚨Report")
        mini_button(report_btn)
        report_btn.clicked.connect(lambda: openLink(REPORT_URL))

        Wiki_btn = QPushButton("📖How to use")
        mini_button(Wiki_btn)
        Wiki_btn.clicked.connect(lambda: openLink(
            "https://shigeyukey.github.io/shige-addons-wiki/anki-spell-checker.html"))


        # close
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        custom_buttons.addWidget(close_btn)

        custom_buttons.addStretch()
        custom_buttons.addWidget(Wiki_btn)
        custom_buttons.addWidget(rate_btn)
        custom_buttons.addWidget(patreon_btn)
        custom_buttons.addWidget(report_btn)
        mainLayout.addLayout(custom_buttons)
        ######

        self.setLayout(mainLayout)

        # layout.addWidget(self.list)
        # layout.addLayout(control_box)
        # self.setLayout(layout)

    def _update(self, *args):
        self.list.clear()

        download = []
        dic_files = get_dictionaries()
        for key, value in self._enabled.items():
            if key not in dic_files and value:
                download.append(key)
            if key in dic_files and value:
                dic_files.remove(key)
                self._downloaded[key] = True
            if not value:
                self._downloaded[key] = False
        if download:
            self._manageDownloads(download)

        for dic in dic_files:
            if dic == "personal":
                continue
            item = QListWidgetItem(f"Custom: {dic}.bdic")
            item.setBackground(QCOLOR_GREEN)
            item.setData(Qt.ItemDataRole.WhatsThisRole, "custom")
            item.setData(Qt.ItemDataRole.UserRole, dic)
            self.list.addItem(item)

        for key, language in LANGUAGE_LIST.items():
            name = language[0]
            item = QListWidgetItem(name)
            if self._enabled[key]:
                item.setBackground(QCOLOR_ORANGE)
            if self._downloaded[key]:
                item.setBackground(QCOLOR_GREEN)
            item.setData(Qt.ItemDataRole.UserRole, key)
            self.list.addItem(item)

    def _downloadItemUpdate(self):
        li = self.list
        dl = get_dictionaries()
        for i in range(li.count()):
            key = li.item(i).data(Qt.ItemDataRole.UserRole)
            if key in dl:
                li.item(i).setBackground(QCOLOR_GREEN)

    @background_op()
    def _manageDownloads(self, keys, *args):
        for key in keys:
            file_path = os.path.join(DICT_DIR, key + ".bdic.disabled")
            if os.path.isfile(file_path):
                os.rename(file_path, file_path.removesuffix(".disabled"))
            else:
                self._download(key)
        self._downloadItemUpdate()
        return keys


    #MARK: _download
    def _download(self, key):

        language_data = LANGUAGE_LIST[key]
        dict_source = language_data[1]
        dict_url = URL_DICTIONARIES(dict_source)
        download_response = on_download(dict_url)
        list_raw = download_response.json()

        targets = ["index.aff", "index.dic"]

        downloads = []
        for item in list_raw:
            item_name = item["name"]
            is_target = False
            for target in targets:
                if target in item_name:
                    is_target = True
                    break
            if is_target:
                downloads.append(item["download_url"])

        temp_files = []
        temp_dict = os.path.join(DICT_DIR, "tmp")
        for download_url in downloads:
            download_url:str
            url_parts = download_url.split(".")
            file_extension = url_parts[-1]
            file_name_parts = (key, file_extension)
            file_name = ".".join(file_name_parts)
            save_path = download_to_file(download_url, temp_dict, file_name)
            temp_files.append(save_path)

        compile_BDIC(temp_dict, key, remove=True)

    def _enable(self):
        sel = [i for i in range(self.list.count()) if self.list.item(i).isSelected()]
        if sel:
            for i in sel:
                fn = self.list.item(i).data(Qt.ItemDataRole.UserRole)
                cu = self.list.item(i).data(Qt.ItemDataRole.WhatsThisRole)
                if cu:
                    continue
                if fn is not None:
                    self._enabled[fn] = True
        set_user_data("enabled", self._enabled)
        self._update()

    def _disable(self):
        sel = [i for i in range(self.list.count())
                if self.list.item(i).isSelected()]
        if sel:
            for i in sel:
                fn = self.list.item(i).data(Qt.ItemDataRole.UserRole)
                cu = self.list.item(i).data(Qt.ItemDataRole.WhatsThisRole)
                file_path = os.path.join(DICT_DIR, fn + ".bdic")
                if cu:
                    os.remove(file_path)
                if fn is not None:
                    self._enabled[fn] = False
                    if os.path.isfile(file_path):
                        os.rename(file_path, file_path + ".disabled")
        set_user_data("enabled", self._enabled)
        self._update()

    def _toggle(self):
        fn = self.list.currentItem().data(Qt.ItemDataRole.UserRole)
        if fn is not None:
            self._enabled[fn] = not self._enabled[fn]
        set_user_data("enabled", self._enabled)
        self._update()

    #MARK: _on_conversion_mode_changed
    def _on_conversion_mode_changed(self, index):
        conversion_mode = self._conversion_combo.itemData(index)
        if conversion_mode is None:
            return
        set_conversion_mode(conversion_mode)
        print(f"SpellChecker: conversion mode: {conversion_mode}")
        if conversion_mode == "legacy":
            if not conversion_binaries_installed():
                tooltip("Spell Checker: downloading the convert_dict binaries...")
            download_conversion_binaries()
