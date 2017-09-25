import os
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QSoundEffect
class Models:

#======================== Images =======================
    images = []
    for file_ in os.listdir("./data"):
        x=4
        if file_.endswith((".jpg", ".jpeg", ".png")):
            images.append(file_)

#======================== Sounds =======================
    select_sound = QSoundEffect()
    next_set_sound = QSoundEffect()
    select_sound.setSource(QUrl.fromLocalFile(os.path.join('sounds','click.wav')))
    next_set_sound.setSource(QUrl.fromLocalFile(os.path.join('sounds','camera-roll.wav')))
    select_sound.setLoopCount(0)
    next_set_sound.setLoopCount(0)
