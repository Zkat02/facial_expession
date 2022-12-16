import os
import numpy as np
from tensorflow import keras, expand_dims
from PIL import Image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

label_to_text = {0: 'anger', 1: 'disgust', 2: 'fear', 3: 'happiness', 4: 'sadness', 5: 'surprise', 6: 'neutral'}


def to_pixels(image):
    """
    convert image into pixels brightness string
    """
    width = image.size[0]
    height = image.size[1]
    pixels = image.load()
    s = []
    for j in range(width):
        for i in range(height):
            p = pixels[i, j]
            p = sum(p) / 3
            s.append(str(p))
    return s


def recognise(image_name):
    """
    prediction facial expression by neural network
    image_name : string that describe path to image
    """

    model_name = 'best_model.h5'
    path_to_model = os.path.join('neural_models.', model_name)
    model = keras.models.load_model(path_to_model)  # загружаем лучшую из обученных моделей

    image = Image.open(image_name)  # Открываем изображение
    image = image.resize((48, 48))
    image = to_pixels(image)

    image = np.array(image, dtype=float).reshape((48, 48))

    predicted = model.predict(expand_dims(image, 0)).argmax()
    prediction = label_to_text[predicted]
    print(f"Prediction: {prediction}")
    return prediction
