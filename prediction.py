import tensorflow.keras.models as models
import os
import sys
import cv2
from PIL import Image
import numpy as np
import shutil
import time


def predict_img():

        isExist = os.path.exists('ToBePredicted/target.png')
        while (isExist == False):
            time.sleep(5)
            isExist = os.path.exists('ToBePredicted/target.png')

        img = cv2.imread('ToBePredicted/target.png')
        img = cv2.resize(img, (224, 224))

        img = np.asarray(img)  # alter the img to numpy array
        outputs = model.predict(img.reshape(1, 224, 224, 3))  # The result of prediction with probabilities
        print(outputs)
        index = int(np.argmax(outputs))
        return index

if __name__ == "__main__":
    while True:
        model = models.load_model("models/vege_model.h5")
        class_names = ['Broccoli', 'Cabbage', 'Carrot', 'Eggplant']
        class_dict = {}

        index = predict_img()
        print("The predicted result is " + class_names[index])

        f = open("pred_result.txt", "w")
        f.write(class_names[index])
        f.close()
        time.sleep(1)
