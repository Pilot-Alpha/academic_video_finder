from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
from alg import find_video
import os



app = Flask(__name__)
CORS(app)

@app.route('/get_video', methods=['POST'])
def get_video():
    data = request.get_json(silent=True) or {}

    grade = data.get('grade')
    subject = data.get('subject')
    chapter = data.get('chapter')
    video_type = data.get('videoType')

    if grade == "SSC":
        grade = "Class 9 10 SSC"
    else:
        grade = "Class 11 12 HSC"

    videos = jsonify(find_video(grade, subject, chapter, video_type))

    return videos


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))