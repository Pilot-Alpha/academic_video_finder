from flask import Flask, request, jsonify
from flask_cors import CORS



app = Flask(__name__)
CORS(app=app)

@app.route('/get_video', methods=['POST'])
def get_video():
    data = request.json

    grade = data.get('grade')
    subject = data.get('subject')
    chapter = data.get('chapter')
    video_type = data.get('videoType')

    if grade == "9_10":
        grade = "Class 9 10 SSC"
    else:
        grade = "Class 11 12 HSC"


    

if __name__ == '__main__':
    app.run(debug=True)