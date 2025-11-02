
import io
import logging
import socketserver
from http import server
from threading import Condition

from flask import Flask, Response, render_template_string

# Asynchronous camera library for Raspberry Pi
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

# HTML template for the web page
PAGE = """
<html>
<head>
    <title>Raspberry Pi - Live Video Stream</title>
</head>
<body>
<center><h1>Raspberry Pi - Live Video Stream</h1></center>
<center><img src="{{ url_for('video_feed') }}" width="1920" height="1080"></center>
</body>
</html>
"""

class StreamingOutput(io.BufferedIOBase):
    """
    Output buffer for the camera frames. This class is thread-safe.
    """
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

app = Flask(__name__)
output = StreamingOutput()

def generate_frames():
    """Generator function that yields camera frames."""
    while True:
        with output.condition:
            output.condition.wait()
            frame = output.frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template_string(PAGE)

@app.route('/video_feed')
def video_feed():
    """The video streaming route."""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Initialize the camera
    picam2 = Picamera2()
    config = picam2.create_video_configuration(main={"size": (1920, 1080)})
    picam2.configure(config)
    
    # Start recording to the streaming output
    picam2.start_recording(JpegEncoder(), FileOutput(output))
    
    print("Streaming server started. Open http://<RASPBERRY_PI_IP>:5000 in your browser.")
    # Run the Flask app
    # Host '0.0.0.0' makes it accessible on the network
    app.run(host='0.0.0.0', port=5000, threaded=True)

