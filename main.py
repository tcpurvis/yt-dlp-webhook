from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def home():
    return "yt-dlp webhook is live!"

@app.route('/extract', methods=['POST'])
def extract():
    video_url = request.json.get("url")
    try:
        meta_proc = subprocess.run(
            ["yt-dlp", "--list-subs", "-J", video_url],
            capture_output=True, text=True
        )
        print("STDERR:", meta_proc.stderr)
        print("STDOUT:", meta_proc.stdout)

        if not meta_proc.stdout.strip():
            raise ValueError("yt-dlp returned no output")

        meta = json.loads(meta_proc.stdout)
        title = meta.get("title", "No title")
        subs = list(meta.get("subtitles", {}).keys())

        format_proc = subprocess.run(
            ["yt-dlp", "-F", video_url],
            capture_output=True, text=True
        )
        audio_lines = format_proc.stdout.splitlines()
        audio_tracks = list({
            line.split()[0] for line in audio_lines if "audio only" in line
        })

        return jsonify({
            "url": video_url,
            "title": title,
            "subtitles": subs,
            "audioTracks": audio_tracks
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
