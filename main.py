from flask import Flask, request, jsonify
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "yt-dlp webhook is live!"

@app.route('/extract', methods=['POST'])
def extract():
    try:
        # Log incoming headers and body for debugging
        print("Headers:", dict(request.headers))
        print("Raw data:", request.data)
        print("request.json:", request.json)

        # Force Flask to parse JSON
        data = request.get_json(force=True)
        print("Parsed JSON:", data)

        # Extract URL from JSON payload
        video_url = data.get("url")

        # Respond with the URL for now (debugging)
        return jsonify({"received_url": video_url})

    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500

# Required for Render to run your app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
