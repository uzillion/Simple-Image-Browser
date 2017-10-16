"""
File: view.py
By: Uzair Inamdar
Last edited: 10/16/2017

This file is responsible for handling the layout and events of the program
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QApplication
from PyQt5.QtGui import QPixmap
from models import *
from PyQt5.QtCore import *
from click_filter import *
import sys
import json
import urllib.request
import atexit
import shutil

class View(QWidget):

    def __init__(self, W):
        self.dump = False       # print debug info | True = print, False = Don't print
        self.firstRun = True
        self.testCounter = 0
        self.W = int(W)
        super().__init__()
        self.images = []
        self.models = Models(self)
        self.models.initSound()
        self.image_index = 0        # Keeps track of the first image in image list to be displayed in the thumbnail bar
        self.mode = 0         # Determines and Tracks current mode of view (1 - Full Screen, 0 - Thumbnail)
        self.selected_index = 0     # Keeps track of the current selected index in the thumbnail bar
        self.loadTags()
        self.loadImages()
        self.initUI()
        atexit.register(shutil.rmtree, './cache')       # On exit, delete cache folder that holds search image results

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
        self.tagBox = QLineEdit(self)
        self.tagBox.setStyleSheet("QLineEdit{ background: #f8f8f8; selection-background-color: #f8f8f8; }")
        self.tagBox.setPlaceholderText("Enter your tags here")
        self.tagBox.resize(self.W/2,self.H/10)
        self.tagBox.move(20, self.H*(5/6))

        # Setting-up seach box
        self.searchBox = QLineEdit(self)
        self.searchBox.setStyleSheet("QLineEdit{ background: #f8f8f8; selection-background-color: #f8f8f8; }")
        self.searchBox.setPlaceholderText("Enter search string...")
        self.searchBox.resize(self.W/2,self.H/10)
        self.searchBox.move(20, self.H*(4.5/6))

        # Setting-up range box
        self.rangeBox = QLineEdit(self)
        self.rangeBox.setStyleSheet("QLineEdit{ background: #f8f8f8; selection-background-color: #f8f8f8; }")
        self.rangeBox.resize(self.W/8,self.H/10)
        self.rangeBox.move(self.W/1.3, self.H*(4.5/6))
        self.rangeBox.setAlignment(Qt.AlignCenter)

        self.rangeText = QLabel(self)
        temp = "Max Search Results"
        self.rangeText.setText(temp)
        self.rangeText.setStyleSheet("font-weight: 600")
        self.rangeText.resize(self.W/3, self.H/14)
        self.rangeText.move(self.W/1.37, self.H*(6/7))

        # Setting-up test button
        self.testButton = QPushButton('Test', self)
        self.testButton.setStyleSheet("background-color: #F5F5F5")
        self.testButton.move(20,self.H*(6/7))
        self.testButton.resize(self.W/8, self.H/14)
        self.testButton.clicked.connect(self.testUrl)

        # Setting-up image save button
        self.imgSaveButton = QPushButton('Save', self)
        self.imgSaveButton.setStyleSheet("background-color: #F5F5F5")
        self.imgSaveButton.move(21+self.W/8, self.H*(6/7))
        self.imgSaveButton.resize(self.W/8, self.H/14)
        self.imgSaveButton.clicked.connect(self.saveImgs)

        # Setting-up image exit button
        self.exitButton = QPushButton('Exit', self)
        self.exitButton.setStyleSheet("background-color: #F5F5F5")
        self.exitButton.move(21+(2*self.W/8), self.H*(6/7))
        self.exitButton.resize(self.W/8, self.H/14)
        self.exitButton.clicked.connect(self.exitApp)

        # Setting-up image delete button
        self.deleteButton = QPushButton('Delete', self)
        self.deleteButton.setStyleSheet("background-color: #F5F5F5")
        self.deleteButton.move(21+(3*self.W/8), self.H*(6/7))
        self.deleteButton.resize(self.W/8, self.H/14)
        self.deleteButton.clicked.connect(self.deleteImg)

        # Setting-up search button for tags
        self.searchButton = QPushButton('Search', self)
        self.searchButton.setStyleSheet("background-color: #F5F5F5")
        self.searchButton.move(self.W/1.9,self.H*(4.55/6))
        self.searchButton.resize(self.W/8, self.H/12)
        self.searchButton.clicked.connect(self.searchTag)

        # Setting-up add and save buttons for tags
        self.addButton = QPushButton('Add Tag', self)
        self.addButton.setStyleSheet("background-color: #F5F5F5")
        self.addButton.move(self.W/1.9,self.H*(5/6))
        self.addButton.resize(self.W/6, self.H/10)
        self.addButton.clicked.connect(self.addTag)

        self.tagSaveButton = QPushButton('Save Tags', self)
        self.tagSaveButton.setStyleSheet("background-color: #F5F5F5")
        self.tagSaveButton.move(self.W/1.42,self.H*(5/6))
        self.tagSaveButton.resize(self.W/6, self.H/10)
        self.tagSaveButton.clicked.connect(self.saveTags)

        # Setting up layout for holding tags
        self.tagList = QVBoxLayout()
        self.tagList.setSpacing(10)
        self.tagList.setContentsMargins(40, 0, 5, 0)

        self.tagBox.hide()
        self.addButton.hide()
        self.tagSaveButton.hide()

        self.setFocus()
        if len(self.images) != 0:
            self.thumbnail_bar()
            self.select(0)
        self.show()

    def loadImages(self):
        for img in Models.dbImages:
            if img not in self.images:
                self.images = [img] + self.images       # Appending images from database
        for img in Models.urlImages:
            if img not in self.images:
                self.images = [img] + self.images       # Appending images from search results
        # print(self.images)
        Models.urlImages = []
        # if self.firstRun != True:
            # self.thumbnail_bar()

    def thumbnail_bar(self):     # Creates a List of QLabels and places them in a horizontal Layout
        labels = []
        if len(self.images) < 5:
            self.size = len(self.images)
        else:
            self.size = 5
        for i in range(0, 6):
            labels.insert(i, QLabel(self))
            if i < self.size:
                pixmap = QPixmap(self.images[i])
                labels[i].setPixmap(pixmap.scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio, Qt.SmoothTransformation))      # Sets images to each label in layout
                labels[i].setStyleSheet('border: 10px solid red')
            labels[i].setFixedSize((self.W-40)/5, (self.W-40)/5)
            labels[i].setAlignment(Qt.AlignCenter)      # Align images to the center of the label
            self.layout.addWidget(labels[i])        # Add label into layout container
            clickable(self.getWidget(i)).connect(self.indexOfLabel)     # Connects the click even to the indexOfLabel function

        # Properties of full screen view label:
        # labels.insert(5, QLabel(self))
        # labels[5].setAlignment(Qt.AlignCenter)
        # self.layout.addWidget(labels[5])
        # clickable(self.getWidget(5)).connect(self.indexOfLabel)
        self.getWidget(5).setStyleSheet('border: 20px solid red')
        self.getWidget(5).setFixedSize(self.W/1.33, self.H/1.28)
        self.getWidget(5).hide()
        self.firstRun = False

    def refresh(self, start):
        self.image_index = start
        if len(self.images) < 5:
            self.size = len(self.images)
        else:
            self.size = 5
        for i in range(0,self.size):
            pixmap = QPixmap(self.images[(self.image_index+i)%len(self.images)])
            self.getWidget(i).setPixmap(pixmap.scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            if i != self.selected_index:
                self.getWidget(i).setStyleSheet('border: 10px solid red')

        if self.selected_index >= len(self.images) and self.selected_index != 0:
            self.select(len(self.images)-1)
        if len(self.images) < 5:
            self.getWidget(len(self.images)).clear()
            self.getWidget(len(self.images)).setStyleSheet('border: none')

    def drawTags(self):
        image_key = self.images[(self.image_index+self.selected_index)%len(self.images)]
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
        self.models.expand_sound.play()
        self.layout.addLayout(self.tagList)     # Adding TagList layout to main layout
        self.mode = 1
        self.selected_index = index
        pixContainer = self.getWidget(index).pixmap()

        for i in range(0, self.size):   # Hiding thumbnail_bar
            self.getWidget(i).hide()
        self.searchBox.hide()
        self.testButton.hide()
        self.imgSaveButton.hide()
        self.exitButton.hide()
        self.deleteButton.hide()
        self.rangeText.hide()
        self.rangeBox.hide()
        self.searchButton.hide()

        self.getWidget(5).show()    # Shows label that displays in full screen
        self.getWidget(5).setPixmap(pixContainer.scaled((self.W/1.33)-40, (self.H/1.28)-40, Qt.KeepAspectRatio, Qt.SmoothTransformation))   # Sets image in selected label to full screen label
        self.layout.setContentsMargins(20, 0, 0, 0)    # Pushes image to the top of the window
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)    # Pushes image to the top of the window
        self.getTags().setAlignment(Qt.AlignRight)
        self.tagBox.show()
        self.addButton.show()
        self.tagSaveButton.show()
        self.drawTags()


    def circularTraverse(self, steps, direction):    # Responsible for Circular Traversing the image list in the given direction
        if direction == "left":
            return (self.image_index-steps)%(len(self.images))
        else:
            return (self.image_index+steps)%(len(self.images))

    def select(self, selected_index):   # Selects new item
        if selected_index < self.size:
            self.getWidget(self.selected_index).setStyleSheet("border: 10px solid red")   # Changes old image box to not selected border
            self.getWidget(selected_index).setStyleSheet("border: 10px solid green")    # Changes new image box to selected border
            self.selected_index = selected_index      # Updates Current selection index

    def shiftLeft(self):            # Shifts the select box and scope of the Thumbnail Bar to the left
        if self.selected_index != 0:         # Shift select box till first image
            if self.mode == 1:
                pixContainer = self.getWidget(self.selected_index-1).pixmap()
                self.getWidget(5).setPixmap(pixContainer.scaled((self.W/1.33)-40, (self.H/1.28)-40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.select(self.selected_index-1)

        else:
            if len(self.images)>=5:       # If there are more than 5 images, shift scope of Thumbnail Bar to left
                for i in range(4, 0, -1):     # Shifts scope
                    self.getWidget(i).setPixmap(self.getWidget(i-1).pixmap().scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                pixmap = QPixmap(self.images[self.circularTraverse(1, "left")])
                self.getWidget(0).setPixmap(pixmap.scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                if self.mode == 1:     # If in full screen mode, load previous image
                    self.getWidget(5).setPixmap(self.getWidget(0).pixmap().scaled((self.W/1.33)-40, (self.H/1.28)-40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.image_index = self.circularTraverse(1, "left")

    def shiftRight(self):       # Shifts the select box and scope of the Thumbnail Bar to the right
        if len(self.images) >= 5:
            upper_limit = 4
        else:
            upper_limit = len(self.images)-1

        if self.selected_index != upper_limit:      # Shift select box till last image
            if self.mode == 1:
                pixContainer = self.getWidget(self.selected_index+1).pixmap()
                self.getWidget(5).setPixmap(pixContainer.scaled((self.W/1.33)-40, (self.H/1.28)-40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.select(self.selected_index+1)
        else:
            if len(self.images) >= 5:      # If there are more than 5 images, shift scope of Thumbnail Bar to rght
                for i in range(0, 4):    # Shifts scope
                    self.getWidget(i).setPixmap(self.getWidget(i+1).pixmap().scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                temp_img = self.images[self.circularTraverse(5, "right")]
                pixmap = QPixmap(temp_img)
                # print(temp_img)
                self.getWidget(4).setPixmap(pixmap.scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                if self.mode == 1:    # If in full screen mode, load next image
                    self.getWidget(5).setPixmap(self.getWidget(4).pixmap().scaled((self.W/1.33)-40, (self.H/1.28)-40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.image_index = self.circularTraverse(1, "right")

    def shrink(self, index):     # Makes necessary changes to change back to Thumbnail Mode
        self.models.expand_sound.play()
        self.mode = 0       # Upadates mode variable
        self.getWidget(5).hide()    # Hides full screen label

        for i in range(0,self.size):    # Un-hides thumbnail labels
            self.getWidget(i).show()
        self.searchBox.show()
        self.testButton.show()
        self.imgSaveButton.show()
        self.exitButton.show()
        self.deleteButton.show()
        self.rangeText.show()
        self.rangeBox.show()
        self.searchButton.show()

        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setAlignment(Qt.AlignVCenter)    # Pushes image to the top of the window
        self.tagBox.hide()
        self.addButton.hide()
        self.tagSaveButton.hide()
        for i in range(0, len(self.getTags())):
            self.getTags().itemAt(0).widget().setParent(None)
        self.layout.removeItem(self.tagList)




#=========================================== EVENT HANDLERS =========================================

    def testUrl(self):
        try:
            urllib.request.urlretrieve(self.searchBox.text(), "./cache/"+str(self.testCounter)+".jpg")
        except:
            print('Problem in retrieving image from url')
        self.searchBox.setText("")
        test_image = "./cache/"+str(self.testCounter)+".jpg"
        self.images = [test_image] + self.images
        if self.firstRun:
            self.thumbnail_bar()
        else:
            self.refresh(0)
        self.select(self.images.index(test_image))
        self.setFocus()

    def saveImgs(self):
        for img in self.images:
            if img not in Models.dbImages:               # Look for unsaved images
                shutil.copy2(img, './data')              # Copy new images to database
                Models.dbImages = [img.replace('./cache', './data')] + Models.dbImages      # Update registry
                if img in self.tags:
                    url_tags = self.tags[img]           # Copy the new image tags to permanent resgistry
                    del self.tags[img]                  # Remove temp tags from registry
                else:
                    url_tags = []
                self.tags[img.replace('./cache', './data')] = url_tags      # Associate tags to proper path
        if len(self.images) == 0:
            self.tags = {}
        self.saveTags()
        if len(self.images) != 0:
            self.images = []
            self.loadImages()
            self.refresh(0)
        self.setFocus()

    def exitApp(self):
        sys.exit()

    def deleteImg(self):
        if len(self.images) > 0:
            image = self.images[(self.image_index+self.selected_index)%len(self.images)]    # Get the image file name to be deleted
            if image in self.tags:      # Check if image had any tags, if true delete them
                del self.tags[image]
            os.remove(image)    # Remove the file form the file system
            self.images.remove(image)   # Remove image from load list
            self.refresh(self.image_index)  # Refresh the display
            self.setFocus()

    def searchTag(self):
        if not (self.searchBox.text().isspace() or self.searchBox.text() == ""):
            self.models.searchTag(self.searchBox.text())
            if self.rangeBox.text() != "":
                self.models.setLimit(self.rangeBox.text())
            else:
                self.models.setLimit("10")      # Setting default search result to 10 results
            self.models.searchImages()
            self.loadImages()
            # print(Models.urlImages)
            if self.firstRun:
                self.thumbnail_bar()
            else:
                self.refresh(0)
            self.select(0) # Selects first image-box in layout
            self.setFocus()
            self.searchBox.setText("")

    def loadTags(self):
        # If file exists, open and load tags. If does not exist, initialize empty tags dictionary
        try:
            f = open("tags.json","r")
            self.tags = json.load(f)
            f.close()
        except:
            self.tags = {}

    def addTag(self):
        # Add tag if not empty string or spaces
        if not (self.tagBox.text().isspace() or self.tagBox.text() == ""):
            # image_key = str((self.image_index+self.selected_index)%len(self.images)) # Generating image key for dictionary from unique combination of image_index and selected_index
            image_key = self.images[(self.image_index+self.selected_index)%len(self.images)]
            if image_key not in self.tags:      # If no tags exist, create a new list for tags
                self.tags[image_key] = []
            self.tags[image_key].append(self.tagBox.text())    # Append to the tags lis of image
            self.tagBox.setText("")
            self.setFocus()     # Return focus to main window
            self.drawTags()

    def saveTags(self):
        try:
            os.remove('tags.json')
        except:
            pass
        f = open("tags.json", "w+")        # Create file if does not exist
        json.dump(self.tags, f)     # save tags in file
        print("{} saved".format(self.tags))
        f.close()
        self.setFocus()     # Return focus back to window

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

        if e.key() == Qt.Key_Right and len(self.images)>0:
            self.models.select_sound.play()
            self.shiftRight()
            if self.mode == 1:
                self.drawTags()


        if e.key() == Qt.Key_Left and len(self.images)>0:
            self.models.select_sound.play()
            self.shiftLeft()
            if self.mode == 1:
                self.drawTags()

        elif e.key() == Qt.Key_Period and self.mode == 0 and len(self.images) > 5:    # Moves to the next 5 images only if there are enough images to overflow
            self.models.next_set_sound.play()
            self.image_index=self.circularTraverse(5, "right")
            for i in range(0,5):
                self.getWidget(i).setPixmap(QPixmap("data/"+self.images[self.circularTraverse(i, "right")]).scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.select(0)

        elif e.key() == Qt.Key_Comma and self.mode == 0 and len(self.images) > 5:     # Moves to the previous 5 images only if there are enough images to overflow
            self.models.next_set_sound.play()
            self.image_index=self.circularTraverse(5, "left")
            for i in range(0,5):
                self.getWidget(i).setPixmap(QPixmap("data/"+self.images[self.circularTraverse(i, "right")]).scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.select(0)

        elif e.key() == Qt.Key_Up and self.mode == 0 and len(self.images) > 0:
            self.enlarge(self.selected_index)

        elif e.key() == Qt.Key_Down and self.mode == 1:
            self.setFocus()
            self.shrink(self.selected_index)
            if len(self.images) >= 5:      # Checks if there are more than 5 images
                center_distance = self.selected_index - 2      # Calculates the distance of the seleted image from the center box
                if center_distance > 0:     # Checks if the selected image is right of center
                    # Shifts thumbnail bar accordingly to place selected image in middle on coming back to thumbnai bar mode:
                    for i in range(0, center_distance):
                        for j in range(0,4):
                            self.getWidget(j).setPixmap(self.getWidget(j+1).pixmap().scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        self.getWidget(4).setPixmap(QPixmap(self.images[self.circularTraverse(5, "right")]).scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        self.image_index = self.circularTraverse(1, "right")
                elif center_distance < 0:      # Checks if selected image is left of center
                    # Shifts thumbnail bar accordingly to place selected image in middle on coming back to thumbnai bar mode:
                    for i in range(0, abs(center_distance)):
                        for j in range(4, 0, -1):
                            self.getWidget(j).setPixmap(self.getWidget(j-1).pixmap().scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        self.getWidget(0).setPixmap(QPixmap(self.images[self.circularTraverse(1, "left")]).scaled(((self.W-40)/5)-20, ((self.W-40)/5)-20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        self.image_index = self.circularTraverse(1, "left")
                self.select(2)

        elif e.key() == Qt.Key_Escape:      # Returns focus back to main window
            self.setFocus()

        if self.dump and len(self.images) > 0:
            image_key = self.images[(self.image_index+self.selected_index)%len(self.images)]
            print('\nimage_index: {}'.format(self.image_index))
            print('select_index: {} ({})'.format(self.selected_index, image_key))
            try:
                print('tags: {}'.format(self.tags[image_key]))
            except:
                print('tags: []')
