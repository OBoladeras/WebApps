from database import Database
from security import PasswordEncryptor
from flask import Flask, render_template, jsonify, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route("/", methods=["GET", "POST"])
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            if request.form["post_type"] == "add_contact":
                username = request.form["username"]
                public_key = request.form["public_key"]

        else:
            return render_template(
                "index.html",
                username=session["username"],
                public_key=session["public_key"],
            )


@app.route("/login")
@app.route("/signup")
def login():
    error = session.pop("error", None)
    return render_template("login.html", error=error)


# Api Side
@app.route("/authentication/<typeA>", methods=["POST"])
def authentication(typeA):
    def answer(user_id, public_key):
        if user_id:
            session["user_id"] = user_id
            session["public_key"] = public_key
            return redirect(url_for("index"))
        else:
            session["error"] = ["Invalid username or password"]
            return redirect(url_for("login"))

    if "authentication" in request.url:
        if typeA == "login":
            username = request.form["username"]
            password = request.form["password"]

            user_id, public_key = Database().login(
                username, PasswordEncryptor().encrypt(password)
            )
            return answer(user_id, public_key)
        elif typeA == "signup":
            username = request.form["username"]
            password = request.form["password"]

            user_id, public_key = Database().signup(
                username, PasswordEncryptor().encrypt(password)
            )
            return answer(user_id, public_key)
        else:
            return render_template("login.html")


@app.route("/message", methods=["POST"])
def receive_message():
    try:
        data = request.get_json()
        name = data.get("name")
        message = data.get("message")

        print(f"Received message from {name}: {message}")

        return jsonify(
            {"status": "success", "message": "Message received successfully"}
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
