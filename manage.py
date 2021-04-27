from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask_bootstrap import Bootstrap

import sqlite3 as sql

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index/")
def index_page():
    return render_template("index.html")

@app.route("/user/<username>")
def user_page(username):
    if username== "admin":
        return "Welcome admin"
    else:
        return "Welcome exhibitor"


@app.route("/list")
def list_data():
    con =  sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM booths")

    rows = cur.fetchall()
    return render_template("list.html", rows = rows)


@app.route("/newbooth")
def new_booth():
    return render_template("newbooth.html")

@app.route("/addrec", methods=["POST"])
def addrec():
    if request.method == "POST":
        name = request.form["nm"]
        merch = request.form["merch"]
        days = request.form["days"]

        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO booths (name, merch, days) VALUES (?, ?, ?)", (name, merch, days,))
        con.commit()
        con =  sql.connect("database.db")

        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM booths")

        rows = cur.fetchall()

        return render_template("list.html", rows = rows)

@app.route("/showpng/")
def png_page():
    return render_template("showpng.html")

# def create_database():
#     conn = sql.connect("database.db")
#     conn.execute("CREATE TABLE booths (name TEXT, merch TEXT, days TEXT)")
#     conn.close()

# create_database()


if __name__ == '__main__':
    app.run(debug=True)