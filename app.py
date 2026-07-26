print("APP STARTED")

from flask import Flask, render_template, request
from datetime import datetime
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    # Add Student
    roll_no = request.form.get("roll_no")
    student_name = request.form.get("student_name")

    if roll_no and student_name:
        with open("students.txt", "a") as file:
            file.write(f"{roll_no},{student_name}\n")


    # Delete Student
    delete_student = request.form.get("delete_student")

    if delete_student:

        if os.path.exists("students.txt"):

            with open("students.txt", "r") as file:
                students = file.read().splitlines()

            students = [
                student for student in students
                if student != delete_student
            ]

            with open("students.txt", "w") as file:
                for student in students:
                    file.write(student + "\n")



    # Read Students
    if os.path.exists("students.txt"):

        with open("students.txt", "r") as file:
            students = file.read().splitlines()

    else:
        students = []



    # Attendance Checkbox Data

    present_students = request.form.getlist("present")

    absent_students = request.form.getlist("absent")



    total_students = len(students)

    students_present = len(present_students)

    students_absent = len(absent_students)



    # Light Automation

    light_intensity = 40

    if students_present > 0 and light_intensity < 50:
        light_status = "ON"

    else:
        light_status = "OFF"



    # AI Suggestion

    if students_present == 0:

        suggestion = "Classroom empty. Switch OFF lights to save energy."

    else:

        suggestion = "Classroom active. Lights are controlled automatically."




    # Save Attendance Log

    if request.form.get("submit_attendance"):

        with open("attendance.txt", "a") as file:

            file.write("\nDate & Time: ")
            file.write(str(datetime.now()))

            file.write("\nPresent Students: ")
            file.write(", ".join(present_students))

            file.write("\nAbsent Students: ")
            file.write(", ".join(absent_students))

            file.write("\nLight Status: ")
            file.write(light_status)

            file.write("\n----------------------")



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

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
