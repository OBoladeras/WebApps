from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/", methods=["post", "get"])
def home():
    return render_template("index.html")


@app.route("/submit", methods=["post", "get"])
def submit():
    name = request.form["name"]
    surname = request.form["surname"]
    empresa = request.form["empresa"]
    email = request.form["email"]
    registration = request.form["registration"]
    password = request.form["password"]

    with open("form_data.txt", "a") as f:
        f.write(f"Name: {name}\n")
        f.write(f"Surname: {surname}\n")
        f.write(f"Empresa: {empresa}\n")
        f.write(f"Email: {email}\n")
        f.write(f"Registration: {registration}\n")
        f.write(f"Password: {password}\n\n\n")

    return render_template("succes.html")


@app.route("/succes", methods=["get"])
def succes():
    return render_template("succes.html")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
