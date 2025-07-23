from flask import Flask, request, jsonify
import subprocess
import json
import os


# force redeploy

app = Flask(__name__)

@app.route('/')
def home():
    return "yt-dlp webhook is live!"

@app.route('/extract', methods=['POST'])
def extract():
    try:
        print("Headers:", dict(request.headers))
        print("Raw data:", request.data)
        print("request.json:", request.json)

        data = request.get_json(force=True)
        print("Parsed JSON:", data)

        if not data or "url" not in data:
            raise ValueError("Missing or invalid 'url' in request body")

        video_url = data["url"]
        print("Processing:", video_url)

        # Get video metadata with subtitles
        meta_proc = subprocess.run(
            ["yt-dlp", "--cookies", "cookies.txt", "--list-subs", "-J", video_url]
            capture_output=True, text=True
        )
        print("Meta STDERR:", meta_proc.stderr)
        print("Meta STDOUT:", meta_proc.stdout)

        if not meta_proc.stdout.strip():
            raise ValueError("yt-dlp returned no JSON")

        meta = json.loads(meta_proc.stdout)
        title = meta.get("title", "No title")
        subs = list(meta.get("subtitles", {}).keys())

        # Get available audio formats
        format_proc = subprocess.run(
            ["yt-dlp", "-F", video_url],
            capture_output=True, text=True
        )
        audio_lines = format_proc.stdout.splitlines()
        audio_tracks = list({
            line.split()[0]
            for line in audio_lines if "audio only" in line
        })

        return jsonify({
            "url": video_url,
            "title": title,
            "subtitles": subs,
            "audioTracks": audio_tracks
        })

    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500


# Required for Render to run your app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
