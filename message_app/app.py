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

                if Database().insert_contact(username, public_key, session["user_id"]):
                    return redirect(url_for("index"))
                else:
                    session["share_error"] = ["Invalid username or public key"]
                    return redirect(url_for("index"))
        else:
            return render_template(
                "index.html",
                username=session["username"],
                public_key=session["public_key"],
                share_error=session.pop("share_error", None),
                contacts=Database().select_contacts(session["user_id"]),
            )


@app.route("/login")
@app.route("/signup")
def login():
    error = session.pop("error", None)
    return render_template("login.html", error=error)


# Api Side
@app.route("/authentication/<typeA>", methods=["POST"])
def authentication(typeA):
    def answer(user_id, username, public_key):
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["public_key"] = public_key
            return redirect(url_for("index"))
        else:
            session["error"] = ["Invalid username or password"]
            return redirect(url_for("login"))

    if "authentication" in request.url:
        if typeA == "login":
            email = request.form["email"]
            password = request.form["password"]

            user_id, public_key, username = Database().login(
                email, PasswordEncryptor().encrypt(password)
            )
            return answer(user_id, username, public_key)
        elif typeA == "signup":
            email = request.form["email"]
            username = request.form["username"]
            password = request.form["password"]

            user_id, public_key, username = Database().signup(
                email, username, PasswordEncryptor().encrypt(password)
            )
            return answer(user_id, username, public_key)
        else:
            return render_template("login.html")


@app.route("/message/<contact_id>", methods=["POST"])
def loadChat(contact_id=None):
    if contact_id:
        return Database().select_messages_chat(contact_id, session["user_id"])


@app.route("/message", methods=["POST"])
def receive_message():
    try:
        data = request.get_json()
        message = data.get("message")
        sender_id = data.get("senderID")
        receiver_id = data.get("receiverID")

        return jsonify({"success": True})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Invalid data format"}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
