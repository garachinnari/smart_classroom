print("APP STARTED")

from flask import Flask, render_template, request
from datetime import datetime
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    students_present = int(request.form.get("students", 30))

    total_students = 60
    students_absent = total_students - students_present

    light_intensity = 40

    if students_present > 0 and light_intensity < 50:
        light_status = "ON"
    else:
        light_status = "OFF"

    if students_present == 0:
        suggestion = "Classroom empty. Switch OFF lights to save energy."
    else:
        suggestion = "Classroom active. Lights are controlled automatically."

    # Save attendance record
    with open("attendance.txt", "a") as file:
        file.write(f"Time: {datetime.now()}\n")
        file.write(f"Students Present: {students_present}\n")
        file.write(f"Students Absent: {students_absent}\n")
        file.write(f"Light Status: {light_status}\n")
        file.write("--------------------\n")

    # Read attendance history
    with open("attendance.txt", "r") as file:
        attendance_log = file.read()

    return render_template(
        "index.html",
        light_status=light_status,
        students_present=students_present,
        students_absent=students_absent,
        suggestion=suggestion,
        attendance_log=attendance_log
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
