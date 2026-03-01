from flask import Flask
import pymysql

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="student_user",
        password="student123",
        database="student_db"
    )

@app.route("/")
def home():
    return "Student Management System Running 🚀"

@app.route("/test-db")
def test_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    connection.close()
    return f"Database Connected: {result}"

if __name__ == "__main__":
    app.run(debug=True)