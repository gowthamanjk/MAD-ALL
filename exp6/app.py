from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import pytesseract

# Initialize Flask app
app = Flask(__name__)
CORS(app)


# Replace 'sign.h5' with the path to your model
model = load_model('roadsign.h5')

# OCR function using pytesseract
def perform_ocr(image):
    text = pytesseract.image_to_string(image)
    return text.strip()

@app.route('/process-image', methods=['POST'])
def process_image():
    # Check if an image is uploaded
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Resize or preprocess the image if needed
    image_resized = cv2.resize(image, (224, 224))
    image_array = np.expand_dims(image_resized, axis=0) / 255.0
    
    # Predict with the model
    predictions = model.predict(image_array)
    predicted_label = np.argmax(predictions, axis=1)[0]
    
    # Perform OCR to extract text from the sign
    ocr_text = perform_ocr(image)
    
    return jsonify({'label': int(predicted_label), 'text': ocr_text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
