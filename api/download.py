import yt_dlp
import tempfile
from flask import Flask, request, jsonify

def handler(request):
    data = request.get_json()
    url = data.get("url")
    
    try:
        # Download to a temp folder
        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {"outtmpl": f"{tmpdir}/%(title)s.%(ext)s", "format": "mp4"}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        return jsonify({"message": "✅ Download complete!"})
    except Exception as e:
        return jsonify({"message": f"❌ Error: {str(e)}"})
