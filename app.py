from flask import Flask, render_template, request, redirect
from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

app = Flask(__name__)
app.secret_key = "supersecretkey"


def get_connection():
    return pymysql.connect(
        host="localhost",
        user="student_user",
        password="student123",
        database="student_db"
    )

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "Student Management System Running 🚀"


# ---------------- DB TEST ----------------
@app.route("/test-db")
def test_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    connection.close()
    return f"Database Connected: {result}"


# ---------------- ADD STUDENT ----------------
@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if "admin" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]

        connection = get_connection()
        cursor = connection.cursor()

        sql = "INSERT INTO students (name, email, course) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, email, course))

        connection.commit()
        connection.close()

        return redirect("/add-student")

    return render_template("add_student.html")

#----------------- VIEW STUDENTS ----------------
@app.route("/students")
def students():
    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    connection.close()

    return render_template("students.html", students=data)
#----------------- DELETE STUDENT ----------------
@app.route("/delete/<int:id>")
def delete_student(id):
    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    connection.commit()
    connection.close()

    return redirect("/students")

#----------------- UPDATE STUDENT ----------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]

        cursor.execute(
            "UPDATE students SET name=%s, email=%s, course=%s WHERE id=%s",
            (name, email, course, id)
        )
        connection.commit()
        connection.close()
        return redirect("/students")

    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    connection.close()

    return render_template("edit_student.html", student=student)

#----------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM admins WHERE username=%s", (username,))
        admin = cursor.fetchone()
        connection.close()

        if admin and check_password_hash(admin[2], password):
            session["admin"] = username
            return redirect("/students")
        else:
            return "Invalid credentials"

    return render_template("login.html")

#----------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)