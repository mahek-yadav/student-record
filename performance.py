import time
import random
import csv
import matplotlib.pyplot as plt

from student import Student
from avl_tree import AVLTree
from bplus_tree import BPlusTree


def generate_students(n):
    students = []

    for i in range(n):
        students.append(
            Student(
                10000 + i,
                f"Student_{i}",
                random.choice(["CSE", "IT", "AIML"]),
                random.randint(1, 8),
                round(random.uniform(6, 10), 2),
                random.choice(["Mumbai", "Pune", "Delhi"])
            )
        )

    random.shuffle(students)
    return students


def build_trees(students):
    avl = AVLTree()
    bplus = BPlusTree()

    for s in students:
        avl.insert(s)
        bplus.insert(s)

    return avl, bplus


def measure_performance(n):
    students = generate_students(n)
    results = {}

    # Insertion
    avl = AVLTree()
    start = time.perf_counter()

    for s in students:
        avl.insert(s)

    results["AVL Insertion"] = time.perf_counter() - start

    bplus = BPlusTree()
    start = time.perf_counter()

    for s in students:
        bplus.insert(s)

    results["B+ Insertion"] = time.perf_counter() - start

    # Searching
    search_ids = [
        s.student_id for s in students[:min(100, n)]
    ]

    start = time.perf_counter()
    for sid in search_ids:
        avl.search(sid)
    results["AVL Searching"] = time.perf_counter() - start

    start = time.perf_counter()
    for sid in search_ids:
        bplus.search(sid)
    results["B+ Searching"] = time.perf_counter() - start

    # Range searching
    low = 10000 + n // 4
    high = 10000 + (3 * n // 4)

    start = time.perf_counter()
    avl.range_search(low, high)
    results["AVL Range"] = time.perf_counter() - start

    start = time.perf_counter()
    bplus.range_search(low, high)
    results["B+ Range"] = time.perf_counter() - start

    # Deletion: use separately built trees.
    avl_delete, bplus_delete = build_trees(students)

    delete_ids = [
        s.student_id for s in students[:min(20, n)]
    ]

    start = time.perf_counter()
    for sid in delete_ids:
        avl_delete.delete(sid)
    results["AVL Deletion"] = time.perf_counter() - start

    start = time.perf_counter()
    for sid in delete_ids:
        bplus_delete.delete(sid)
    results["B+ Deletion"] = time.perf_counter() - start

    return results


def run_performance():
    sizes = [100, 500, 1000, 5000, 10000]
    all_results = {}

    for n in sizes:
        print(f"\nTesting {n} students...")
        all_results[n] = measure_performance(n)

    # Save measurements to CSV.
    with open("performance_results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Dataset Size", "Operation", "Time (seconds)"])

        for n, results in all_results.items():
            for operation, value in results.items():
                writer.writerow([n, operation, value])

    operations = ["Insertion", "Searching", "Deletion", "Range"]

    for operation in operations:
        avl_values = [
            all_results[n][f"AVL {operation}"]
            for n in sizes
        ]

        bplus_values = [
            all_results[n][f"B+ {operation}"]
            for n in sizes
        ]

        plt.figure(figsize=(8, 5))

        plt.plot(sizes, avl_values, marker="o", label="AVL Tree")
        plt.plot(sizes, bplus_values, marker="o", label="B+ Tree")

        plt.xlabel("Number of Student Records")
        plt.ylabel("Execution Time (seconds)")
        plt.title(operation + " Time Comparison")
        plt.legend()
        plt.grid(True)

        filename = operation.lower() + "_comparison.png"
        plt.savefig(filename)
        plt.show()
        plt.close()

    print("\nPerformance testing completed.")
    print("Results saved in performance_results.csv")


def automated_comparison():
    print("\nAUTOMATED TREE COMPARISON")

    students = generate_students(1000)

    avl, bplus = build_trees(students)

    test_ids = [10000, 10200, 10500, 10999]

    passed = 0
    total = 0

    # Search comparison.
    for sid in test_ids:
        total += 1

        a = avl.search(sid)
        b = bplus.search(sid)

        if a and b and a.student_id == b.student_id:
            passed += 1
            print("Search test passed:", sid)
        else:
            print("Search test failed:", sid)

    # Range comparison.
    total += 1

    a = [s.student_id for s in avl.range_search(10100, 10300)]
    b = [s.student_id for s in bplus.range_search(10100, 10300)]

    if a == b:
        passed += 1
        print("Range search test passed.")
    else:
        print("Range search test failed.")

    # Deletion comparison.
    total += 1

    avl.delete(10000)
    bplus.delete(10000)

    if not avl.search(10000) and not bplus.search(10000):
        passed += 1
        print("Deletion test passed.")
    else:
        print("Deletion test failed.")

    # Duplicate detection.
    total += 1

    duplicate = students[1]

    if not avl.insert(duplicate) and not bplus.insert(duplicate):
        passed += 1
        print("Duplicate detection test passed.")
    else:
        print("Duplicate detection test failed.")

    with open("comparison_report.txt", "w") as file:
        file.write("AUTOMATED COMPARISON REPORT\n")
        file.write("===========================\n")
        file.write(f"Total tests: {total}\n")
        file.write(f"Passed tests: {passed}\n")
        file.write(f"Failed tests: {total - passed}\n")
        file.write(f"Success rate: {passed / total * 100:.2f}%\n")

    print("\nTotal tests:", total)
    print("Passed:", passed)
    print("Failed:", total - passed)
    print("Report saved in comparison_report.txt")
