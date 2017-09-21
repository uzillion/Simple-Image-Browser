"""
File: image-browser.py
By: Uzair Inamdar
Last edited: 9/16/2017

This is a simple image browser that has thumbnail mode and fill window mode
Operational Keys are:
'>' for viewing next 5 pictures
'<' for viewing previous 5 pictures
[Up arrow key] for viewing in fill window mode
[Down arrow key] for viewing in thumbnail mode
[Left and right arrow keys] for viewing traveling between pictures
[Click] on picture to expand in fill window mode

"""

import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from controller import *
from images import *
from view import *


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.view = View()
        self.images = Images().images
        self.events = Controller()
        self.views = View()
        self.app = app
        self.title = 'Image Browser'
        self.views.initUI()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
