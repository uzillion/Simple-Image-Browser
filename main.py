"""
File: main.py
By: Uzair Inamdar
Last edited: 10/16/2017

This is a simple image browser that has thumbnail mode and fill window mode
Operational Keys are:
'>' for viewing next 5 pictures
'<' for viewing previous 5 pictures
[Up arrow key] for viewing in fill window mode
[Down arrow key] for viewing in thumbnail mode
[Left and right arrow keys] for viewing traveling between pictures
'Escape' or click on picture to return control back to browser
[Click] on picture in thumbnail mode to expand to fill window mode

"""

import sys
from PyQt5.QtWidgets import QApplication
from view import *


class Window(View):

    def __init__(self):
        if len(sys.argv) != 2:      # If width is not specified
            super().__init__(800)      # Sending width of window
            print("You can also specify width of Window in this format:")
            print("-> main.py [Width]")
        else:
            super().__init__(sys.argv[1])      # Sending width of window
            if int(sys.argv[1]) not in range(600, 1201):    # If width is not in range
                print("Only width between 600 to 1200 pixels allowed")
                sys.exit(0)
        self.app = app

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
