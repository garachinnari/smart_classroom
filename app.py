from flask import Flask, render_template, request
from datetime import datetime
import os

app = Flask(__name__)

STUDENT_FILE = "students.txt"
ATTENDANCE_FILE = "attendance.txt"


# Read students
def get_students():
    students = []

    if os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "r") as file:
            for line in file:
                data = line.strip().split("|")

                if len(data) == 2:
                    students.append({
                        "roll": data[0],
                        "name": data[1]
                    })

    return students



# Save students
def save_students(students):

    with open(STUDENT_FILE, "w") as file:

        for student in students:
            file.write(
                student["roll"] + "|" + student["name"] + "\n"
            )



@app.route("/", methods=["GET", "POST"])
def home():

    students = get_students()
    attendance = []


    if request.method == "POST":


        # Add Student

        if request.form.get("action") == "add":

            roll = request.form.get("roll")
            name = request.form.get("name")


            if roll and name:

                students.append({
                    "roll": roll,
                    "name": name
                })

                save_students(students)




        # Delete Student

        elif request.form.get("action") == "delete":

            index = int(request.form.get("index"))

            students.pop(index)

            save_students(students)




        # Save Attendance

        elif request.form.get("action") == "attendance":


            with open(ATTENDANCE_FILE, "w") as file:


                file.write(
                    "Date: "
                    + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    + "\n"
                )


                for i, student in enumerate(students):

                    status = request.form.get(
                        "status_" + str(i)
                    )


                    if status:

                        file.write(
                            student["roll"]
                            + "|"
                            + student["name"]
                            + "|"
                            + status
                            + "\n"
                        )




    # Read attendance log

    if os.path.exists(ATTENDANCE_FILE):

        with open(ATTENDANCE_FILE, "r") as file:

            attendance = file.readlines()



    present_count = 0
    absent_count = 0


    for line in attendance:

        if "|Present" in line:
            present_count += 1

        if "|Absent" in line:
            absent_count += 1



    total_students = len(students)



    # Smart Light

    if present_count > 0:

        light_status = "ON 💡"

        suggestion = (
            "Students detected. "
            "Classroom is active. "
            "Lights are ON."
        )

    else:

        light_status = "OFF 🌙"

        suggestion = (
            "No students detected. "
            "Save energy by switching OFF lights."
        )



    return render_template(

        "index.html",

        students=students,

        attendance=attendance,

        total_students=total_students,

        students_present=present_count,

        students_absent=absent_count,

        light_status=light_status,

        suggestion=suggestion

    )



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
