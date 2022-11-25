import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, Flatten
import random
import time
from PIL import Image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

label_to_text = {0:'anger', 1:'disgust', 2:'fear', 3:'happiness', 4: 'sadness', 5: 'surprise', 6: 'neutral'}

def to_pixels(image):
    "преобразование изображения в нужный формат для предсказания"
    width = image.size[0]  # Определяем ширину
    height = image.size[1]  # Определяем высоту
    pixels = image.load()
    s = []
    for j in range(width):
        for i in range(height):
            p = pixels[i, j]
            p = sum(p)/3
            s.append(str(p))
    return s

def recognise(image_name):
    "предсказание значения нейросетью"
    model_name = 'best_model.h5'
    path_to_model = os.path.join('neural_models.', model_name)
    model = tf.keras.models.load_model(path_to_model)  # загружаем лучшую из обученных моделей

    image = Image.open(image_name)  # Открываем изображение
    image = image.resize((48, 48))
    image = to_pixels(image)

    image = np.array(image, dtype=float).reshape((48, 48))

    predicted = model.predict(tf.expand_dims(image, 0)).argmax()
    print(f"Prediction: {label_to_text[predicted]}")
    plt.imshow(image.reshape((48, 48)))
    plt.show()

image_name1 = "media/calculation_image/2022/11/25/hapiness.jpg"
image_name2 = "media/calculation_image/2022/11/24/sadness.jpg"
recognise(image_name1)
recognise(image_name2)