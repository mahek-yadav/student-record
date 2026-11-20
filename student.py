
class Student:
    def __init__(self, student_id, name, department,
                 semester, cgpa, city):

        self.student_id = int(student_id)
        self.name = name
        self.department = department
        self.semester = int(semester)
        self.cgpa = float(cgpa)
        self.city = city

    def display(self):
        print("-" * 40)
        print("Student ID:", self.student_id)
        print("Name:", self.name)
        print("Department:", self.department)
        print("Semester:", self.semester)
        print("CGPA:", self.cgpa)
        print("City:", self.city)
        print("-" * 40)
