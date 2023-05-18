# -*- coding: utf-8 -*-
# J094
# 2023.05.10
import os
import sys
sys.path.append(os.path.realpath("."))

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from src.widgets.file_list.ui_form import Ui_FileList

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QApplication, QWidget, QListWidgetItem


class FileList(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.ui = Ui_FileList()
        self.ui.setupUi(self)
        
        self.ui.listWidget_Files.clicked.connect(self.slot_clicked)
        
    def update_list(self):
        self.ui.listWidget_Files.clear()
        for (i, image_path) in enumerate(self.main_window.image_paths):
            _, image_name = os.path.split(image_path)
            item = QListWidgetItem()
            if os.path.exists(self.main_window.output_paths[i]):
                item.setCheckState(Qt.CheckState.Checked)
            else:    
                item.setCheckState(Qt.CheckState.Unchecked)
            item.setSizeHint(QSize(200, 20))
            item.setText(image_name)
            self.ui.listWidget_Files.addItem(item)
        self.ui.label_Total.setText('{}'.format(len(self.main_window.image_paths)))
    
    def slot_clicked(self):
        index = self.ui.listWidget_Files.currentRow()
        self.main_window.image_path = self.main_window.image_paths[index]
        self.main_window.load_file()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = FileList()
    widget.show()
    sys.exit(app.exec())
