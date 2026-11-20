import csv
from student import Student

FILE_NAME = "students.csv"


def load_students():
    students = []

    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Handle spaces and different header formats
                row = {
                    key.strip().lower().replace(" ", "").replace("_", ""): value
                    for key, value in row.items()
                    if key is not None
                }

                student = Student(
                    int(row["studentid"]),
                    row["name"],
                    row["department"],
                    int(row["semester"]),
                    float(row["cgpa"]),
                    row["city"]
                )

                students.append(student)

    except FileNotFoundError:
        print("CSV file not found. Starting with empty records.")

    except (KeyError, ValueError) as e:
        print("Error reading CSV file:", e)

    return students


def save_students(students):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        fields = [
            "StudentID", "Name", "Department",
            "Semester", "CGPA", "City"
        ]

        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for s in students:
            writer.writerow({
                "StudentID": s.student_id,
                "Name": s.name,
                "Department": s.department,
                "Semester": s.semester,
                "CGPA": s.cgpa,
                "City": s.city
            })

    print("Student records saved successfully.")
