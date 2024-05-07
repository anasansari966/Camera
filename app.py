from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import os
import numpy as np

app = Flask(__name__)

# Access the camera
camera = cv2.VideoCapture(0)

# Initialize a counter for unique filenames
capture_counter = 0

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    while True:
        success, frame = camera.read()  # Read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    global capture_counter  # Access the global counter variable
    _, frame = camera.read()  # Capture frame from camera
    # Generate a unique filename with a counter appended
    filename = f'static/capture_{capture_counter}.jpg'
    cv2.imwrite(filename, frame)  # Save the captured frame
    capture_counter += 1  # Increment the counter for the next capture
    return render_template('capture.html', filename=filename)

@app.route('/retake', methods=['POST'])
def retake():
    global capture_counter
    capture_counter -= 1  # Decrement the counter to prevent skipping numbers
    return redirect(url_for('index'))

@app.route('/save', methods=['POST'])
def save():
    # You can handle saving the images here if needed
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
