from flask import Flask, render_template, request
from datetime import datetime
import os

app = Flask(__name__)

students = []
attendance = []


@app.route("/", methods=["GET", "POST"])
def home():

    global students, attendance

    if request.method == "POST":

        # Add student
        if request.form.get("action") == "add":

            roll = request.form.get("roll_no")
            name = request.form.get("student_name")

            if roll and name:
                students.append({
                    "roll": roll,
                    "name": name
                })


        # Delete student
        if request.form.get("action") == "delete":

            index = int(request.form.get("index"))
            students.pop(index)



        # Save attendance
        if request.form.get("action") == "attendance":

            attendance.clear()

            for i, student in enumerate(students):

                status = request.form.get(f"status_{i}")

                if status:
                    attendance.append({
                        "roll": student["roll"],
                        "name": student["name"],
                        "status": status
                    })



    total_students = len(students)

    present = len(
        [a for a in attendance if a["status"] == "Present"]
    )

    absent = len(
        [a for a in attendance if a["status"] == "Absent"]
    )


    if present > 0:
        light_status = "ON 💡"
        suggestion = "Students are present. Classroom is active."
    else:
        light_status = "OFF 🌙"
        suggestion = "No students detected. Save energy by switching OFF lights."


    return render_template(
        "index.html",
        students=students,
        attendance=attendance,
        total_students=total_students,
        students_present=present,
        students_absent=absent,
        light_status=light_status,
        suggestion=suggestion,
        time=datetime.now()
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
