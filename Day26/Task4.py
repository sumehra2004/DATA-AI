# CIFAR-10 Image Classification using CNN (Single Page Implementation)

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

print("TensorFlow Version:", tf.__version__)

# 1. Load Dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

# Class labels
class_names = ['airplane','automobile','bird','cat','deer',
               'dog','frog','horse','ship','truck']

# 2. Display Sample Images
plt.figure(figsize=(8,8))
for i in range(9):
    plt.subplot(3,3,i+1)
    plt.imshow(x_train[i])
    plt.title(class_names[y_train[i][0]])
    plt.axis('off')
plt.show()

# 3. Data Preprocessing (Normalization)
x_train = x_train / 255.0
x_test = x_test / 255.0

# 4. Build CNN Model
model = keras.Sequential([
    layers.Conv2D(32,(3,3),activation='relu',input_shape=(32,32,3)),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(64,(3,3),activation='relu'),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(64,(3,3),activation='relu'),
    layers.Flatten(),
    layers.Dense(64,activation='relu'),
    layers.Dense(10,activation='softmax')
])

model.summary()

# 5. Compile Model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 6. Train Model
history = model.fit(x_train, y_train,
                    epochs=10,
                    validation_data=(x_test, y_test))

# 7. Evaluate Model
test_loss, test_accuracy = model.evaluate(x_test, y_test)
print("Test Accuracy:", test_accuracy)

# 8. Plot Training Accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("Training vs Validation Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend(['Training','Validation'])
plt.show()

# 9. Make Prediction
predictions = model.predict(x_test)
index = 3
predicted_class = np.argmax(predictions[index])

plt.imshow(x_test[index])
plt.title("Predicted: " + class_names[predicted_class])
plt.axis('off')
plt.show()