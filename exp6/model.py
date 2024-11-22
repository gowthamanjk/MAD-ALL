import numpy as np
import cv2
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical

# Function to preprocess the image (resize and normalize)
def preprocess_image(image_path, target_size=(64, 64)):
    img = cv2.imread(image_path)
    img = cv2.resize(img, target_size)
    img = img.astype('float32') / 255.0  # Normalize pixel values
    return img

# Function to load and preprocess dataset
def load_dataset(image_paths, labels, num_classes):
    images = np.array([preprocess_image(image_path) for image_path in image_paths])
    labels = to_categorical(labels, num_classes)
    return images, labels

# Build CNN Model for OCR
def build_model(input_shape, num_classes):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))  # Output layer for classification

    model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Define number of classes (you will need to adjust this for your dataset)
num_classes = 10  # For example, 10 classes of road signs
input_shape = (64, 64, 3)  # RGB image size 64x64

# Assuming the dataset is already available in a directory
# Update with your actual dataset directory
dataset_dir = "C:\Users\91638\OneDrive\Documents\dataset\jaffy\train_data"
image_paths = []
labels = []

# Loading dataset (update according to your dataset structure)
for label in range(num_classes):
    class_dir = os.path.join(dataset_dir, str(label))  # Assuming each class has a folder
    for image_name in os.listdir(class_dir):
        image_path = os.path.join(class_dir, image_name)
        image_paths.append(image_path)
        labels.append(label)

# Load the dataset
train_images, train_labels = load_dataset(image_paths, labels, num_classes)

# Train the model
model = build_model(input_shape, num_classes)
model.summary()

# Train the model
model.fit(train_images, train_labels, epochs=10, batch_size=32, validation_split=0.2)

# Save the trained model as sign.h5
model.save('sign.h5')

# Function to predict road sign (OCR)
def predict_road_sign(image_path):
    model = tf.keras.models.load_model('sign.h5')
    img = preprocess_image(image_path)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    prediction = model.predict(img)
    predicted_class = np.argmax(prediction)
    return predicted_class

# Example prediction (make sure to provide a valid image path)
image_path = 'path_to_test_sign_image.jpg'
predicted_class = predict_road_sign(image_path)
print(f'Predicted class: {predicted_class}')
