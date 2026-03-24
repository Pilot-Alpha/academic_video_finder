import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from alg import find_video

# 1. Update paths to look outside the backend folder
# We tell Flask the frontend is in the sibling directory
app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)

@app.route('/get_video', methods=['POST'])
def get_video():
    data = request.get_json(silent=True) or {}
    grade = "Class 9 10 SSC" if data.get('grade') == "SSC" else "Class 11 12 HSC"
    
    # Ensure find_video knows where the 'data' folder is
    videos = jsonify(find_video(grade, data.get('subject'), data.get('chapter'), data.get('videoType')))
    return videos

# 2. Add the route to serve the Frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # If the file exists in the frontend folder, serve it (JS, CSS, Images)
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # Otherwise, serve index.html (handles React/Vue routing)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    # Railway provides the PORT environment variable
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
