from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

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
def view_students():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    connection.close()

    return render_template("students.html", students=students)

#----------------- DELETE STUDENT ----------------
@app.route("/delete/<int:id>")
def delete_student(id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    connection.commit()
    connection.close()

    return redirect("/students")

#----------------- UPDATE STUDENT ----------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
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
# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)