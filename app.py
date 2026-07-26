from flask import Flask, render_template, request
from datetime import datetime
import os

app = Flask(__name__)

STUDENTS_FILE = "students.txt"
ATTENDANCE_FILE = "attendance.txt"
LOG_FILE = "attendance_log.txt"


# Read students
def get_students():
    if not os.path.exists(STUDENTS_FILE):
        return []

    with open(STUDENTS_FILE, "r") as file:
        return [line.strip() for line in file if line.strip()]


# Save students
def save_students(students):
    with open(STUDENTS_FILE, "w") as file:
        for student in students:
            file.write(student + "\n")


# Read today's attendance
def get_attendance():
    if not os.path.exists(ATTENDANCE_FILE):
        return []

    with open(ATTENDANCE_FILE, "r") as file:
        return [line.strip() for line in file if line.strip()]


@app.route("/", methods=["GET", "POST"])
def home():

    students = get_students()

    if request.method == "POST":

        # Add Student
        if "add_student" in request.form:

            roll_no = request.form.get("roll_no")
            name = request.form.get("student_name")

            if roll_no and name:
                student = f"{roll_no},{name}"

                if student not in students:
                    students.append(student)
                    save_students(students)


        # Delete Student
        if "delete_student" in request.form:

            delete = request.form.get("delete_student")

            if delete in students:
                students.remove(delete)
                save_students(students)


        # Submit Attendance
        if "submit_attendance" in request.form:

            present_students = request.form.getlist("present")


            with open(ATTENDANCE_FILE, "w") as file:
                for student in present_students:
                    file.write(student + "\n")


            # Save Log
            with open(LOG_FILE, "a") as file:
                file.write("\nDate: ")
                file.write(
                    datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                )

                file.write("\nPresent Students:\n")

                for student in present_students:
                    file.write(student + "\n")



    students = get_students()

    attendance = get_attendance()


    total_students = len(students)

    students_present = len(attendance)

    students_absent = total_students - students_present



    # Smart Light Logic

    if students_present > 0:
        light_status = "ON 💡"
    else:
        light_status = "OFF 🌙"



    # AI Suggestion

    if students_present > 0:

        suggestion = (
            "Students are detected. "
            "Keep lights ON and monitor classroom."
        )

    else:

        suggestion = (
            "Classroom is empty. "
            "Turn OFF lights to save energy."
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
