
class BPlusNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []
        self.next = None
        self.records = []


class BPlusTree:
    def __init__(self, order=4):
        self.root = BPlusNode(leaf=True)
        self.order = order

    def search(self, student_id):
        node = self.root

        while not node.leaf:
            i = 0
            while i < len(node.keys) and student_id >= node.keys[i]:
                i += 1
            node = node.children[i]

        for student in node.records:
            if student.student_id == student_id:
                return student

        return None

    def insert(self, student):
        if self.search(student.student_id):
            return False

        split = self._insert(self.root, student)

        if split:
            key, right_node = split

            new_root = BPlusNode()
            new_root.keys = [key]
            new_root.children = [self.root, right_node]

            self.root = new_root

        return True

    def _insert(self, node, student):
        if node.leaf:
            i = 0

            while i < len(node.records) and \
                    node.records[i].student_id < student.student_id:
                i += 1

            node.records.insert(i, student)

            if len(node.records) > self.order - 1:
                mid = len(node.records) // 2

                right = BPlusNode(leaf=True)
                right.records = node.records[mid:]
                node.records = node.records[:mid]

                right.next = node.next
                node.next = right

                return right.records[0].student_id, right

            return None

        i = 0
        while i < len(node.keys) and student.student_id >= node.keys[i]:
            i += 1

        split = self._insert(node.children[i], student)

        if split:
            key, right = split
            node.keys.insert(i, key)
            node.children.insert(i + 1, right)

        if len(node.children) > self.order:
            mid = len(node.children) // 2

            right = BPlusNode()
            right.children = node.children[mid:]
            node.children = node.children[:mid]

            node.keys = [
                self.first_key(child)
                for child in node.children[1:]
            ]

            right.keys = [
                self.first_key(child)
                for child in right.children[1:]
            ]

            return self.first_key(right.children[0]), right

        return None

    def first_key(self, node):
        while not node.leaf:
            node = node.children[0]

        return node.records[0].student_id

    def find_leaf(self, student_id):
        node = self.root

        while not node.leaf:
            i = 0
            while i < len(node.keys) and student_id >= node.keys[i]:
                i += 1

            node = node.children[i]

        return node

    def get_all(self):
        node = self.root

        while not node.leaf:
            node = node.children[0]

        records = []

        while node:
            records.extend(node.records)
            node = node.next

        return records

    def range_search(self, low, high):
        if low > high:
            return []

        node = self.find_leaf(low)
        results = []

        while node:
            for student in node.records:
                if low <= student.student_id <= high:
                    results.append(student)

                if student.student_id > high:
                    return results

            node = node.next

        return results

    def delete(self, student_id):
        records = self.get_all()

        remaining = [
            s for s in records
            if s.student_id != student_id
        ]

        if len(remaining) == len(records):
            return False

        # Rebuild the tree from the remaining records.
        self.root = BPlusNode(leaf=True)

        for student in remaining:
            self.insert(student)

        return True

    def display_all(self):
        records = self.get_all()

        if not records:
            print("No student records found.")
            return

        for student in records:
            student.display()

    def top_cgpa(self):
        return [
            s for s in self.get_all()
            if s.cgpa > 9.0
        ]

    def filter_department(self, department):
        return [
            s for s in self.get_all()
            if s.department.lower() == department.lower()
        ]

    def get_node_structure(self):
        result = []

        def visit(node, depth=0):
            result.append({
                "keys": list(node.keys),
                "leaf": node.leaf,
                "depth": depth,
                "records": [
                    s.student_id for s in node.records
                ]
            })

            for child in node.children:
                visit(child, depth + 1)

        visit(self.root)
        return result
