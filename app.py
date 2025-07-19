from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from process import run_mosaic
from werkzeug.utils import secure_filename
import uuid


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files')
    for file in files:
        if file.filename.endswith(('.tif', '.TIF')):
            # Secure the filename to avoid Windows issues
            filename = secure_filename(file.filename)

            # Optionally add a UUID to avoid name clashes
            unique_name = f"{uuid.uuid4().hex}_{filename}"
            file.save(os.path.join(UPLOAD_FOLDER, unique_name))
    run_mosaic(UPLOAD_FOLDER)
    return render_template('result.html')

@app.route('/download')
def download_file():
    return send_file("static/output.tif", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5501)
