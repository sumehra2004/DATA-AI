# Intelligent CNN System for Image Recognition
# Dataset: CIFAR-10

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.models import load_model

print("TensorFlow Version:", tf.__version__)

# -------------------------------------------------
# SECTION 1 — DATASET PREPARATION
# -------------------------------------------------

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

class_names = [
'airplane','automobile','bird','cat','deer',
'dog','frog','horse','ship','truck'
]

print("Training Images:", x_train.shape[0])
print("Testing Images:", x_test.shape[0])
print("Image Dimensions:", x_train.shape[1:])
print("Number of Classes:", len(class_names))

# Dataset summary table
data = {
"Training Samples":[x_train.shape[0]],
"Testing Samples":[x_test.shape[0]],
"Classes":[len(class_names)]
}
df = pd.DataFrame(data)
print(df)

# Visualize 12 images
plt.figure(figsize=(10,6))
for i in range(12):
    plt.subplot(3,4,i+1)
    plt.imshow(x_train[i])
    plt.title(class_names[y_train[i][0]])
    plt.axis('off')
plt.show()

# Dataset imbalance analysis
unique, counts = np.unique(y_train, return_counts=True)
print("Samples per class:")
for u,c in zip(unique,counts):
    print(class_names[u],":",c)

# -------------------------------------------------
# SECTION 2 — IMAGE PREPROCESSING
# -------------------------------------------------

# Resize example
resized = cv2.resize(x_train[0], (32,32))

# Normalize pixels
x_train = x_train / 255.0
x_test = x_test / 255.0

# Noise removal
blur = cv2.GaussianBlur(x_train[0],(3,3),0)

# Contrast adjustment
contrast = cv2.convertScaleAbs(x_train[0], alpha=1.5, beta=0)

# Brightness adjustment
bright = cv2.convertScaleAbs(x_train[0], alpha=1, beta=40)

# -------------------------------------------------
# SECTION 3 — CNN MODEL DESIGN
# -------------------------------------------------

def create_cnn():
    model = models.Sequential([
        layers.Conv2D(32,(3,3),activation='relu',input_shape=(32,32,3)),
        layers.MaxPooling2D((2,2)),
        layers.Conv2D(64,(3,3),activation='relu'),
        layers.MaxPooling2D((2,2)),
        layers.Conv2D(128,(3,3),activation='relu'),
        layers.Flatten(),
        layers.Dense(128,activation='relu'),
        layers.Dense(10,activation='softmax')
    ])
    return model

model = create_cnn()

model.compile(
optimizer='adam',
loss='sparse_categorical_crossentropy',
metrics=['accuracy']
)

model.summary()

history = model.fit(
x_train,y_train,
epochs=10,
validation_split=0.2,
batch_size=64
)

# Plot accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("Training vs Validation Accuracy")
plt.legend(["train","validation"])
plt.show()

# -------------------------------------------------
# SECTION 4 — MODEL EVALUATION
# -------------------------------------------------

test_loss, test_acc = model.evaluate(x_test,y_test)
print("Test Accuracy:",test_acc)

predictions = model.predict(x_test)
pred_labels = np.argmax(predictions,axis=1)

# Confusion Matrix
cm = confusion_matrix(y_test,pred_labels)
print("Confusion Matrix:\n",cm)

# Classification Report
print(classification_report(y_test,pred_labels,target_names=class_names))

# Show predictions
plt.figure(figsize=(10,5))
for i in range(10):
    plt.subplot(2,5,i+1)
    plt.imshow(x_test[i])
    plt.title(class_names[pred_labels[i]])
    plt.axis('off')
plt.show()

# -------------------------------------------------
# SECTION 5 — MODEL IMPROVEMENT
# -------------------------------------------------

improved_model = models.Sequential([
layers.Conv2D(32,(3,3),activation='relu',input_shape=(32,32,3)),
layers.BatchNormalization(),
layers.MaxPooling2D((2,2)),
layers.Conv2D(64,(3,3),activation='relu'),
layers.BatchNormalization(),
layers.MaxPooling2D((2,2)),
layers.Conv2D(128,(3,3),activation='relu'),
layers.Dropout(0.5),
layers.Flatten(),
layers.Dense(128,activation='relu'),
layers.Dense(10,activation='softmax')
])

improved_model.compile(
optimizer='adam',
loss='sparse_categorical_crossentropy',
metrics=['accuracy']
)

improved_model.fit(x_train,y_train,epochs=10,validation_split=0.2)

# -------------------------------------------------
# SECTION 6 — DATA AUGMENTATION
# -------------------------------------------------

datagen = ImageDataGenerator(
rotation_range=20,
horizontal_flip=True,
zoom_range=0.2
)

datagen.fit(x_train)

model.fit(
datagen.flow(x_train,y_train,batch_size=64),
epochs=5,
validation_data=(x_test,y_test)
)

# -------------------------------------------------
# SECTION 7 — TRANSFER LEARNING
# -------------------------------------------------

base_model = MobileNet(
weights='imagenet',
include_top=False,
input_shape=(32,32,3)
)

for layer in base_model.layers:
    layer.trainable=False

x = layers.Flatten()(base_model.output)
x = layers.Dense(128,activation='relu')(x)
output = layers.Dense(10,activation='softmax')(x)

transfer_model = models.Model(base_model.input,output)

transfer_model.compile(
optimizer='adam',
loss='sparse_categorical_crossentropy',
metrics=['accuracy']
)

transfer_model.fit(x_train,y_train,epochs=5)

# -------------------------------------------------
# SECTION 8 — HYPERPARAMETER OPTIMIZATION
# -------------------------------------------------

learning_rates = [0.01,0.001,0.0001]

for lr in learning_rates:
    model = create_cnn()
    opt = tf.keras.optimizers.Adam(learning_rate=lr)
    model.compile(optimizer=opt,loss='sparse_categorical_crossentropy',metrics=['accuracy'])
    print("Training with learning rate:",lr)
    model.fit(x_train,y_train,epochs=2,batch_size=64)

# -------------------------------------------------
# SECTION 9 — MODEL DEPLOYMENT
# -------------------------------------------------

# Save model
model.save("cnn_image_classifier.h5")

print("Model saved successfully")

# Load model
loaded_model = load_model("cnn_image_classifier.h5")

print("Model loaded successfully")

# Simple prediction function
def predict_image(path):
    img = cv2.imread(path)
    img = cv2.resize(img,(32,32))
    img = img/255.0
    img = np.expand_dims(img,axis=0)

    pred = loaded_model.predict(img)
    label = class_names[np.argmax(pred)]

    plt.imshow(cv2.cvtColor(img[0],cv2.COLOR_BGR2RGB))
    plt.title("Predicted: "+label)
    plt.axis('off')
    plt.show()

# Example usage
# predict_image("test_image.jpg")