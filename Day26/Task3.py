# Handwritten Digit Recognition using CNN (MNIST)

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

# 1. Load Dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# 2. Preprocess Data
x_train = x_train/255.0
x_test = x_test/255.0
x_train = x_train.reshape(-1,28,28,1)
x_test = x_test.reshape(-1,28,28,1)

# 3. Build CNN Model
model = keras.Sequential([
    layers.Conv2D(32,(3,3),activation='relu',input_shape=(28,28,1)),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(64,(3,3),activation='relu'),
    layers.MaxPooling2D((2,2)),
    layers.Flatten(),
    layers.Dense(128,activation='relu'),
    layers.Dense(10,activation='softmax')
])

# 4. Compile Model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 5. Train Model
model.fit(x_train, y_train, epochs=5, validation_data=(x_test,y_test))

# 6. Evaluate Model
loss, accuracy = model.evaluate(x_test, y_test)
print("Test Accuracy:", accuracy)

# 7. Predict Sample Digit
predictions = model.predict(x_test)
index = 5
predicted_digit = np.argmax(predictions[index])

# 8. Display Result
plt.imshow(x_test[index].reshape(28,28), cmap='gray')
plt.title("Predicted Digit: " + str(predicted_digit))
plt.axis('off')
plt.show()