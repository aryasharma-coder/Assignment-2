# server.py
from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string
import os
from datetime import datetime

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder='uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

INDEX_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Screenshots</title>
  <meta http-equiv="refresh" content="30"> <!-- refresh every 30s -->
  <style> body { font-family: Arial; padding: 20px; } img { max-width: 100%; margin-bottom: 20px; border:1px solid #ccc; } </style>
</head>
<body>
  <h1>Uploaded Screenshots (auto-refresh every 30s)</h1>
  {% for f in files %}
    <div>
      <time>{{ f.timestamp }}</time><br>
      <img src="{{ url_for('uploaded_file', filename=f.name) }}" alt="{{ f.name }}">
    </div>
  {% else %}
    <p>No screenshots yet.</p>
  {% endfor %}
</body>
</html>
"""

@app.route('/')
def index():
    files = []
    for name in sorted(os.listdir(app.config['UPLOAD_FOLDER']), reverse=True):
        path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        ts = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
        files.append({'name': name, 'timestamp': ts})
    return render_template_string(INDEX_HTML, files=files)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload():
    # Expecting "file" field
    if 'file' not in request.files:
        return 'No file part', 400
    f = request.files['file']
    if f.filename == '':
        return 'No selected file', 400
    # Save with timestamp to avoid name collisions
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    filename = f"{timestamp}_{secure_filename(f.filename)}"
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(path)
    return 'OK', 200

def secure_filename(name):
    # simple safe filename fallback
    return "".join(c for c in name if c.isalnum() or c in '._-').strip()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
