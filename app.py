import os
from flask import Flask, request, render_template_string, redirect, url_for, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Konfigurasi Upload
UPLOAD_FOLDER = "static/videos"
ALLOWED_EXTENSIONS = {"mp4", "avi", "mov", "mkv"}
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

# Pastikan folder upload tersedia
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_video():
    if request.method == "POST":
        if "file" not in request.files:
            return "Tidak ada file yang dipilih"
        
        file = request.files["file"]
        
        if file.filename == "":
            return "Nama file kosong"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            return redirect(url_for("show_videos"))

    return render_template_string(UPLOAD_HTML)

@app.route("/videos")
def show_videos():
    videos = os.listdir(UPLOAD_FOLDER)
    return render_template_string(VIDEOS_HTML, videos=videos)

# Tangani error jika file terlalu besar
@app.errorhandler(413)
def request_entity_too_large(error):
    return "File terlalu besar! Maksimal 2GB.", 413

# Template HTML dalam variabel string
UPLOAD_HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Video</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        <h2>Upload Video (Maksimal 2GB)</h2>
        <form action="/" method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept="video/*" required>
            <button type="submit">Upload</button>
        </form>
        <br>
        <a href="{{ url_for('show_videos') }}">Lihat Video yang Diupload</a>
    </div>
</body>
</html>
"""


VIDEOS_HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daftar Video</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        <h2>Daftar Video</h2>
        <div class="video-grid">
            {% for video in videos %}
                <div class="video-card">
                    <video controls>
                        <source src="{{ url_for('static', filename='videos/' + video) }}" type="video/mp4">
                        Browser Anda tidak mendukung tag video.
                    </video>
                    <p>{{ video }}</p>
                </div>
            {% endfor %}
        </div>
        <br>
        <a href="{{ url_for('upload_video') }}">Upload Video Lagi</a>
    </div>
</body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True)
