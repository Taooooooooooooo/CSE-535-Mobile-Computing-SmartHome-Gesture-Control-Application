from datetime import datetime
import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp4'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def unique_filename(filename):
    base, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return secure_filename(f"{base}_{timestamp}{ext}")

@app.route('/upload/', methods=['POST'])
def upload_file():
    try:
        my_files = request.files

        if not my_files:
            return jsonify({'error': 'No files received'}), 400

        for item in my_files:
            uploaded_file = my_files.get(item)

            if uploaded_file.filename == '':
                return jsonify({'error': 'No selected file'}), 400

            if uploaded_file and allowed_file(uploaded_file.filename):
                unique_name = unique_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
                return jsonify({'message': 'File uploaded successfully'}), 200
            else:
                return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        traceback_str = traceback.format_exc()
        error_message = f"An error occurred: {str(e)}\n\n{traceback_str}"
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
