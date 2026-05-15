from collections import deque


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTreeDemo:
    def __init__(self):
        """Initialize an empty binary search tree."""
        self.root = None
        self._size = 0

    def insert(self, data):
        """Insert a value into the tree."""
        if self.root is None:
            self.root = TreeNode(data)
            self._size += 1
            return

        current = self.root
        while True:
            if data < current.data:
                if current.left is None:
                    current.left = TreeNode(data)
                    self._size += 1
                    return
                current = current.left
            elif data > current.data:
                if current.right is None:
                    current.right = TreeNode(data)
                    self._size += 1
                    return
                current = current.right
            else:
                return

    def search(self, data):
        """Return True if the value exists in the tree."""
        current = self.root
        while current:
            if data == current.data:
                return True
            if data < current.data:
                current = current.left
            else:
                current = current.right
        return False

    def find_min(self):
        """Return the smallest value in the tree."""
        if self.root is None:
            raise ValueError("Cannot find minimum of an empty tree")

        current = self.root
        while current.left:
            current = current.left
        return current.data

    def find_max(self):
        """Return the largest value in the tree."""
        if self.root is None:
            raise ValueError("Cannot find maximum of an empty tree")

        current = self.root
        while current.right:
            current = current.right
        return current.data

    def inorder(self):
        """Return values in left-root-right order."""
        values = []

        def traverse(node):
            if node:
                traverse(node.left)
                values.append(node.data)
                traverse(node.right)

        traverse(self.root)
        return values

    def inorder_iterative(self):
        """Return inorder traversal using an explicit stack."""
        values = []
        stack = []
        current = self.root

        while stack or current:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            values.append(current.data)
            current = current.right

        return values

    def preorder(self):
        """Return values in root-left-right order."""
        values = []

        def traverse(node):
            if node:
                values.append(node.data)
                traverse(node.left)
                traverse(node.right)

        traverse(self.root)
        return values

    def preorder_iterative(self):
        """Return preorder traversal using an explicit stack."""
        if self.root is None:
            return []

        values = []
        stack = [self.root]
        while stack:
            node = stack.pop()
            values.append(node.data)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return values

    def postorder(self):
        """Return values in left-right-root order."""
        values = []

        def traverse(node):
            if node:
                traverse(node.left)
                traverse(node.right)
                values.append(node.data)

        traverse(self.root)
        return values

    def postorder_iterative(self):
        """Return postorder traversal using an explicit stack."""
        if self.root is None:
            return []

        values = []
        stack = [(self.root, False)]
        while stack:
            node, visited = stack.pop()
            if visited:
                values.append(node.data)
            else:
                stack.append((node, True))
                if node.right:
                    stack.append((node.right, False))
                if node.left:
                    stack.append((node.left, False))

        return values

    def level_order(self):
        """Return values one level at a time from left to right."""
        if self.root is None:
            return []

        values = []
        nodes = deque([self.root])
        while nodes:
            node = nodes.popleft()
            values.append(node.data)
            if node.left:
                nodes.append(node.left)
            if node.right:
                nodes.append(node.right)
        return values

    def height(self):
        """Return the number of nodes on the longest root-to-leaf path."""
        def node_height(node):
            if node is None:
                return 0
            return 1 + max(node_height(node.left), node_height(node.right))

        return node_height(self.root)

    def height_iterative(self):
        """Return tree height using an explicit stack."""
        if self.root is None:
            return 0

        max_height = 0
        stack = [(self.root, 1)]
        while stack:
            node, height = stack.pop()
            max_height = max(max_height, height)
            if node.left:
                stack.append((node.left, height + 1))
            if node.right:
                stack.append((node.right, height + 1))

        return max_height

    def size(self):
        """Return the number of values in the tree."""
        return self._size
