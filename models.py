"""
File: models.py
By: Uzair Inamdar
Last edited: 10/16/2017

This file is responsible for loading data and assets for the image-browser
"""

import os
import shutil
import requests
import json
import urllib.request
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QSoundEffect
class Models:

    def __init__(self, base):
        self.base = base
        try:
            os.mkdir('./data')
        except:
            pass
        try:
            os.mkdir('./cache')
        except:
            shutil.rmtree('./cache')
            os.mkdir('./cache')
        # self.limit = base.rangeBox.text()
        # self.tag = base.searchBox.text()
        # self.tag = self.tag.replace(" ", "%20")
#======================== Images =======================
    dbImages = []
    urlImages = []
    for file_ in os.listdir("./data"):
        if file_.endswith((".jpg", ".jpeg", ".png")):
            dbImages.append("./data/"+file_)

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
        print('=========================================================')
        for img in imageList['photo']:
            imgPath = "https://farm"+str(img['farm'])+".staticflickr.com/"+str(img['server'])+"/"+str(img['id'])+"_"+str(img['secret'])+".jpg"
            print(imgPath)
            urllib.request.urlretrieve(imgPath, "./cache/"+str(img['id'])+"_"+str(img['secret'])+".jpg")
        print('=========================================================')
        for file_ in os.listdir("./cache"):
            Models.urlImages.append("./cache/"+file_)

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
