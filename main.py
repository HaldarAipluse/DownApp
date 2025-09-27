from flask import Flask, request, jsonify, render_template_string
import yt_dlp
import os

app = Flask(__name__)

# 📂 Download location (Android Download folder)
DOWNLOAD_PATH = "/storage/emulated/0/Download"

# 🔹 HTML, CSS, JS all inside Python
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Instagram Video Downloader</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #121212;
      color: #fff;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .card {
      background: #1e1e1e;
      padding: 20px;
      border-radius: 12px;
      text-align: center;
      width: 350px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    input {
      width: 90%;
      padding: 10px;
      border-radius: 8px;
      border: none;
      margin: 10px 0;
    }
    button {
      padding: 10px 20px;
      border: none;
      border-radius: 8px;
      background: #ff0069;
      color: white;
      cursor: pointer;
      font-weight: bold;
    }
    button:hover {
      background: #e6005c;
    }
    #status {
      margin-top: 15px;
      font-size: 14px;
      color: #00ff99;
    }
  </style>
</head>
<body>
  <div class="card">
    <h2>📥 Instagram Video Downloader</h2>
    <form id="downloadForm">
      <input type="text" id="url" placeholder="Paste Instagram URL" required>
      <button type="submit">Download</button>
    </form>
    <p id="status"></p>
  </div>

  <script>
    document.getElementById("downloadForm").addEventListener("submit", async function(e){
      e.preventDefault();
      let url = document.getElementById("url").value;
      document.getElementById("status").innerText = "Downloading...";
      
      let response = await fetch("/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
      });

      let result = await response.json();
      document.getElementById("status").innerText = result.message;
    });
  </script>
</body>
</html>
"""

# Route for frontend
@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

# Route for download
@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")

    try:
        ydl_opts = {
            "outtmpl": os.path.join(DOWNLOAD_PATH, "%(title)s.%(ext)s"),
            "format": "mp4"
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return jsonify({"message": "✅ Download complete! Check your Download folder."})
    except Exception as e:
        return jsonify({"message": f"❌ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)