from flask import Flask, render_template, request
from datetime import datetime
import os

app = Flask(__name__)

STUDENT_FILE = "students.txt"
ATTENDANCE_FILE = "attendance.txt"
LOG_FILE = "attendance_log.txt"


# Load Students
def load_students():
    if not os.path.exists(STUDENT_FILE):
        return []

    with open(STUDENT_FILE, "r") as file:
        return [line.strip() for line in file if line.strip()]


# Save Students
def save_students(students):
    with open(STUDENT_FILE, "w") as file:
        for student in students:
            file.write(student + "\n")


# Load Attendance
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

        if "roll_no" in request.form and "student_name" in request.form:

            roll = request.form["roll_no"]
            name = request.form["student_name"]

            student = roll + "," + name

            if student not in students:
                students.append(student)
                save_students(students)



        # Delete Student

        if "delete_student" in request.form:

            student = request.form["delete_student"]

            if student in students:
                students.remove(student)
                save_students(students)




        # Save Attendance

        if request.form.get("submit_attendance"):

            attendance_data = []


            for key, value in request.form.items():

                if key.startswith("attendance_"):

                    attendance_data.append(value)



            with open(ATTENDANCE_FILE, "w") as file:

                for data in attendance_data:
                    file.write(data + "\n")



            # Attendance Log

            with open(LOG_FILE, "a") as file:

                file.write("\n--------------------\n")

                file.write(
                    "Date: "
                    + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    + "\n"
                )

                for data in attendance_data:
                    file.write(data + "\n")




    students = load_students()

    attendance = load_attendance()



    total_students = len(students)


    present_students = [
        a for a in attendance
        if a.startswith("present_")
    ]


    absent_students = [
        a for a in attendance
        if a.startswith("absent_")
    ]



    students_present = len(present_students)

    students_absent = len(absent_students)



    # Smart Light

    if students_present > 0:
        light_status = "ON 💡"
    else:
        light_status = "OFF 🌙"



    # AI Suggestion

    if students_present > 0:

        suggestion = (
            "Students are present. "
            "Classroom is active and lights are ON."
        )

    else:

        suggestion = (
            "No students detected. "
            "Save electricity by switching OFF lights."
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
