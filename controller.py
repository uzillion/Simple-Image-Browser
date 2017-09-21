class Controller:

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

    def circularTraverse(self, steps, direction):    # Responsible for Circular Traversing the image list in the given direction
        if direction == "left":
            return (self.image_index-steps)%(len(self.images))
        else:
            return (self.image_index+steps)%(len(self.images))



    def getWidget(self, index):     # Gets stored widget from layout in the passed index
        return layout.itemAt(index).widget()

    def indexOfLabel(self, label):      # Provides the index of the clicked label for further operations
        if self.mode == 0:
            self.select(view.layout.indexOf(label))
            self.enlarge(view.layout.indexOf(label))

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
        view.layout.setContentsMargins(20, 0, 20, 0)



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
