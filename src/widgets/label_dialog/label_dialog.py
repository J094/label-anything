# -*- coding: utf-8 -*-
# J094
# 2023.05.17
import os
import sys
sys.path.append(os.path.realpath("."))

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from src.widgets.label_dialog.ui_form import Ui_LabelDialog

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QListWidgetItem, QHBoxLayout, QCheckBox, QLabel, 
    QDialog,
)
from PySide6.QtGui import QColor, QPixmap, QPainter, QBrush, QPen


class LabelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LabelDialog()
        self.ui.setupUi(self)
        
        self.ui.pushButton_OK.clicked.connect(self.slot_ok)
        self.ui.pushButton_Cancel.clicked.connect(self.slot_cancel)
        
    def add_item(self, label_name):
        r, g, b = self.parent().color_map[label_name]
        item = QListWidgetItem()
        item.setSizeHint(QSize(200, 20))
        
        item_widget = QWidget()
        
        layout_h = QHBoxLayout()
        layout_h.setContentsMargins(9, 1, 9, 1)
        
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
        
        label_label_name = QLabel(label_name)
        
        label_label_color = QLabel()
        label_label_color.setFixedWidth(20)
        label_label_color.setPixmap(pixmap)

        layout_h.addWidget(label_label_name)
        layout_h.addWidget(label_label_color)
        
        item_widget.setLayout(layout_h)
        
        self.ui.listWidget_Label_Name.addItem(item)
        self.ui.listWidget_Label_Name.setItemWidget(item, item_widget)
        
    def update_list(self):
        self.ui.listWidget_Label_Name.clear()
        # parent() returns MainWindow
        for label_name in self.parent().label_names:
            self.add_item(label_name)
    
    def clear_text(self):
        self.ui.lineEdit_Label_Name.clear()
        self.ui.lineEdit_Group_ID.clear()
        
    def slot_ok(self):
        self.accept()
    
    def slot_cancel(self):
        self.clear_text()
        self.reject()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = LabelDialog()
    widget.show()
    sys.exit(app.exec())
