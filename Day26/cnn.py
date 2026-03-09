# cnn_project_fixed.py
# Comprehensive CNN Project – Image Classification & Computer Vision

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from tensorflow.keras import layers, models, regularizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNet

print("TensorFlow Version:", tf.__version__)
print("GPU Available:", tf.config.list_physical_devices('GPU'))

# --------------------------------------------------
# SECTION 1 — DATASET LOADING
# --------------------------------------------------

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

class_names = ['airplane','automobile','bird','cat','deer',
               'dog','frog','horse','ship','truck']

print("Training samples:", x_train.shape[0])
print("Image size:", x_train.shape[1:])
print("Number of classes:", len(class_names))

# --------------------------------------------------
# SECTION 2 — IMAGE FUNDAMENTALS
# --------------------------------------------------

plt.figure(figsize=(10,6))
for i in range(10):
    plt.subplot(2,5,i+1)
    plt.imshow(x_train[i])
    plt.title(class_names[y_train[i][0]])
    plt.axis("off")
plt.show()

# RGB to Grayscale
img = x_train[0]
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

plt.subplot(1,2,1)
plt.imshow(img)
plt.title("RGB")

plt.subplot(1,2,2)
plt.imshow(gray, cmap="gray")
plt.title("Grayscale")
plt.show()

# Histogram
plt.hist(img.flatten(), bins=50)
plt.title("Pixel Value Distribution")
plt.show()

# Normalize images
x_train = x_train / 255.0
x_test = x_test / 255.0

# --------------------------------------------------
# SECTION 3 — MATH FOUNDATIONS
# --------------------------------------------------

print("Image matrix shape:", img.shape)

v1 = np.array([1,2,3])
v2 = np.array([4,5,6])

print("Dot Product:", np.dot(v1,v2))

A = np.random.rand(3,3)
B = np.random.rand(3,3)

print("Matrix Multiplication:\n", np.matmul(A,B))

# Manual Convolution
kernel = np.array([[1,0,-1],[1,0,-1],[1,0,-1]])
img_gray = gray

h,w = img_gray.shape
output = np.zeros((h-2,w-2))

for i in range(h-2):
    for j in range(w-2):
        region = img_gray[i:i+3, j:j+3]
        output[i,j] = np.sum(region * kernel)

plt.imshow(output, cmap="gray")
plt.title("Manual Convolution Output")
plt.show()

# --------------------------------------------------
# SECTION 4 — BASIC CNN
# --------------------------------------------------

def build_cnn(activation='relu'):

    model = models.Sequential([
        layers.Conv2D(32,(3,3),activation=activation,input_shape=(32,32,3)),
        layers.MaxPooling2D((2,2)),
        layers.Conv2D(64,(3,3),activation=activation),
        layers.MaxPooling2D((2,2)),
        layers.Conv2D(64,(3,3),activation=activation),
        layers.Flatten(),
        layers.Dense(64,activation=activation),
        layers.Dense(10,activation='softmax')
    ])

    return model

model = build_cnn()

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

history = model.fit(
    x_train,y_train,
    epochs=5,
    validation_data=(x_test,y_test)
)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.legend(["Train","Validation"])
plt.title("Training vs Validation Accuracy")
plt.show()

# --------------------------------------------------
# SECTION 5 — POOLING COMPARISON
# --------------------------------------------------

input_img = layers.Input(shape=(32,32,3))

conv = layers.Conv2D(32,(3,3),activation='relu')(input_img)

max_pool = layers.MaxPooling2D((2,2))(conv)
avg_pool = layers.AveragePooling2D((2,2))(conv)

model_max = models.Model(input_img,max_pool)
model_avg = models.Model(input_img,avg_pool)

# --------------------------------------------------
# SECTION 6 — REGULARIZATION
# --------------------------------------------------

