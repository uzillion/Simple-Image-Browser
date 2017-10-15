"""
File: models.py
By: Uzair Inamdar
Last edited: 9/25/2017

This file is responsible for loading data and assets for the image-browser
"""

import os
import requests
import json
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QSoundEffect
class Models:

    def __init__(self, base):
        self.base = base
        # self.limit = base.rangeBox.text()
        # self.tag = base.searchBox.text()
        # self.tag = self.tag.replace(" ", "%20")
#======================== Images =======================
    dbImages = {}
    urlImages = []
    try:
        f = open("meta.json","r")
        dbImages = json.load(f)
        f.close()
    except:
        dbImages = {}

    def searchTag(self, tag):
        self.tag = tag
        self.tag = self.tag.replace(" ", "%20")

    def setLimit(self, limit):
        self.limit = limit

    def searchImages(self):
        req = 'https://api.flickr.com/services/rest/'
        req = req + '?method=flickr.photos.search'
        req = req + '&per_page='+self.limit
        req = req + '&format=json&nojsoncallback=1&extras=geo'
        req = req + '&api_key=83a6ef0d071350b24c6e8689e0078093'
        req = req + '&tags='+self.tag
        res = requests.get(req).json()
        imageList = res['photos']
        for img in imageList['photo']:
            imgPath = "https://farm"+str(img['farm'])+".staticflickr.com/"+str(img['server'])+"/"+str(img['id'])+"_"+str(img['secret'])+".jpg"
            print(imgPath)
            Models.urlImages.append(imgPath)

#======================== Sounds =======================
    def initSound(self):
        self.select_sound = QSoundEffect(self.base)
        self.next_set_sound = QSoundEffect(self.base)
        self.expand_sound = QSoundEffect(self.base)
        self.shrink_sound = QSoundEffect(self.base)
        self.select_sound.setSource(QUrl.fromLocalFile(os.path.join('./data/sounds','click.wav')))
        self.shrink_sound.setSource(QUrl.fromLocalFile(os.path.join('./data/sounds','click.wav')))
        self.next_set_sound.setSource(QUrl.fromLocalFile(os.path.join('./data/sounds','camera-roll.wav')))
        self.expand_sound.setSource(QUrl.fromLocalFile(os.path.join('./data/sounds','expand.wav')))
        self.select_sound.setLoopCount(0)
        self.shrink_sound.setLoopCount(0)
        self.expand_sound.setLoopCount(0)
        self.next_set_sound.setLoopCount(0)
