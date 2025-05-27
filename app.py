from flask import Flask, Response, render_template
import cv2
import numpy as np
import threading
import time

app = Flask(__name__)

# Global variables for video streaming
output_frame = None
lock = threading.Lock()
background_captured = False
bg_frame = None

def generate_frames():
    global output_frame, lock, background_captured, bg_frame
    
    # Initialize webcam
    video = cv2.VideoCapture(0)
    time.sleep(2)
    
    # Capture static background frame
    if not background_captured:
        for _ in range(30):
            success, bg_frame = video.read()
        bg_frame = np.flip(bg_frame, axis=1)
        background_captured = True
    
    while True:
        success, frame = video.read()
        if not success:
            break
            
        # Flip the frame horizontally (mirror effect)
        frame = np.flip(frame, axis=1)
        
        # Convert BGR image to HSV color space
        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Slightly smoothen the image
        blurred_hsv = cv2.GaussianBlur(hsv_img, (35, 35), 0)
        
        # Lower red hue range
        red_lower_1 = np.array([0, 120, 70])
        red_upper_1 = np.array([10, 255, 255])
        mask_red1 = cv2.inRange(hsv_img, red_lower_1, red_upper_1)
        
        # Upper red hue range
        red_lower_2 = np.array([170, 120, 70])
        red_upper_2 = np.array([180, 255, 255])
        mask_red2 = cv2.inRange(hsv_img, red_lower_2, red_upper_2)
        
        # Combine both red masks
        full_mask = mask_red1 + mask_red2
        
        # Clean up noise from the mask
        full_mask = cv2.morphologyEx(
            full_mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        
        # Replace detected red areas with background
        frame[np.where(full_mask == 255)] = bg_frame[np.where(full_mask == 255)]
        
        # Encode the frame in JPEG format
        with lock:
            ret, buffer = cv2.imencode('.jpg', frame)
            output_frame = buffer.tobytes()
            
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + output_frame + b'\r\n')

@app.route('/')
def index():
    return """
    <html>
        <head>
            <title>Harry Potter's Invisibility Cloak</title>
            <style>
                body { 
                    background-color: #1a1a1a;
                    color: #ffffff;
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin: 0;
                    padding: 20px;
                }
                h1 { color: #ffd700; }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                }
                .video-container {
                    margin: 20px 0;
                    padding: 10px;
                    background-color: #333;
                    border-radius: 10px;
                }
                img {
                    max-width: 100%;
                    height: auto;
                    border-radius: 5px;
                }
                .instructions {
                    background-color: #333;
                    padding: 20px;
                    border-radius: 10px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Harry Potter's Invisibility Cloak</h1>
                <div class="video-container">
                    <img src="/video_feed">
                </div>
                <div class="instructions">
                    <h2>Instructions:</h2>
                    <p>1. Stand away from the camera for 5 seconds while it captures the background</p>
                    <p>2. Hold a red cloth in front of the camera</p>
                    <p>3. Watch as the red cloth becomes invisible, revealing the background!</p>
                </div>
            </div>
        </body>
    </html>
    """

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/health')
def health_check():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)