model_dropout = models.Sequential([
    layers.Conv2D(32,(3,3),activation='relu',input_shape=(32,32,3)),
    layers.MaxPooling2D((2,2)),
    layers.Dropout(0.5),
    layers.Flatten(),
    layers.Dense(128,activation='relu',
                 kernel_regularizer=regularizers.l2(0.001)),
    layers.Dense(10,activation='softmax')
])

model_dropout.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model_dropout.fit(x_train,y_train,epochs=5,validation_data=(x_test,y_test))

# --------------------------------------------------
# SECTION 7 — BATCH NORMALIZATION
# --------------------------------------------------

model_bn = models.Sequential([
    layers.Conv2D(32,(3,3),activation='relu',input_shape=(32,32,3)),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(64,(3,3),activation='relu'),
    layers.BatchNormalization(),
    layers.Flatten(),
    layers.Dense(64,activation='relu'),
    layers.Dense(10,activation='softmax')
])

model_bn.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model_bn.fit(x_train,y_train,epochs=5,validation_data=(x_test,y_test))

# --------------------------------------------------
# SECTION 8 — DATA AUGMENTATION
# --------------------------------------------------

datagen = ImageDataGenerator(
    rotation_range=20,
    horizontal_flip=True,
    zoom_range=0.2
)

datagen.fit(x_train)

model.fit(
    datagen.flow(x_train,y_train,batch_size=32),
    epochs=5,
    validation_data=(x_test,y_test)
)

# --------------------------------------------------
# SECTION 9 — HYPERPARAMETER TUNING
# --------------------------------------------------

learning_rates = [0.1,0.01,0.001]

for lr in learning_rates:

    temp_model = build_cnn()

    opt = tf.keras.optimizers.Adam(learning_rate=lr)

    temp_model.compile(
        optimizer=opt,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    print("Training with learning rate:", lr)

    temp_model.fit(x_train,y_train,epochs=2)

# --------------------------------------------------
# SECTION 10 — TRANSFER LEARNING (MobileNet)
# --------------------------------------------------

print("Preparing images for MobileNet...")

x_train_resized = tf.image.resize(x_train,(96,96))
x_test_resized = tf.image.resize(x_test,(96,96))

base_model = MobileNet(
    weights='imagenet',
    include_top=False,
    input_shape=(96,96,3)
)

for layer in base_model.layers:
    layer.trainable = False

x = layers.Flatten()(base_model.output)
x = layers.Dense(128,activation='relu')(x)
output = layers.Dense(10,activation='softmax')(x)

transfer_model = models.Model(base_model.input,output)

transfer_model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

transfer_model.fit(
    x_train_resized,y_train,
    epochs=5,
    validation_data=(x_test_resized,y_test)
)

# --------------------------------------------------
# SECTION 11 — LENET MODEL
# --------------------------------------------------

lenet = models.Sequential([
    layers.Conv2D(6,(5,5),activation='relu',input_shape=(32,32,3)),
    layers.AveragePooling2D((2,2)),
    layers.Conv2D(16,(5,5),activation='relu'),
    layers.AveragePooling2D((2,2)),
    layers.Flatten(),
    layers.Dense(120,activation='relu'),
    layers.Dense(84,activation='relu'),
    layers.Dense(10,activation='softmax')
])

lenet.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

lenet.fit(x_train,y_train,epochs=5)

# --------------------------------------------------
# SECTION 12 — BASIC OBJECT DETECTION (YOLO)
# --------------------------------------------------

if os.path.exists("yolov3.weights") and os.path.exists("yolov3.cfg"):

    net = cv2.dnn.readNet("yolov3.weights","yolov3.cfg")

    image = cv2.imread("sample.jpg")

    if image is not None:

        height,width,_ = image.shape

        blob = cv2.dnn.blobFromImage(
            image,
            1/255,
            (416,416),
            swapRB=True
        )

        net.setInput(blob)

        layer_names = net.getUnconnectedOutLayersNames()

        outputs = net.forward(layer_names)

        print("YOLO detection executed")

else:

    print("YOLO files not found — skipping object detection")

print("Project Execution Complete")