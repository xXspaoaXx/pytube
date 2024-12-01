import os
from flask import Flask, render_template, request, url_for
from pytubefix import YouTube

app = Flask(__name__, static_folder="/tmp", static_url_path="/static")

DOWNLOAD_FOLDER = "/tmp"  # 一時ディレクトリに保存

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download_video():
    url = request.form.get("url")
    try:
        # YouTubeから動画をダウンロード
        yt = YouTube(url, use_po_token=True)
        stream = yt.streams.get_highest_resolution()
        filepath = stream.download(DOWNLOAD_FOLDER)

        # ダウンロードしたファイル名を取得
        filename = os.path.basename(filepath)

        # HTMLから参照可能なURLを生成
        video_url = url_for('static', filename=f'tmp/{filename}')

        return render_template('index.html', video_url=video_url)

    except Exception as e:
        return f"<h3>Error: {e}</h3>"

if __name__ == "__main__":
    app.run(debug=True)
