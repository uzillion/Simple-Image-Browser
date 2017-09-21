from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from images import *
import controller
from PyQt5.QtCore import Qt
class View(QWidget, controller.Controller):

    def __init__(self):
        super().__init__()
        self.image_index = 0        # Keeps track of the first image in image list to be displayed in the thumbnail bar
        self.mode = 0         # Determines and Tracks current mode of view (1 - Full Screen, 0 - Thumbnail)
        self.selected_index = 0     # Keeps track of the current selected index in the thumbnail bar
        self.layout = QHBoxLayout(self)     # Creates a Horizontal Layout
        self.layout.setContentsMargins(20, 0, 20, 0)    # Removes margins around stored object in the layout
        self.layout.setSpacing(0)           # Removes spaces between layout objects
        self.thumbnail_bar()
        self.select(0)        # Selects first image-box in layout

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setStyleSheet("background-color: #324d7a")
        self.move(250, 250)
        self.setFixedSize(800, 600)
        self.layout = QHBoxLayout(self)     # Creates a Horizontal Layout
        self.layout.setContentsMargins(20, 0, 20, 0)    # Removes margins around stored object in the layout
        self.layout.setSpacing(0)           # Removes spaces between layout objects
        self.thumbnail_bar()
        self.select(0) # Selects first image-box in layou
        self.show()

    def thumbnail_bar(self):     # Creates a List of QLabels and places them in a horizontal Layout
        labels = []
        self.size = 5
        if len(Images.images) < 5:       # If there are less than 5 images
            self.size = len(Images.images)
        for i in range(0, self.size+1):
            labels.insert(i, QLabel(self))
            if i != (self.size):
                labels[i].setPixmap(QPixmap("data/"+self.images[i]).scaled(132, 132, Qt.KeepAspectRatio))      # Sets images to each label in layout
                labels[i].setMaximumSize(152,152)
            labels[i].setAlignment(Qt.AlignCenter)      # Align images to the center of the label
            labels[i].setStyleSheet('border: 10px solid red')
            self.layout.addWidget(labels[i])        # Add label into layout container
            self.clickable(self.getWidget(i)).connect(self.indexOfLabel)     # Connects the click even to the indexOfLabel function

        # Properties of full screen view label:
        self.getWidget(self.size).setStyleSheet('border: 20px solid red')
        self.getWidget(self.size).setMinimumSize(800, 600)
        self.getWidget(self.size).hide()

        def enlarge(self, index):    # Makes necessary changes to change to Full Screen (Window Fill) Mode
            self.mode = 1
            self.selected_index = index
            pixContainer = self.getWidget(index).pixmap()
            for i in range(0, self.size):
                self.getWidget(i).hide()
            self.getWidget(self.size).show()    # Shows label that displays in full screen
            self.getWidget(self.size).setPixmap(pixContainer.scaled(760, 560, Qt.KeepAspectRatio))   # Sets image in selected label to full screen label
            self.layout.setContentsMargins(0, 0, 0, 500)    # Pushes image to the top of the window
