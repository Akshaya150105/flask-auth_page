from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
from app.utils.file_processor import allowed_file, process_eob_file

upload = Blueprint('upload', __name__)

@upload.route('/api/upload_eob', methods=['GET', 'POST'])
@login_required
def upload_eob():
    if request.method == 'POST':
        file = request.files.get('file')
        
        if not file or file.filename == '':
            return jsonify({"error": "No file selected!"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file format! Only CSV and JSON are allowed."}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the file to extract preview
        file_extension = filename.rsplit('.', 1)[1].lower()
        file_summary = process_eob_file(file_path, file_extension)

        if "error" in file_summary:
            return jsonify({"error": file_summary["error"]}), 500

        return jsonify({"message": "File uploaded successfully", "preview": file_summary})

    return render_template('upload_eob.html')

@upload.route('/api/list_eob_files', methods=['GET'])
@login_required
def list_eob_files():
    files = []
    for filename in os.listdir(current_app.config['UPLOAD_FOLDER']):
        if allowed_file(filename):
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            files.append({
                'filename': filename,
                'size': os.path.getsize(file_path),
                'uploaded_at': os.path.getctime(file_path)
            })
    
    return jsonify({'files': files}), 200