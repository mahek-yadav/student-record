
from student import Student
from avl_tree import AVLTree
from bplus_tree import BPlusTree
from file_handler import load_students, save_students

avl = AVLTree()
bplus = BPlusTree()


def load_data():
    students = load_students()

    for s in students:
        avl.insert(s)
        bplus.insert(s)

    print(len(students), "records loaded successfully.")


def insert_student():
    try:
        student_id = int(input("Student ID: "))
        name = input("Student Name: ")
        department = input("Department: ")
        semester = int(input("Semester: "))
        cgpa = float(input("CGPA: "))
        city = input("City: ")

        if semester < 1 or cgpa < 0 or cgpa > 10:
            print("Invalid semester or CGPA.")
            return

        if avl.search(student_id):
            print("Error: Duplicate Student ID!")
            return

        s = Student(
            student_id, name, department,
            semester, cgpa, city
        )

        avl.insert(s)
        bplus.insert(s)

        save_students(avl.get_all())
        print("Student inserted successfully.")

    except ValueError:
        print("Please enter valid numeric values.")


def search_student():
    try:
        student_id = int(input("Enter Student ID: "))

        print("\nAVL TREE RESULT:")
        result1 = avl.search(student_id)

        if result1:
            result1.display()
        else:
            print("Student not found.")

        print("\nB+ TREE RESULT:")
        result2 = bplus.search(student_id)

        if result2:
            result2.display()
        else:
            print("Student not found.")

    except ValueError:
        print("Invalid Student ID.")


def delete_student():
    try:
        student_id = int(input("Enter Student ID to delete: "))

        if not avl.search(student_id):
            print("Student not found.")
            return

        avl.delete(student_id)
        bplus.delete(student_id)

        save_students(avl.get_all())
        print("Student deleted successfully.")

    except ValueError:
        print("Invalid Student ID.")


def range_search():
    try:
        low = int(input("Enter starting ID: "))
        high = int(input("Enter ending ID: "))

        if low > high:
            print("Starting ID must be smaller than ending ID.")
            return

        print("\nAVL TREE RANGE RESULTS:")
        for s in avl.range_search(low, high):
            s.display()

        print("\nB+ TREE RANGE RESULTS:")
        for s in bplus.range_search(low, high):
            s.display()

    except ValueError:
        print("Invalid range.")


def display_students():
    print("\nAVL TREE SORTED RECORDS:")
    avl.display_all()

    print("\nB+ TREE SORTED RECORDS:")
    bplus.display_all()


def top_cgpa():
    print("\nSTUDENTS WITH CGPA GREATER THAN 9.0:")

    for s in avl.top_cgpa():
        s.display()


def department_filter():
    department = input("Enter department: ")

    print("\nAVL TREE RESULTS:")
    for s in avl.filter_department(department):
        s.display()

    print("\nB+ TREE RESULTS:")
    for s in bplus.filter_department(department):
        s.display()


def multiple_ranges():
    ranges = [
        (1000, 1500),
        (2500, 3000),
        (7000, 9000)
    ]

    for low, high in ranges:
        print(f"\nRange: {low} - {high}")

        results = bplus.range_search(low, high)

        if not results:
            print("No records found.")

        for s in results:
            s.display()


def main():
    load_data()

    while True:
        print("\n========== UNIVERSITY STUDENT RECORD SYSTEM ==========")
        print("1. Insert Student")
        print("2. Search Student")
        print("3. Delete Student")
        print("4. Range Search")
        print("5. Display Sorted Records")
        print("6. Top CGPA Students")
        print("7. Department Filtering")
        print("8. Multiple Range Queries")
        print("9. Performance Comparison")
        print("10. Tree Visualization")
        print("11. Automated Comparison")
        print("12. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            insert_student()

        elif choice == "2":
            search_student()

        elif choice == "3":
            delete_student()

        elif choice == "4":
            range_search()

        elif choice == "5":
            display_students()

        elif choice == "6":
            top_cgpa()

        elif choice == "7":
            department_filter()

        elif choice == "8":
            multiple_ranges()

        elif choice == "9":
            from performance import run_performance
            run_performance()

        elif choice == "10":
            from visualization import show_trees
            show_trees(avl, bplus)

        elif choice == "11":
            from performance import automated_comparison
            automated_comparison()

        elif choice == "12":
            save_students(avl.get_all())
            print("Exiting application.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
