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

    message = f"You chose chapter {chapter} of subject {subject} of class {grade}"

    return jsonify({'message':message})

if __name__ == '__main__':
    app.run(debug=True)