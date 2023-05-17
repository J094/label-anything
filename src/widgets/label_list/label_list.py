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
from src.widgets.label_list.ui_form import Ui_LabelList

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QListWidgetItem, QHBoxLayout, QCheckBox, QLabel,
)
from PySide6.QtGui import QColor, QPixmap, QPainter, QBrush, QPen


class LabelList(QWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.ui = Ui_LabelList()
        self.ui.setupUi(self)
        
    def add_item(self, labeled_object):
        r, g, b = self.main_window.color_map[labeled_object.label_name]
        item = QListWidgetItem()
        item.setSizeHint(QSize(200, 20))
        
        item_widget = QWidget()
        
        layout_h = QHBoxLayout()
        layout_h.setContentsMargins(9, 1, 9, 1)
        
        check_box = QCheckBox()
        check_box.setFixedWidth(20)
        check_box.setChecked(True)
        
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter()
        pen = QPen(QColor(r, g, b))
        brush = QBrush(QColor(r, g, b))
        painter.begin(pixmap)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(4, 4, 10, 10)
        painter.end()
        
        label_color = QLabel()
        label_color.setFixedWidth(20)
        label_color.setPixmap(pixmap)
        
        label_name = QLabel(labeled_object.label_name)

        layout_h.addWidget(check_box)
        layout_h.addWidget(label_color)
        layout_h.addWidget(label_name)
        
        item_widget.setLayout(layout_h)
        
        self.ui.listWidget_Labels.addItem(item)
        self.ui.listWidget_Labels.setItemWidget(item, item_widget)
        
    def update_list(self):
        self.ui.listWidget_Labels.clear()
        for labeled_object in self.main_window.labeled_objects:
            self.add_item(labeled_object)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = LabelList()
    widget.show()
    sys.exit(app.exec())
