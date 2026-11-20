
import matplotlib.pyplot as plt


def show_avl(root, ax):
    ax.set_title("AVL Tree")

    positions = {}
    edges = []
    counter = [0]

    def layout(node, depth=0):
        if not node:
            return

        layout(node.left, depth + 1)

        x = counter[0]
        counter[0] += 1

        key = node.student.student_id
        positions[key] = (x, -depth)

        if node.left:
            edges.append((key, node.left.student.student_id))

        if node.right:
            edges.append((key, node.right.student.student_id))

        layout(node.right, depth + 1)

    layout(root)

    if not positions:
        ax.text(0.5, 0.5, "Empty Tree", ha="center")
        ax.axis("off")
        return

    for parent, child in edges:
        x1, y1 = positions[parent]
        x2, y2 = positions[child]
        ax.plot([x1, x2], [y1, y2])

    for key, (x, y) in positions.items():
        ax.text(
            x, y, str(key),
            ha="center", va="center",
            bbox=dict(boxstyle="circle", fc="white", ec="black")
        )

    ax.axis("off")


def show_bplus(root, ax):
    ax.set_title("B+ Tree")

    positions = {}
    edges = []
    leaves = []

    def layout(node, depth=0):
        if node.leaf:
            x = len(leaves) * 2
            leaves.append(node)
            positions[id(node)] = (
                x, -depth,
                ",".join(str(s.student_id) for s in node.records)
            )
            return x

        child_positions = []

        for child in node.children:
            child_x = layout(child, depth + 1)
            child_positions.append(child_x)
            edges.append((id(node), id(child)))

        x = sum(child_positions) / len(child_positions)

        positions[id(node)] = (
            x, -depth,
            ",".join(map(str, node.keys))
        )

        return x

    layout(root)

    for parent, child in edges:
        x1, y1, _ = positions[parent]
        x2, y2, _ = positions[child]
        ax.plot([x1, x2], [y1, y2])

    for node_id, (x, y, label) in positions.items():
        ax.text(
            x, y, label,
            ha="center", va="center",
            bbox=dict(boxstyle="round", fc="white", ec="black")
        )

    for i in range(len(leaves) - 1):
        x1, y1, _ = positions[id(leaves[i])]
        x2, y2, _ = positions[id(leaves[i + 1])]

        ax.annotate(
            "",
            xy=(x2 - 0.3, y2 - 0.3),
            xytext=(x1 + 0.3, y1 - 0.3),
            arrowprops=dict(arrowstyle="->")
        )

    ax.axis("off")


def show_trees(avl, bplus):
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    show_avl(avl.root, axes[0])
    show_bplus(bplus.root, axes[1])

    plt.tight_layout()
    plt.savefig("tree_visualization.png")
    plt.show()

    print("Tree visualization saved successfully.")
