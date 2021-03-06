# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 01:55:24 2021

@author: subha
"""

#Import necessary libraries
from flask import Flask, render_template, Response
import cv2
#Initialize the Flask app
import Live_ASL
app = Flask(__name__)
camera = cv2.VideoCapture(0)

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/',methods=['POST', 'GET'])
def index():
    return render_template('index.html')

# @app.route('/')
# def run_script():
#     file = open(r'C:/Users/subha/OneDrive/Desktop/asl/Live_ASL', 'r').read()
#     return exec(file)


@app.route('/')
def dynamic_page():
    return Live_ASL()

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run()