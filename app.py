from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from pytubefix import YouTube  # YouTubeライブラリ
from time import sleep

app = Flask(__name__)

# ダウンロード先のフォルダー
download_folder = os.path.join(os.getcwd(), "downloads")
os.makedirs(download_folder, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download_video():
    url = request.form.get("url")
    quality = request.form.get("quality")  # 画質を取得
    audio_only = request.form.get("audio_only") == "true"  # 音声のみかどうかを取得

    if not url:
        return jsonify({"error": "URLが提供されていません"}), 400

    try:
        po_token = "MnSbccdpy_I1yZtJ_h7BO4fiM1a8tGMi5QVwyO8ymw94S5MvCSTWJLUjorNZ708DB9jOBCslMDr0yfDaTr5QWIc2EMBvwgz6KexXnatFpMBULgMCFcrAUcT-PzeXA4H8rpQ1UhSxw1kRNP1d4k0BgeqzADducA=="
        visitor_data = "Cgt1YXpNSDM1anBpSSj6gbW5BjIKCgJKUBIEGgAgKA%3D%3D"
        yt = YouTube(url,use_po_token=True)
        yt.set_po_token(po_token, visitor_data)

        if audio_only:
            stream = yt.streams.filter(only_audio=True).first()
        else:
            stream = yt.streams.filter(progressive=True, file_extension="mp4", res=quality).first()

        if not stream:
            return jsonify({"error": "選択した画質または音声の形式が利用できません"}), 404

        file_path = stream.download(output_path=download_folder)
        return jsonify({"status": "complete", "file_path": os.path.basename(file_path)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/delete", methods=["POST"])
def delete_video():
    files = os.listdir(download_folder)
    if not files:
        return jsonify({"message": "No files to delete."})

    latest_file = max([os.path.join(download_folder, f) for f in files], key=os.path.getctime)
    
    try:
        sleep(3)
        os.remove(latest_file)
        return redirect(url_for("index"))
    except PermissionError as e:
        return jsonify({"error": f"ファイルの削除に失敗しました: {e}"}), 500


@app.route("/downloads/<filename>")
def serve_video(filename):
    return redirect(url_for('static', filename=f'downloads/{filename}'))


if __name__ == "__main__":
    app.run(debug=True)
