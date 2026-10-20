import html
import json
import os
import shutil

from aqt import mw
from aqt.qt import (
    QAbstractItemView, QColor, QDialog, QFont, QHBoxLayout, QLabel,
    QPlainTextEdit, QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, Qt
)
from aqt.utils import tooltip

from .const import ADDON_PATH, DICT_DIR

MEDICAL_DIRECTORY_NAME = "medical_bdic"
MEDICAL_META_FILE_NAME = "dictionaries.json"
ENABLED_COLOR = QColor(0, 255, 0, 50)


#MARK: load_medical_dictionary_entries
def load_medical_dictionary_entries():
    medical_directory = os.path.join(ADDON_PATH, MEDICAL_DIRECTORY_NAME)
    meta_path = os.path.join(medical_directory, MEDICAL_META_FILE_NAME)
    if not os.path.isfile(meta_path):
        return []
    try:
        with open(meta_path, "r", encoding="utf-8") as meta_file:
            payload = json.load(meta_file)
    except Exception as error:
        print("Error reading medical dictionaries.json:", error)
        return []
    entries = payload.get("dictionaries", [])
    return entries


#MARK: MedicalDictDialog
class MedicalDictDialog(QDialog):

    def __init__(self, parent: QWidget = mw, list_widget=None):
        super().__init__(parent)

        self.parent_widget = parent
        self.list_widget = list_widget

        self.medical_directory = os.path.join(ADDON_PATH, MEDICAL_DIRECTORY_NAME)
        self.dictionaries = self.load_dictionary_entries()

        self.setWindowTitle("Medical Dictionaries")
        self.setGeometry(100, 100, 640, 400)

        self.name_table = QTableWidget(self)
        self.name_table.setColumnCount(1)
        self.name_table.setHorizontalHeaderLabels(["Dictionary"])
        self.name_table.horizontalHeader().setStretchLastSection(True)
        self.name_table.verticalHeader().setVisible(False)
        self.name_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.name_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.name_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.name_table.currentCellChanged.connect(self.on_selection_changed)

        self.detail_label = QLabel(self)
        self.detail_label.setWordWrap(True)
        self.detail_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.detail_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.enable_button = QPushButton("Enable", self)
        self.enable_button.clicked.connect(self.enable_selected_dictionary)
        self.enable_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.enable_button.setStyleSheet("QPushButton { padding: 2px; }")

        self.disable_button = QPushButton("Disable", self)
        self.disable_button.clicked.connect(self.disable_selected_dictionary)
        self.disable_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.disable_button.setStyleSheet("QPushButton { padding: 2px; }")

        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.reject)
        self.close_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.close_button.setStyleSheet("QPushButton { padding: 2px; }")

        self.license_button = QPushButton("License", self)
        self.license_button.clicked.connect(self.show_license)
        self.license_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.license_button.setStyleSheet("QPushButton { padding: 2px; }")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.enable_button)
        button_layout.addWidget(self.disable_button)
        button_layout.addWidget(self.license_button)
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.detail_label, 1)
        right_layout.addLayout(button_layout)

        right_widget = QWidget(self)
        right_widget.setLayout(right_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.name_table, 2)
        main_layout.addWidget(right_widget, 3)

        self.setLayout(main_layout)

        self.populate_table()
        self.center()


    #MARK: center
    def center(self):
        if self.parent_widget:
            parent_rect = self.parent_widget.geometry()
            self_rect = self.geometry()
            x = parent_rect.x() + (parent_rect.width() - self_rect.width()) // 2
            y = parent_rect.y() + (parent_rect.height() - self_rect.height()) // 2
            self.move(x, y)


    #MARK: load_dictionary_entries
    def load_dictionary_entries(self):
        entries = load_medical_dictionary_entries()
        return entries


    #MARK: populate_table
    def populate_table(self):
        dictionary_count = len(self.dictionaries)
        self.name_table.setRowCount(dictionary_count)
        for row_index in range(dictionary_count):
            entry = self.dictionaries[row_index]
            display_name = entry.get("name", "")
            if display_name == "":
                display_name = entry.get("file", "")
            item = QTableWidgetItem(display_name)
            self.name_table.setItem(row_index, 0, item)
            self.apply_row_color(row_index)
        if dictionary_count > 0:
            self.name_table.setCurrentCell(0, 0)
        else:
            self.detail_label.setText("No medical dictionaries found.")


    #MARK: get_dictionary_target_path
    def get_dictionary_target_path(self, entry):
        file_name = entry.get("file", "")
        target_path = os.path.join(DICT_DIR, file_name)
        return target_path


    #MARK: is_dictionary_enabled
    def is_dictionary_enabled(self, entry):
        target_path = self.get_dictionary_target_path(entry)
        return os.path.isfile(target_path)


    #MARK: apply_row_color
    def apply_row_color(self, row_index):
        entry = self.dictionaries[row_index]
        item = self.name_table.item(row_index, 0)
        if item is None:
            return
        if self.is_dictionary_enabled(entry):
            item.setBackground(ENABLED_COLOR)
        else:
            item.setData(Qt.ItemDataRole.BackgroundRole, None)


    #MARK: on_selection_changed
    def on_selection_changed(self, current_row, current_column, previous_row, previous_column):
        self.update_detail_view(current_row)


    #MARK: update_detail_view
    def update_detail_view(self, row_index):
        if row_index < 0 or row_index >= len(self.dictionaries):
            self.detail_label.setText("Please select a dictionary.")
            return
        entry = self.dictionaries[row_index]
        display_name = html.escape(str(entry.get("name", "")))
        file_name = html.escape(str(entry.get("file", "")))
        word_count = html.escape(str(entry.get("word_count", "")))
        version_value = entry.get("version")
        if version_value is None:
            version_text = "-"
        else:
            version_text = html.escape(str(version_value))
        last_updated = html.escape(str(entry.get("last_updated", "")))
        license_name = html.escape(str(entry.get("license", "")))
        summary_text = html.escape(str(entry.get("summary", "")))
        status_text = "Disabled"
        if self.is_dictionary_enabled(entry):
            status_text = "Enabled"
        detail_text = (
            f"<b>{display_name}</b><br><br>"
            f"{summary_text}<br><br>"
            f"Word count: {word_count}<br>"
            f"Last updated: {last_updated}<br>"
            f"File name: {file_name}<br>"
            f"Version: {version_text}<br>"
            f"License: {license_name}<br>"
            f"Status: {status_text}<br>"
            f"<br><br>"
            f"(This spell-checker add-on is not affiliated with these organizations. Words are extracted automatically so there is a risk that some spellings may contain errors.)"
        )
        self.detail_label.setText(detail_text)


    #MARK: enable_selected_dictionary
    def enable_selected_dictionary(self):
        row_index = self.name_table.currentRow()
        if row_index < 0 or row_index >= len(self.dictionaries):
            tooltip("No dictionary selected")
            return
        entry = self.dictionaries[row_index]
        file_name = entry.get("file", "")
        source_path = os.path.join(self.medical_directory, file_name)
        target_path = self.get_dictionary_target_path(entry)
        if not os.path.isfile(source_path):
            tooltip("Dictionary file not found in the add-on")
            return
        if os.path.isfile(target_path):
            tooltip(f"{entry.get('name', file_name)} is already enabled")
        else:
            try:
                os.makedirs(DICT_DIR, exist_ok=True)
                shutil.copy2(source_path, target_path)
            except Exception as error:
                print("Error enabling medical dictionary:", error)
                tooltip("Could not enable the dictionary (file in use?)")
                return
            tooltip(f"Enabled {entry.get('name', file_name)}")
        self.refresh_after_toggle(row_index)


    #MARK: disable_selected_dictionary
    def disable_selected_dictionary(self):
        row_index = self.name_table.currentRow()
        if row_index < 0 or row_index >= len(self.dictionaries):
            tooltip("No dictionary selected")
            return
        entry = self.dictionaries[row_index]
        target_path = self.get_dictionary_target_path(entry)
        if not os.path.isfile(target_path):
            tooltip(f"{entry.get('name', '')} is already disabled")
        else:
            try:
                os.remove(target_path)
            except Exception as error:
                print("Error disabling medical dictionary:", error)
                tooltip("Could not disable the dictionary (file in use?)")
                return
            tooltip(f"Disabled {entry.get('name', '')}")
        self.refresh_after_toggle(row_index)


    #MARK: refresh_after_toggle
    def refresh_after_toggle(self, row_index):
        self.apply_row_color(row_index)
        self.update_detail_view(row_index)
        if self.list_widget is not None:
            from .dict_custom import refresh_dict_list
            refresh_dict_list(self.list_widget)


    #MARK: show_license
    def show_license(self):
        row_index = self.name_table.currentRow()
        if row_index < 0 or row_index >= len(self.dictionaries):
            tooltip("No dictionary selected")
            return
        entry = self.dictionaries[row_index]
        license_file_name = entry.get("license_file", "")
        license_path = os.path.join(self.medical_directory, license_file_name)
        if not os.path.isfile(license_path):
            tooltip("License file not found")
            return
        try:
            with open(license_path, "r", encoding="utf-8", errors="replace") as license_file:
                license_text = license_file.read()
        except Exception as error:
            print("Error reading license file:", error)
            tooltip("Could not read the license file")
            return
        name = entry.get("name", "")
        self.license_window = LicenseDialog(self, name, license_text)
        self.license_window.show()


#MARK: LicenseDialog
class LicenseDialog(QDialog):

    def __init__(self, parent: QWidget, dictionary_name, license_text):
        super().__init__(parent)

        self.parent_widget = parent

        self.setWindowTitle(f"{dictionary_name} - License")
        self.setGeometry(100, 100, 660, 500)

        self.license_text_box = QPlainTextEdit(self)
        self.license_text_box.setPlainText(license_text)
        self.license_text_box.setReadOnly(True)
        self.license_text_box.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        fixed_font = QFont("monospace")
        fixed_font.setStyleHint(QFont.StyleHint.Monospace)
        self.license_text_box.setFont(fixed_font)

        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.reject)
        self.close_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.close_button.setStyleSheet("QPushButton { padding: 2px; }")

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.license_text_box, 1)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.center()


    #MARK: center
    def center(self):
        if self.parent_widget:
            parent_rect = self.parent_widget.geometry()
            self_rect = self.geometry()
            x = parent_rect.x() + (parent_rect.width() - self_rect.width()) // 2
            y = parent_rect.y() + (parent_rect.height() - self_rect.height()) // 2
            self.move(x, y)
