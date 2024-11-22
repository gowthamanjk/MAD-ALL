import os
import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
import tensorflow as tf
from io import BytesIO
from tensorflow.keras.preprocessing.image import img_to_array

app = Flask(__name__)

# Load pre-trained deep learning model (replace with your model)
model = tf.keras.models.load_model('model.h5')  # Replace 'model.h5' with your model path

# Define a function to preprocess the image before feeding it to the model
def preprocess_image(image):
    image = image.resize((224, 224))  # Resize to the input size expected by the model
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = image / 255.0  # Normalize the image
    return image

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        img = Image.open(BytesIO(file.read()))
        img = preprocess_image(img)

        # Make a prediction using the model
        prediction = model.predict(img)
        predicted_class = np.argmax(prediction)  # Assuming a classification model
        return jsonify({"prediction": str(predicted_class)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
