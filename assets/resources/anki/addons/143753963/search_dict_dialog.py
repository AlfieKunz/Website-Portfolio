
from aqt import mw
from aqt.qt import QHBoxLayout, QSizePolicy, QDialog, QVBoxLayout, QPushButton, QLabel, QWidget
from aqt.utils import openLink

from .shige_config.searchable_combobox import SearchableComboBox
from .get_dict_file import LANGUAGE_DICT
from .const import DICT_DIR


#MARK: SearchDictWindow
class SearchDictDialog(QDialog):

    def __init__(self, parent:QWidget=mw, list_widget=None):
        super().__init__(parent)

        self.parent_widget = parent
        self.list_widget = list_widget

        self.dict_list = list(LANGUAGE_DICT.keys())

        self.setWindowTitle("Search Dictionary")
        self.setGeometry(100, 100, 300, 100)

        self.vbox_layout = QVBoxLayout()

        self.search_input = SearchableComboBox(self)
        self.vbox_layout.addWidget(self.search_input)

        self.result_label = QLabel(self)
        self.result_label.setText("Now loading...")
        self.vbox_layout.addWidget(self.result_label)

        hbox = QHBoxLayout()

        # Download
        self.search_button = QPushButton("Download", self)
        self.search_button.clicked.connect(self.start_download)
        self.search_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.search_button.setStyleSheet("QPushButton { padding: 2px; }")

        hbox.addWidget(self.search_button)

        # Close
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.reject)
        self.close_button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.close_button.setStyleSheet("QPushButton { padding: 2px; }")

        hbox.addStretch()
        hbox.addWidget(self.close_button)

        self.vbox_layout.addLayout(hbox)

        self.setLayout(self.vbox_layout)

        self.additems_languages()
        self.center()


    def center(self):
        if self.parent_widget:
            parent_rect = self.parent_widget.geometry()
            self_rect = self.geometry()
            x = parent_rect.x() + (parent_rect.width() - self_rect.width()) // 2
            y = parent_rect.y() + (parent_rect.height() - self_rect.height()) // 2
            self.move(x, y)

    def additems_languages(self):
        if self.dict_list:
            self.search_input.addItems(self.dict_list)
            self.result_label.setText("Please enter the language name.")
            self.search_input.setCurrentText("")
        else:
            self.result_label.setText("Hmmm, Dictionary not found :-/")
            self.search_input.setCurrentText("")

    def start_download(self):
        language_name = self.search_input.currentText()

        if self.dict_list:
            if language_name in self.dict_list:
                self.result_label.setText(f"Start downloading {language_name}...")
                from .get_dict_file import download_dictionary
                result = download_dictionary(language_name, DICT_DIR)
                print("result: ", result)
                if result:
                    self.result_label.setText(f"Download {language_name} finished! :-)")
                    from .dict_custom import refresh_dict_list
                    refresh_dict_list(self.list_widget)
                else:
                    self.result_label.setText(f"Download {language_name} failed :-/")

