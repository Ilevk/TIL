import os
from datetime import datetime
import shutil

import numpy  as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from google.cloud import storage

key_file = 'disco-abacus-265000-8cfc5503d74e.json'

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_file

mnist = tf.keras.datasets.mnist

fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

train_images = train_images / 255.0

test_images = test_images / 255.0

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=3)

model_name = 'simple_keras_mnist_model'

if os.path.exists(model_name):
    shutil.rmtree(model_name)

path = tf.keras.experimental.export_saved_model(model,
                                               saved_model_path=model_name)

# model_name = 'model_{:.4f}'.format(model.evaluate(test_images,
#                                                   test_labels))

client   = storage.Client.from_service_account_json(key_file).bucket('mnist_ml_serving_test')
bucket   = storage.Client().bucket('mnist_ml_serving_test')

now = datetime.now().strftime('%Y%m%d_%H%M')

def upload_file(fname):
    blob_name = f'prediction/{now}-{model_name}-{fname}'
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(os.path.join(model_name, fname))

for file_name in os.listdir(model_name):
    if file_name == 'saved_model.pb':
        upload_file(file_name)
    else:
        for sub_file_name in os.listdir(os.path.join(model_name, file_name)):
            upload_file(os.path.join(file_name, sub_file_name))
