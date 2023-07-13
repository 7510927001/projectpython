from flask import Flask, render_template, request
import cv2
import os

app = Flask(__name__)

# Define the upload folder for storing video files
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Check if the 'video' file field is present in the request
    if 'video' not in request.files:
        return 'No video file uploaded'
    
    video_file = request.files['video']
    
    # Save the video file to the upload folder
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
    video_file.save(video_path)
    
    # Extract frames from the video
    frames_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'frames')
    os.makedirs(frames_folder, exist_ok=True)
    
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    
    while success:
        # Save frame as JPEG file
        frame_path = os.path.join(frames_folder, f'frame{count}.jpg')
        cv2.imwrite(frame_path, image)
        
        success, image = vidcap.read()
        count += 1
    
    # Get the list of frame filenames
    frame_files = sorted(os.listdir(frames_folder))
    
    return render_template('frames.html', frame_files=frame_files)

if __name__ == '__main__':
    app.run(debug=True)
