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
#
import sys
from PyQt5.QtWidgets import QApplication
from view import *


class Window(View):

    def __init__(self):
        super().__init__()
        self.app = app

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
