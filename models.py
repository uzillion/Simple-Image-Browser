"""
File: models.py
By: Uzair Inamdar
Last edited: 9/25/2017

This file is responsible for loading data and assets for the image-browser
"""

import os
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QSoundEffect
class Models:

    def __init__(self, base):
        self.base = base
#======================== Images =======================
    images = []
    for file_ in os.listdir("./data"):
        x=4
        if file_.endswith((".jpg", ".jpeg", ".png")):
            images.append(file_)

#======================== Sounds =======================
    def initSound(self):
        self.select_sound = QSoundEffect(self.base)
        self.next_set_sound = QSoundEffect(self.base)
        self.expand_sound = QSoundEffect(self.base)
        self.select_sound.setSource(QUrl.fromLocalFile(os.path.join('./data/sounds','click.wav')))
        self.next_set_sound.setSource(QUrl.fromLocalFile(os.path.join('./data/sounds','camera-roll.wav')))
        self.expand_sound.setSource(QUrl.fromLocalFile(os.path.join('./data/sounds','expand.wav')))
        self.select_sound.setLoopCount(0)
        self.expand_sound.setLoopCount(0)
        self.next_set_sound.setLoopCount(0)
