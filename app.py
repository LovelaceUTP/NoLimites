import os
from functools import wraps
# import base64
# from PIL import Image
# from io import BytesIO
from cs50 import SQL
from flask import (Flask, redirect, render_template, request, session)
from flask_session import Session

horario = ""
remuneracion = ""
modalidad = ""
experiencia = ""
sector = ""

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///registros.db")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
# @login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/pregunta1", methods=["GET", "POST"])
def p1():
    if request.method == "POST":
        horario = request.form.get("horario")

    return render_template("p1index.html")

@app.route("/pregunta2", methods=["GET", "POST"])
def p2():
    return render_template("p2index.html")

@app.route("/pregunta3", methods=["GET", "POST"])
def p3():
    if request.method == "POST":
        remuneracion = request.form.get("remuneracion")

    return render_template("p3index.html")

@app.route("/pregunta4", methods=["GET", "POST"])
def p4():
    if request.method == "POST":
        modalidad = request.form.get("modalidad")

    return render_template("p4index.html")

@app.p5("/pregunta5", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        experiencia = request.form.get("experiencia")

    return render_template("p5index.html")

@app.route("/pregunta6", methods=["GET", "POST"])
def p6():

    return render_template("p7index.html")

@app.route("/pregunta7", methods=["GET", "POST"])
def p7():

    return render_template("p8index.html")

@app.route("/pregunta8", methods=["GET", "POST"])
def p8():
    if request.method == "POST":
        sector = request.form.get("sector")

    return render_template("p9index.html")

@app.route("/pregunta9", methods=["GET", "POST"])
def p9():

    return render_template("p10index.html")


@app.route("/pregunta10", methods=["GET", "POST"])
def p10():

    return render_template("p11index.html")



@app.route("/logout")
def logout():
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)