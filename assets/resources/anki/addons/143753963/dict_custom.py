import os
from aqt import mw
from aqt.utils import tooltip, askUser, openFolder

from .shige_config.button_manager import mini_button
from aqt.qt import (
QWidget, QVBoxLayout, QTabWidget, QListWidget, QListWidgetItem, Qt,
QAbstractItemView, QHBoxLayout, QPushButton, QLabel
)

from .search_dict_dialog import SearchDictDialog
from .medical_dict_dialog import MedicalDictDialog, load_medical_dictionary_entries
from .get_dict_file import LANGUAGE_DICT
from .const import DICT_DIR

PERSONAL_BDIC_FILE_NAME = "personal.bdic"
PERSONAL_BDIC_DISPLAY_NAME = "Your Personal Dictionary"


#MARK: get_medical_dictionary_name_map
def get_medical_dictionary_name_map():
    name_map = {}
    entries = load_medical_dictionary_entries()
    for entry in entries:
        file_name = entry.get("file", "")
        display_name = entry.get("name", "")
        if file_name == "" or display_name == "":
            continue
        name_map[file_name] = display_name
    return name_map


#MARK: get_dictionaries_v2
def get_dictionaries_v2():
    dicts = []
    medical_name_map = get_medical_dictionary_name_map()
    for file in os.listdir(DICT_DIR):
        if file.endswith(".bdic"):
            if file == PERSONAL_BDIC_FILE_NAME:
                dicts.append(PERSONAL_BDIC_DISPLAY_NAME)
                continue
            found = False
            for lang_name, dict_file in LANGUAGE_DICT.items():
                if dict_file == file:
                    dicts.append(lang_name)
                    found = True
                    break
            if not found:
                if file in medical_name_map:
                    dicts.append(medical_name_map[file])
                else:
                    dicts.append(file)
    return dicts


#MARK: refresh_dict_list
def refresh_dict_list(list_widget: QListWidget):
    list_widget.clear()
    dict_list = get_dictionaries_v2()
    if dict_list:
        for language_name in dict_list:
            item = QListWidgetItem(language_name)
            list_widget.addItem(item)

#MARK: create_tab_list
def create_tab_list(parent):
    # dict_list = list(LANGUAGE_DICT.keys())
    dict_list = get_dictionaries_v2()

    list_widget = QListWidget()
    list_widget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    if dict_list:
        for language_name in dict_list:
            item = QListWidgetItem(language_name)
            list_widget.addItem(item)

    tab = QWidget(parent)
    layout = QVBoxLayout()
    add_button = QPushButton(" 🔍️Add New Dict (Languages) ")
    mini_button(add_button)
    add_button.clicked.connect(lambda: add_new_dict(parent, list_widget))


    add_med_dict_button = QPushButton(" 🔍️Add New Dict (Medical) ")
    mini_button(add_med_dict_button)
    add_med_dict_button.clicked.connect(lambda: add_new_med_dict(parent, list_widget))


    delete_button = QPushButton("🗑️Delete")
    mini_button(delete_button)
    delete_button.clicked.connect(lambda:disable_dict(list_widget))

    userFilesButton = QPushButton("📂Dict Files")
    mini_button(userFilesButton)
    userFilesButton.clicked.connect(lambda: openFolder(DICT_DIR))

    layout_b = QHBoxLayout()
    layout_b.addWidget(add_button)
    layout_b.addWidget(add_med_dict_button)
    layout_b.addWidget(delete_button)
    layout_b.addWidget(userFilesButton)

    layout_b.addStretch()
    layout.addLayout(layout_b)

    layout.addWidget(list_widget)
    tab.setLayout(layout)

    return tab


#MARK: add_new_dict 
def add_new_dict(parent, list_widget):
    print("enable_dict")
    mw.serch_dict_window = SearchDictDialog(parent, list_widget)
    mw.serch_dict_window.show()


#MARK: add_new_med_dict
def add_new_med_dict(parent, list_widget):
    mw.medical_dict_window = MedicalDictDialog(parent, list_widget)
    mw.medical_dict_window.show()


#MARK: disable_dict
def disable_dict(list_widget:QListWidget):
    selected_items = list_widget.selectedItems()
    if not selected_items:
        tooltip("No dictionary selected")
        return

    selected_dict_names = [item.text() for item in selected_items]

    if not askUser(f"delete selected dictionaries ({', '.join(selected_dict_names)})?"):
        return

    medical_name_map = get_medical_dictionary_name_map()
    display_file_map = {}
    for file_name, display_name in medical_name_map.items():
        display_file_map[display_name] = file_name
    display_file_map[PERSONAL_BDIC_DISPLAY_NAME] = PERSONAL_BDIC_FILE_NAME

    deleted_count = 0
    for item in selected_items:
        dict_name = item.text()
        dict_file = None
        if dict_name in LANGUAGE_DICT:
            dict_file = LANGUAGE_DICT[dict_name]
        elif dict_name in display_file_map:
            dict_file = display_file_map[dict_name]
        else:
            dict_file = dict_name

        file_path = os.path.join(DICT_DIR, dict_file)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                deleted_count += 1
            else:
                tooltip(f"File not found: {file_path}")
        except Exception as e:
            print("Error deleting file:", e)
            tooltip(f"Deletion error")

    if deleted_count > 0:
        for item in selected_items[::-1]:
            list_widget.takeItem(list_widget.row(item))

        tooltip(f"{deleted_count} deleted successfully")
