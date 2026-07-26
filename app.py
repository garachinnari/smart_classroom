from flask import Flask, render_template, request
from datetime import datetime
import os

app = Flask(__name__)

STUDENT_FILE = "students.txt"
ATTENDANCE_FILE = "attendance.txt"
LOG_FILE = "attendance_log.txt"


# Load students
def load_students():
    if not os.path.exists(STUDENT_FILE):
        return []

    with open(STUDENT_FILE, "r") as file:
        return [line.strip() for line in file if line.strip()]


# Save students
def save_students(students):
    with open(STUDENT_FILE, "w") as file:
        for student in students:
            file.write(student + "\n")


# Load attendance
def load_attendance():
    if not os.path.exists(ATTENDANCE_FILE):
        return []

    with open(ATTENDANCE_FILE, "r") as file:
        return [line.strip() for line in file if line.strip()]


@app.route("/", methods=["GET", "POST"])
def home():

    students = load_students()

    if request.method == "POST":

        # Add Student
        if request.form.get("roll_no") and request.form.get("student_name"):

            roll = request.form.get("roll_no")
            name = request.form.get("student_name")

            student = roll + "," + name

            if student not in students:
                students.append(student)
                save_students(students)


        # Delete Student
        if request.form.get("delete_student"):

            student = request.form.get("delete_student")

            if student in students:
                students.remove(student)
                save_students(students)


        # Save Attendance
        if request.form.get("submit_attendance"):

            present_students = request.form.getlist("present")


            with open(ATTENDANCE_FILE, "w") as file:
                for student in present_students:
                    file.write(student + "\n")


            with open(LOG_FILE, "a") as file:
                file.write("\n-------------------\n")
                file.write(
                    "Date: " +
                    datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    + "\n"
                )

                file.write("Present Students:\n")

                for student in present_students:
                    file.write(student + "\n")


    students = load_students()
    attendance = load_attendance()


    total_students = len(students)

    students_present = len(attendance)

    students_absent = total_students - students_present


    # Smart Light

    if students_present > 0:
        light_status = "ON 💡"
    else:
        light_status = "OFF 🌙"



    # AI Suggestion

    if students_present > 0:
        suggestion = (
            "Students are present. "
            "Classroom environment is active."
        )
    else:
        suggestion = (
            "Classroom is empty. "
            "Save energy by switching OFF lights."
        )


    return render_template(
        "index.html",
        students=students,
        total_students=total_students,
        students_present=students_present,
        students_absent=students_absent,
        light_status=light_status,
        suggestion=suggestion
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
