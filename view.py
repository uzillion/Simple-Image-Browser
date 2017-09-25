"""
File: view.py
By: Uzair Inamdar
Last edited: 9/25/2017

This file is responsible for handling the layout and events of the program
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QApplication
from PyQt5.QtGui import QPixmap
from models import *
from PyQt5.QtCore import *
from click_filter import *
import json
class View(QWidget):

    def __init__(self, W):
        self.W = int(W)
        super().__init__()
        self.sounds = Models(self)
        self.sounds.initSound()
        self.image_index = 0        # Keeps track of the first image in image list to be displayed in the thumbnail bar
        self.mode = 0         # Determines and Tracks current mode of view (1 - Full Screen, 0 - Thumbnail)
        self.selected_index = 0     # Keeps track of the current selected index in the thumbnail bar
        self.loadTags()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Browser")
        self.setStyleSheet("background-color: #324d7a")
        self.H = (self.W/4)*3
        self.move(250, 250)
        self.setFixedSize(self.W, self.H)

        # Setting-up Layout for images
        self.layout = QHBoxLayout(self)     # Creates a Horizontal Layout
        self.layout.setContentsMargins(20, 0, 20, 0)    # Removes margins around stored object in the layout
        self.layout.setSpacing(0)           # Removes spaces between layout objects
        self.layout.setAlignment(Qt.AlignCenter)    # Pushes image to the top of the window

        # Setting-up text box for adding tags
        self.textBox = QLineEdit(self)
        self.textBox.setStyleSheet("QLineEdit{ background: #f8f8f8; selection-background-color: #f8f8f8; }")
        self.textBox.setPlaceholderText("Enter your tags here")
        self.textBox.resize(self.W/2,self.H/10)
        self.textBox.move(20, self.H*(5/6))

        # Setting-up add and save buttons for tags
        self.addButton = QPushButton('Add Tag', self)
        self.addButton.setStyleSheet("background-color: #F5F5F5")
        self.addButton.move(self.W/1.9,self.H*(5/6))
        self.addButton.resize(self.W/6, self.H/10)
        self.addButton.clicked.connect(self.addTag)

        self.saveButton = QPushButton('Save Tags', self)
        self.saveButton.setStyleSheet("background-color: #F5F5F5")
        self.saveButton.move(self.W/1.42,self.H*(5/6))
        self.saveButton.resize(self.W/6, self.H/10)
        self.saveButton.clicked.connect(self.saveTags)

        # Setting up layout for holding tags
        self.tagList = QVBoxLayout()
        self.tagList.setSpacing(10)
        self.tagList.setContentsMargins(40, 0, 5, 0)

        self.textBox.hide()
        self.addButton.hide()
        self.saveButton.hide()

        self.thumbnail_bar()
        self.select(0) # Selects first image-box in layou
        self.show()

    def thumbnail_bar(self):     # Creates a List of QLabels and places them in a horizontal Layout
        labels = []
        for i in range(0, 6):
            labels.insert(i, QLabel(self))
            if i != (5):
                labels[i].setPixmap(QPixmap("data/"+Models.images[i]).scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio))      # Sets images to each label in layout
                labels[i].setFixedSize((self.W-40)/5, (self.W-40)/5)
            labels[i].setAlignment(Qt.AlignCenter)      # Align images to the center of the label
            labels[i].setStyleSheet('border: 10px solid red')
            self.layout.addWidget(labels[i])        # Add label into layout container
            clickable(self.getWidget(i)).connect(self.indexOfLabel)     # Connects the click even to the indexOfLabel function

        # Properties of full screen view label:
        self.getWidget(5).setStyleSheet('border: 20px solid red')
        self.getWidget(5).setFixedSize(self.W/1.33, self.H/1.28)
        self.getWidget(5).hide()

    def drawTags(self):
        image_key = str((self.image_index+self.selected_index)%len(Models.images))
        if image_key in self.tags:
            for i in range(0, len(self.getTags())):
                self.getTags().itemAt(0).widget().setParent(None)
            for tag in self.tags[image_key]:
                self.getTags().addWidget(QPushButton(tag, self))
                self.getTags().itemAt(len(self.getTags())-1).widget().setStyleSheet("background-color: #f5f5f5")
        else:
            for i in range(0, len(self.getTags())):
                item = self.getTags().itemAt(0).widget().setParent(None)


    def enlarge(self, index):    # Makes necessary changes to change to Full Screen (Window Fill) Mode
        self.sounds.expand_sound.play()
        self.layout.addLayout(self.tagList)     # Adding TagList layout to main layout
        self.mode = 1
        self.selected_index = index
        pixContainer = self.getWidget(index).pixmap()
        for i in range(0, 5):
            self.getWidget(i).hide()
        self.getWidget(5).show()    # Shows label that displays in full screen
        self.getWidget(5).setPixmap(pixContainer.scaled((self.W/1.33)-40, (self.H/1.28)-40, Qt.KeepAspectRatio))   # Sets image in selected label to full screen label
        self.layout.setContentsMargins(0, 0, 0, 0)    # Pushes image to the top of the window
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)    # Pushes image to the top of the window
        self.getTags().setAlignment(Qt.AlignRight)
        self.textBox.show()
        self.addButton.show()
        self.saveButton.show()
        self.drawTags()


    def circularTraverse(self, steps, direction):    # Responsible for Circular Traversing the image list in the given direction
        if direction == "left":
            return (self.image_index-steps)%(len(Models.images))
        else:
            return (self.image_index+steps)%(len(Models.images))

    def select(self, selected_index):   # Selects new item
        self.getWidget(self.selected_index).setStyleSheet("border: 10px solid red")   # Changes old image box to not selected border
        self.getWidget(selected_index).setStyleSheet("border: 10px solid green")    # Changes new image box to selected border
        self.selected_index = selected_index      # Updates Current selection index

    def shiftLeft(self):            # Shifts the select box and scope of the Thumbnail Bar to the left
        if self.selected_index != 0:         # Shift select box till first image
            if self.mode == 1:
                pixContainer = self.getWidget(self.selected_index-1).pixmap()
                self.getWidget(5).setPixmap(pixContainer.scaled((self.W/1.33)-40, (self.H/1.28)-40, Qt.KeepAspectRatio))
            self.select(self.selected_index-1)

        else:
            if 5 == 5:       # If there are more than 5 images, shift scope of Thumbnail Bar to left
                for i in range(4, 0, -1):     # Shifts scope
                    self.getWidget(i).setPixmap(self.getWidget(i-1).pixmap().scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio))
                self.getWidget(0).setPixmap(QPixmap("data/"+Models.images[self.circularTraverse(1, "left")]).scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio))
                if self.mode == 1:     # If in full screen mode, load previous image
                    self.getWidget(5).setPixmap(self.getWidget(0).pixmap().scaled((self.W/1.33)-40, (self.H/1.28)-40, Qt.KeepAspectRatio))
                self.image_index = self.circularTraverse(1, "left")

    def shiftRight(self):       # Shifts the select box and scope of the Thumbnail Bar to the right
        if self.selected_index != 4:      # Shift select box till last image
            if self.mode == 1:
                pixContainer = self.getWidget(self.selected_index+1).pixmap()
                self.getWidget(5).setPixmap(pixContainer.scaled((self.W/1.33)-40, (self.H/1.28)-40, Qt.KeepAspectRatio))
            self.select(self.selected_index+1)
        else:
            if 5 == 5:      # If there are more than 5 images, shift scope of Thumbnail Bar to rght
                for i in range(0, 4):    # Shifts scope
                    self.getWidget(i).setPixmap(self.getWidget(i+1).pixmap().scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio))
                self.getWidget(4).setPixmap(QPixmap("data/"+Models.images[self.circularTraverse(5, "right")]).scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio))
                if self.mode == 1:    # If in full screen mode, load next image
                    self.getWidget(5).setPixmap(self.getWidget(4).pixmap().scaled((self.W/1.33)-40, (self.H/1.28)-40, Qt.KeepAspectRatio))
                self.image_index = self.circularTraverse(1, "right")

    def shrink(self, index):     # Makes necessary changes to change back to Thumbnail Mode
        self.mode = 0       # Upadates mode variable
        self.getWidget(5).hide()    # Hides full screen label
        for i in range(0,5):    # Un-hides thumbnail labels
            self.getWidget(i).show()
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setAlignment(Qt.AlignVCenter)    # Pushes image to the top of the window
        self.textBox.hide()
        self.addButton.hide()
        self.saveButton.hide()
        for i in range(0, len(self.getTags())):
            self.getTags().itemAt(0).widget().setParent(None)
        self.layout.removeItem(self.tagList)




#=========================================== EVENT HANDLERS =========================================

    def loadTags(self):
        # If file exists, open and load tags. If does not exist, initialize empty tags dictionary
        try:
            f = open("tags.json","r")
            self.tags = json.load(f)
            f.close()
        except:
            self.tags = {}

    def addTag(self):
        if not (self.textBox.text().isspace() or self.textBox.text() == ""):
            image_key = str((self.image_index+self.selected_index)%len(Models.images))
            if image_key not in self.tags:
                self.tags[image_key] = []
            self.tags[image_key].append(self.textBox.text())
            self.textBox.setText("")
            self.setFocus()
            self.drawTags()

    def saveTags(self):
        f = open("tags.json", "w+")
        try:
            json.dump(self.tags, f)
        except:
            print(type(self.tags))
        f.close()
        self.setFocus()

    def getWidget(self, index):     # Gets stored widget from layout in the passed index
        return self.layout.itemAt(index).widget()

    def getTags(self):
        return self.layout.itemAt(6).layout()

    def indexOfLabel(self, label):      # Provides the index of the clicked label for further operations
        self.setFocus()
        if self.mode == 0:
            self.select(self.layout.indexOf(label))
            self.enlarge(self.layout.indexOf(label))

    def keyPressEvent(self, e):     # Handles all key press events
        if e.key() == Qt.Key_Right:
            self.sounds.select_sound.play()
            self.shiftRight()
            if self.mode == 1:
                self.drawTags()


        if e.key() == Qt.Key_Left:
            self.sounds.select_sound.play()
            self.shiftLeft()
            if self.mode == 1:
                self.drawTags()

        elif e.key() == Qt.Key_Period and self.mode == 0 and 5 == 5:    # Moves to the next 5 images only if there are enough images to overflow
            self.sounds.next_set_sound.play()
            self.image_index=self.circularTraverse(5, "right")
            for i in range(0,5):
                self.getWidget(i).setPixmap(QPixmap("data/"+Models.images[self.circularTraverse(i, "right")]).scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio))
            self.select(0)

        elif e.key() == Qt.Key_Comma and self.mode == 0 and 5 == 5:     # Moves to the previous 5 images only if there are enough images to overflow
            self.sounds.next_set_sound.play()
            self.image_index=self.circularTraverse(5, "left")
            for i in range(0,5):
                self.getWidget(i).setPixmap(QPixmap("data/"+Models.images[self.circularTraverse(i, "right")]).scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio))
            self.select(0)

        elif e.key() == Qt.Key_Up and self.mode == 0:
            self.enlarge(self.selected_index)

        elif e.key() == Qt.Key_Down and self.mode == 1:
            self.setFocus()
            self.shrink(self.selected_index)
            if 5 == 5:      # Checks if there are more than 5 images
                center_distance = self.selected_index - 2      # Calculates the distance of the seleted image from the center box
                if center_distance > 0:     # Checks if the selected image is right of center
                    # Shifts thumbnail bar accordingly to place selected image in middle on coming back to thumbnai bar mode:
                    for i in range(0, center_distance):
                        for j in range(0,4):
                            self.getWidget(j).setPixmap(self.getWidget(j+1).pixmap().scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio))
                        self.getWidget(4).setPixmap(QPixmap("data/"+Models.images[self.circularTraverse(5, "right")]).scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio))
                        self.image_index = self.circularTraverse(1, "right")
                elif center_distance < 0:      # Checks if selected image is left of center
                    # Shifts thumbnail bar accordingly to place selected image in middle on coming back to thumbnai bar mode:
                    for i in range(0, abs(center_distance)):
                        for j in range(4, 0, -1):
                            self.getWidget(j).setPixmap(self.getWidget(j-1).pixmap().scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio))
                        self.getWidget(0).setPixmap(QPixmap("data/"+Models.images[self.circularTraverse(1, "left")]).scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio))
                        self.image_index = self.circularTraverse(1, "left")
                self.select(2)

        elif e.key() == Qt.Key_Escape:      # Returns focus back to main window
            self.setFocus()
