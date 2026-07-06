from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

VIDEO_FOLDER = "downloads/video"
AUDIO_FOLDER = "downloads/audio"

os.makedirs(VIDEO_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route("/download", methods=["POST"])
def download_video():
    url = request.json.get("url")

    if not url:
        return jsonify({"error": "URL não enviada"}), 400

    try:
        # baixar mp4
        ydl_opts_video = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{VIDEO_FOLDER}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            info = ydl.extract_info(url, download=True)

        # baixar mp3
        ydl_opts_audio = {
            'format': 'bestaudio/best',
            'outtmpl': f'{AUDIO_FOLDER}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
            ydl.download([url])

        return jsonify({
            "status": "download completo",
            "title": info["title"]
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(port=5000)