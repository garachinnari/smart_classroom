from flask import Flask, render_template, request
import os

app = Flask(__name__)

STUDENTS_FILE = "students.txt"
ATTENDANCE_FILE = "attendance.txt"


def load_students():
    if not os.path.exists(STUDENTS_FILE):
        return []

    with open(STUDENTS_FILE, "r") as file:
        return [line.strip() for line in file if line.strip()]


def save_students(students):
    with open(STUDENTS_FILE, "w") as file:
        for student in students:
            file.write(student + "\n")


@app.route("/", methods=["GET", "POST"])
def home():

    students = load_students()

    if request.method == "POST":

        # Add Student
        if "roll_no" in request.form and "student_name" in request.form:
            roll = request.form["roll_no"].strip()
            name = request.form["student_name"].strip()

            if roll and name:
                student = f"{roll},{name}"
                if student not in students:
                    students.append(student)
                    save_students(students)

        # Delete Student
        if "delete_student" in request.form:
            student = request.form["delete_student"]

            if student in students:
                students.remove(student)
                save_students(students)

        # Submit Attendance
        if request.form.get("submit_attendance") == "yes":

            present = request.form.getlist("present")

            with open(ATTENDANCE_FILE, "w") as file:
                for student in present:
                    file.write(student + "\n")

    students = load_students()

    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "r") as file:
            attendance = [line.strip() for line in file if line.strip()]
    else:
        attendance = []

    total_students = len(students)
    students_present = len(attendance)
    students_absent = total_students - students_present

    if students_present > 0:
        light_status = "ON"
        suggestion = "Students are present. Classroom lights are ON."
    else:
        light_status = "OFF"
        suggestion = "No students detected. Turn OFF classroom lights to save energy."

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
    app.run(debug=True)
