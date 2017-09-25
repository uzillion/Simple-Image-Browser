"""
File: click_filter.py
By: Uzair Inamdar
Last edited: 9/25/2017

This file is responsible for handling mouse clicks on various items
"""

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QObject, pyqtSignal, QEvent

def clickable(widget):      # Making QLabels clickable
    class Filter(QObject):      # Filtering through only QObjects
        clicked = pyqtSignal([QLabel])      # Creating signal object and including QLabel object in it
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonPress:
                    if obj.rect().contains(event.pos()):    # If position of click is in the QObjects area
                        self.clicked.emit(obj)      # Emit Signal
                        return True   # Clicked object recognizable
            return False       # Clicked Object blocked by filter
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked
