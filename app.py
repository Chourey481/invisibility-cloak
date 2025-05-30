from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.get_json()
    image_data = data['image'].split(',')[1]
    bg_data = data['background'].split(',')[1]

    # Decode current frame
    decoded = base64.b64decode(image_data)
    img_np = np.array(Image.open(BytesIO(decoded)))
    frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    frame = np.flip(frame, axis=1)

    # Decode background frame
    bg_decoded = base64.b64decode(bg_data)
    bg_np = np.array(Image.open(BytesIO(bg_decoded)))
    background = cv2.cvtColor(bg_np, cv2.COLOR_RGB2BGR)
    background = np.flip(background, axis=1)

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red color range
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 + mask2
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    # Replace red areas with background
    result = frame.copy()
    result[np.where(mask == 255)] = background[np.where(mask == 255)]

    _, buffer = cv2.imencode('.jpg', result)
    result_base64 = base64.b64encode(buffer).decode('utf-8')

    return jsonify({'processed_image': f"data:image/jpeg;base64,{result_base64}"})

@app.route('/health')
def health_check():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
