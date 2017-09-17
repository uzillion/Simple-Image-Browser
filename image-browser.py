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
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import *

def clickable(widget):      # Making QLabels clickable
    class Filter(QObject):      # Filtering through only QObjects
        clicked = pyqtSignal([QLabel])      # Creating signal object and including QLabel object in it
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonPress:
                    if obj.rect().contains(event.pos()):    # If position of click is in the QObjects area
                        self.clicked.emit(obj)      # Emit Signal
                        return True   # Clicked object recognizable
            return False       # Clicked Object bloacked by filter
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.image_index = 0        # Keeps track of the first image in image list to be displayed in the thumbnail bar
        self.mode = 0         # Determines and Tracks current mode of view (1 - Full Screen, 0 - Thumbnail)
        self.selected_index = 0     # Keeps track of the current selected index in the thumbnail bar
        self.app = app
        self.title = 'Image Browser'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setStyleSheet("background-color: #324d7a")
        self.move(250, 250)
        self.setFixedSize(800, 600)
        self.layout = QHBoxLayout(self)     # Creates a Horizontal Layout
        self.layout.setContentsMargins(20, 0, 20, 0)    # Removes margins around stored object in the layout
        self.layout.setSpacing(0)           # Removes spaces between layout objects
        self.images = []
        for file_ in os.listdir("./data"):
            if file_.endswith((".jpg", ".jpeg", ".png")):
                self.images.append(file_)       # Loading images from ./data folder
        self.thumbnail_bar()
        self.select(0)        # Selects first image-box in layout
        self.show()

    '''
    AFTER THIS POINT FUNCTIONS ARE PLACED IN ALPHABETICAL ORDER FOR EASE OF SEARCHING
    '''

    def circularTraverse(self, steps, direction):    # Responsible for Circular Traversing the image list in the given direction
        if direction == "left":
            return (self.image_index-steps)%(len(self.images))
        else:
            return (self.image_index+steps)%(len(self.images))

    def enlarge(self, index):    # Makes necessary changes to change to Full Screen (Window Fill) Mode
        self.mode = 1
        self.selected_index = index
        pixContainer = self.getWidget(index).pixmap()
        for i in range(0, self.size):
            self.getWidget(i).hide()
        self.getWidget(self.size).show()    # Shows label that displays in full screen
        self.getWidget(self.size).setPixmap(pixContainer.scaled(760, 560, Qt.KeepAspectRatio))   # Sets image in selected label to full screen label
        self.layout.setContentsMargins(0, 0, 0, 500)    # Pushes image to the top of the window

    def getWidget(self, index):     # Gets stored widget from layout in the passed index
        return self.layout.itemAt(index).widget()

    def keyPressEvent(self, e):     # Handles all key press events
        if e.key() == Qt.Key_Right:
            self.shiftRight()

        if e.key() == Qt.Key_Left:
            self.shiftLeft()

        elif e.key() == Qt.Key_Period and self.mode == 0 and self.size == 5:    # Moves to the next 5 images only if there are enough images to overflow
            self.image_index=self.circularTraverse(self.size, "right")
            for i in range(0,5):
                self.getWidget(i).setPixmap(QPixmap("data/"+self.images[self.circularTraverse(i, "right")]).scaled(132, 132, Qt.KeepAspectRatio))
            self.select(0)

        elif e.key() == Qt.Key_Comma and self.mode == 0 and self.size == 5:     # Moves to the previous 5 images only if there are enough images to overflow
            self.image_index=self.circularTraverse(self.size, "left")
            for i in range(0,5):
                self.getWidget(i).setPixmap(QPixmap("data/"+self.images[self.circularTraverse(i, "right")]).scaled(132, 132, Qt.KeepAspectRatio))
            self.select(0)

        elif e.key() == Qt.Key_Up and self.mode == 0:
            self.enlarge(self.selected_index)

        elif e.key() == Qt.Key_Down and self.mode == 1:
            self.shrink(self.selected_index)
            if self.size == 5:      # Checks if there are more than 5 images
                center_distance = self.selected_index - 2      # Calculates the distance of the seleted image from the center box
                if center_distance > 0:     # Checks if the selected image is right of center
                    # Shifts thumbnail bar accordingly to place selected image in middle on coming back to thumbnai bar mode:
                    for i in range(0, center_distance):
                        for j in range(0,4):
                            self.getWidget(j).setPixmap(self.getWidget(j+1).pixmap().scaled(132, 132, Qt.KeepAspectRatio))
                        self.getWidget(self.size-1).setPixmap(QPixmap("data/"+self.images[self.circularTraverse(self.size, "right")]).scaled(132, 132, Qt.KeepAspectRatio))
                        self.image_index = self.circularTraverse(1, "right")
                elif center_distance < 0:      # Checks if selected image is left of center
                    # Shifts thumbnail bar accordingly to place selected image in middle on coming back to thumbnai bar mode:
                    for i in range(0, abs(center_distance)):
                        for j in range(4, 0, -1):
                            self.getWidget(j).setPixmap(self.getWidget(j-1).pixmap().scaled(132, 132, Qt.KeepAspectRatio))
                        self.getWidget(0).setPixmap(QPixmap("data/"+self.images[self.circularTraverse(1, "left")]).scaled(132, 132, Qt.KeepAspectRatio))
                        self.image_index = self.circularTraverse(1, "left")
                self.select(2)

    def indexOfLabel(self, label):      # Provides the index of the clicked label for further operations
        if self.mode == 0:
            self.select(self.layout.indexOf(label))
            self.enlarge(self.layout.indexOf(label))

    def select(self, selected_index):   # Selects new item
        self.getWidget(self.selected_index).setStyleSheet("border: 10px solid red")   # Changes old image box to not selected border
        self.getWidget(selected_index).setStyleSheet("border: 10px solid green")    # Changes new image box to selected border
        self.selected_index = selected_index      # Updates Current selection index

    def shiftLeft(self):            # Shifts the select box and scope of the Thumbnail Bar to the left
        if self.selected_index != 0:         # Shift select box till first image
            if self.mode == 1:
                pixContainer = self.getWidget(self.selected_index-1).pixmap()
                self.getWidget(self.size).setPixmap(pixContainer.scaled(760, 560, Qt.KeepAspectRatio))
            self.select(self.selected_index-1)
        else:
            if self.size == 5:       # If there are more than 5 images, shift scope of Thumbnail Bar to left
                for i in range(self.size-1, 0, -1):     # Shifts scope
                    self.getWidget(i).setPixmap(self.getWidget(i-1).pixmap().scaled(132, 132, Qt.KeepAspectRatio))
                self.getWidget(0).setPixmap(QPixmap("data/"+self.images[self.circularTraverse(1, "left")]).scaled(132, 132, Qt.KeepAspectRatio))
                if self.mode == 1:     # If in full screen mode, load previous image
                    self.getWidget(self.size).setPixmap(self.getWidget(0).pixmap().scaled(760, 560, Qt.KeepAspectRatio))
                self.image_index = self.circularTraverse(1, "left")

    def shiftRight(self):       # Shifts the select box and scope of the Thumbnail Bar to the right
        if self.selected_index != self.size-1:      # Shift select box till last image
            if self.mode == 1:
                pixContainer = self.getWidget(self.selected_index+1).pixmap()
                self.getWidget(self.size).setPixmap(pixContainer.scaled(760, 560, Qt.KeepAspectRatio))
            self.select(self.selected_index+1)
        else:
            if self.size == 5:      # If there are more than 5 images, shift scope of Thumbnail Bar to rght
                for i in range(0, self.size-1):    # Shifts scope
                    self.getWidget(i).setPixmap(self.getWidget(i+1).pixmap().scaled(132, 132, Qt.KeepAspectRatio))
                self.getWidget(self.size-1).setPixmap(QPixmap("data/"+self.images[self.circularTraverse(self.size, "right")]).scaled(132, 132, Qt.KeepAspectRatio))
                if self.mode == 1:    # If in full screen mode, load next image
                    self.getWidget(self.size).setPixmap(self.getWidget(self.size-1).pixmap().scaled(760, 560, Qt.KeepAspectRatio))
                self.image_index = self.circularTraverse(1, "right")

    def shrink(self, index):     # Makes necessary changes to change back to Thumbnail Mode
        self.mode = 0       # Upadates mode variable
        self.getWidget(self.size).hide()    # Hides full screen label
        for i in range(0,self.size):    # Un-hides thumbnail labels
            self.getWidget(i).show()
        self.layout.setContentsMargins(20, 0, 20, 0)

    def thumbnail_bar(self):     # Creates a List of QLabels and places them in a horizontal Layout
        labels = []
        self.size = 5
        if len(self.images) < 5:       # If there are less than 5 images
            self.size = len(self.images)
        for i in range(0, self.size+1):
            labels.insert(i, QLabel(self))
            if i != (self.size):
                labels[i].setPixmap(QPixmap("data/"+self.images[i]).scaled(132, 132, Qt.KeepAspectRatio))      # Sets images to each label in layout
                labels[i].setMaximumSize(152,152)
            labels[i].setAlignment(Qt.AlignCenter)      # Align images to the center of the label
            labels[i].setStyleSheet('border: 10px solid red')
            self.layout.addWidget(labels[i])        # Add label into layout container
            clickable(self.getWidget(i)).connect(self.indexOfLabel)     # Connects the click even to the indexOfLabel function

        # Properties of full screen view label:
        self.getWidget(self.size).setStyleSheet('border: 20px solid red')
        self.getWidget(self.size).setMinimumSize(800, 600)
        self.getWidget(self.size).hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
