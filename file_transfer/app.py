import os
import zipfile
import secrets
from flask import Flask, request, jsonify, render_template, send_file

app = Flask(__name__)


def generate_token(length=16):
    token = secrets.token_hex(length)
    return token


@app.route("/", methods=["GET", "POST"])
def transfer():
    if request.method == "GET":
        return render_template("index.html")
    else:
        title = request.form["title"]
        username = request.form["username"]
        files = request.files.getlist("files")

        token = generate_token()
        os.mkdir(f"uploads/{token}")
        for file in files:
            file.save(f"uploads/{token}/{file.filename}")
        with open(f"uploads/{token}/info.json", "w") as f:
            f.write(f'{{"title": "{title}", "username": "{username}"}}')

        print(request.url_root)
        url = f"{request.url_root}download/{token}"
        return render_template("success.html", title=title, url=url)
        return jsonify({"success": True, "token": token}), 200


@app.route("/download/<token>", methods=["GET"])
def download(token):
    if os.path.exists(f"uploads/{token}"):
        with open(f"uploads/{token}/info.json", "r") as f:
            data = eval(f.read())

            title = data["title"]
            username = data["username"]

        files = os.listdir(f"uploads/{token}")
        for file in files:
            if file == "info.json":
                files.remove(file)

        return render_template(
            "download.html", username=username, title=title, token=token, files=files
        )
    else:
        return "The token is not valid"


@app.route("/download/<token>/zip", methods=["GET"])
def download_zip(token):
    if os.path.exists(f"uploads/{token}"):
        zipf = zipfile.ZipFile(f"uploads/{token}.zip", "w", zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(f"uploads/{token}/"):
            for file in files:
                if file != "info.json":
                    zipf.write(os.path.join(root, file), arcname=file)
        zipf.close()

        return send_file(f"uploads/{token}.zip", as_attachment=True)
    else:
        return jsonify({"success": False}), 404


if __name__ == "__main__":
    app.run(debug=True)
