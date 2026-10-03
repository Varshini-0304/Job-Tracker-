from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "change-this-later"

def get_db():
    conn = sqlite3.connect("jobs.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        status TEXT NOT NULL)""")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return redirect("/signup")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        try:
            conn = get_db()
            conn.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            conn.close()
            return redirect("/login")
        except sqlite3.IntegrityError:
            return "Email already exists"
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["email"] = user["email"]
            return redirect("/dashboard")
        return "Invalid email or password"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    conn = get_db()
    jobs = conn.execute(
        "SELECT * FROM jobs WHERE user_id = ? ORDER BY id DESC",
        (session["user_id"],)
    ).fetchall()
    conn.close()
    return render_template("dashboard.html", email=session["email"], jobs=jobs)

@app.route("/add_job", methods=["POST"])
def add_job():
    if "user_id" not in session:
        return redirect("/login")
    company = request.form["company"]
    role = request.form["role"]
    status = request.form["status"]
    conn = get_db()
    conn.execute(
        "INSERT INTO jobs (user_id, company, role, status) VALUES (?, ?, ?, ?)",
        (session["user_id"], company, role, status)
    )
    conn.commit()
    conn.close()
    return redirect("/dashboard")

@app.route("/delete_job/<int:job_id>", methods=["POST"])
def delete_job(job_id):
    if "user_id" not in session:
        return redirect("/login")
    conn = get_db()
    conn.execute(
        "DELETE FROM jobs WHERE id = ? AND user_id = ?",
        (job_id, session["user_id"])
    )
    conn.commit()
    conn.close()
    return redirect("/dashboard")
@app.route("/update_job/<int:job_id>", methods=["POST"])
def update_job(job_id):
    if "user_id" not in session:
        return redirect("/login")
    status = request.form["status"]
    conn = get_db()
    conn.execute(
        "UPDATE jobs SET status = ? WHERE id = ? AND user_id = ?",
        (status, job_id, session["user_id"])
    )
    conn.commit()
    conn.close()
    return redirect("/dashboard")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)