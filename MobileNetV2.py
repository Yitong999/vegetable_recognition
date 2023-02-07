# -*- coding: utf-8 -*-

import tensorflow as tf
import matplotlib.pyplot as plt
from time import *
import random



'''
Load the data, adjusting for further training.

@param data_dir: data path for training
@param test_data_dir: data path for evaluation
@param img_height: adjusted img height
@param: img_width: adjust img width
@param: batch_size: carefully chosen batch size
'''

def data_load(data_dir, test_data_dir, img_height, img_width, batch_size):
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        label_mode='categorical',
        seed=10,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        test_data_dir,
        label_mode='categorical',
        seed=10,
        image_size=(img_height, img_width),
        batch_size=batch_size)
    class_names = train_ds.class_names

    return train_ds, val_ds, class_names

#construct MobileNetV2 model
#Do transfer learning
def model_load(IMG_SHAPE=(224, 224, 3), class_num=12):
    # load mobilenet model
    base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                                   include_top=False,
                                                   weights='imagenet')
    base_model.trainable = False
    model = tf.keras.models.Sequential([
        tf.keras.layers.experimental.preprocessing.Rescaling(1. / 127.5, offset=-1, input_shape=IMG_SHAPE),
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(class_num, activation='softmax')
    ])
    model.summary()
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


# The learning curve
#save the curve graph to results.png
def show_loss_acc(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    plt.style.use('fast')
    plt.figure(figsize=(8, 8))
    plt.subplot(2, 1, 1)
    plt.plot(acc, label='Training Accuracy')
    plt.plot(val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.ylabel('Accuracy')
    plt.ylim([min(plt.ylim()), 1])
    plt.title('Training and Validation Accuracy')

    plt.subplot(2, 1, 2)
    plt.plot(loss, label='Training Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.ylabel('Cross Entropy')
    plt.title('Training and Validation Loss')
    plt.xlabel('epoch')
    plt.savefig('results.png', dpi=100)


def train(epochs):
    begin_time = time()
    train_ds, val_ds, class_names = data_load("data/train",
                                              "data/val", 224, 224, 16)
    print(class_names)
    model = model_load(class_num=len(class_names))

    history = model.fit(train_ds, validation_data=val_ds, epochs=epochs)

    model.save("models/vege_model.h5")

    end_time = time()
    run_time = end_time - begin_time
    print('total training time：', run_time, "s")

    show_loss_acc(history)



if __name__ == '__main__':
    train(epochs=10) #10 times for training
