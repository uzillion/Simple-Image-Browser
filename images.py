import os
class Images:
    images = []
    for file_ in os.listdir("./data"):
        x=4
        if file_.endswith((".jpg", ".jpeg", ".png")):
            images.append(file_)
