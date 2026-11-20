
class AVLNode:
    def __init__(self, student):
        self.student = student
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        return node.height if node else 0

    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def update_height(self, node):
        node.height = 1 + max(
            self.height(node.left),
            self.height(node.right)
        )

    def rotate_right(self, y):
        x = y.left
        temp = x.right

        x.right = y
        y.left = temp

        self.update_height(y)
        self.update_height(x)

        return x

    def rotate_left(self, x):
        y = x.right
        temp = y.left

        y.left = x
        x.right = temp

        self.update_height(x)
        self.update_height(y)

        return y

    def insert_node(self, node, student):
        if not node:
            return AVLNode(student)

        if student.student_id < node.student.student_id:
            node.left = self.insert_node(node.left, student)
        elif student.student_id > node.student.student_id:
            node.right = self.insert_node(node.right, student)
        else:
            return node

        self.update_height(node)
        b = self.balance(node)

        if b > 1 and student.student_id < node.left.student.student_id:
            return self.rotate_right(node)

        if b < -1 and student.student_id > node.right.student.student_id:
            return self.rotate_left(node)

        if b > 1 and student.student_id > node.left.student.student_id:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if b < -1 and student.student_id < node.right.student.student_id:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def search_node(self, node, student_id):
        if not node or node.student.student_id == student_id:
            return node

        if student_id < node.student.student_id:
            return self.search_node(node.left, student_id)

        return self.search_node(node.right, student_id)

    def minimum(self, node):
        while node.left:
            node = node.left
        return node

    def delete_node(self, node, student_id):
        if not node:
            return None

        if student_id < node.student.student_id:
            node.left = self.delete_node(node.left, student_id)

        elif student_id > node.student.student_id:
            node.right = self.delete_node(node.right, student_id)

        else:
            if not node.left:
                return node.right

            if not node.right:
                return node.left

            temp = self.minimum(node.right)
            node.student = temp.student
            node.right = self.delete_node(
                node.right, temp.student.student_id
            )

        self.update_height(node)
        b = self.balance(node)

        if b > 1 and self.balance(node.left) >= 0:
            return self.rotate_right(node)

        if b > 1 and self.balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if b < -1 and self.balance(node.right) <= 0:
            return self.rotate_left(node)

        if b < -1 and self.balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def insert(self, student):
        if self.search(student.student_id):
            return False

        self.root = self.insert_node(self.root, student)
        return True

    def search(self, student_id):
        node = self.search_node(self.root, student_id)
        return node.student if node else None

    def delete(self, student_id):
        if not self.search(student_id):
            return False

        self.root = self.delete_node(self.root, student_id)
        return True

    def get_all(self, node=None, records=None):
        if records is None:
            records = []
            node = self.root

        if node:
            self.get_all(node.left, records)
            records.append(node.student)
            self.get_all(node.right, records)

        return records

    def range_search(self, low, high):
        return [
            s for s in self.get_all()
            if low <= s.student_id <= high
        ]

    def top_cgpa(self):
        return [s for s in self.get_all() if s.cgpa > 9.0]

    def filter_department(self, department):
        return [
            s for s in self.get_all()
            if s.department.lower() == department.lower()
        ]

    def display_all(self):
        records = self.get_all()

        if not records:
            print("No student records found.")
            return

        for student in records:
            student.display()
