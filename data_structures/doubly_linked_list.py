class Node:
    def __init__(self, data=None, node_id=None):
        self.data = data
        self.node_id = node_id
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0
        self._next_node_id = 1

    def insert(self, data, node_id=None):
        """Insert a node at the end of the list."""
        if node_id is None:
            node_id = self._next_node_id
            self._next_node_id += 1
        else:
            self._next_node_id = max(self._next_node_id, node_id + 1)
        new_node = Node(data, node_id=node_id)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def _unlink(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        self._size -= 1

    def _node_at(self, index):
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range for list of size {self._size}")
        current = self.head
        for _ in range(index):
            current = current.next
        return current

    def _insert_before_node(self, node, data, node_id=None):
        if node_id is None:
            node_id = self._next_node_id
            self._next_node_id += 1
        else:
            self._next_node_id = max(self._next_node_id, node_id + 1)
        new_node = Node(data, node_id=node_id)
        new_node.next = node
        new_node.prev = node.prev
        if node.prev:
            node.prev.next = new_node
        else:
            self.head = new_node
        node.prev = new_node
        self._size += 1

    def remove(self, data):
        """Remove the first node with the given value."""
        current = self.head
        while current:
            if current.data == data:
                self._unlink(current)
                return
            current = current.next
        raise ValueError("Value not found in the list")

    def remove_at(self, index):
        """Remove the node at position index (0-based from head)."""
        self._unlink(self._node_at(index))

    def remove_by_node_id(self, node_id):
        """Remove the node with the given node_id."""
        current = self.head
        while current:
            if current.node_id == node_id:
                self._unlink(current)
                return
            current = current.next
        raise ValueError(f"No node with id {node_id}")

    def insert_at(self, index, data, node_id=None):
        """Insert data before the node at position index (0 = new head, size = new tail)."""
        if index < 0 or index > self._size:
            raise IndexError(f"Insert index {index} out of range for list of size {self._size}")
        if index == self._size:
            self.insert(data, node_id=node_id)
        else:
            self._insert_before_node(self._node_at(index), data, node_id=node_id)

    def insert_after(self, node_id, data, new_node_id=None):
        """Insert data immediately after the node with the given node_id."""
        current = self.head
        while current:
            if current.node_id == node_id:
                if current is self.tail:
                    self.insert(data, node_id=new_node_id)
                else:
                    self._insert_before_node(current.next, data, node_id=new_node_id)
                return
            current = current.next
        raise ValueError(f"No node with id {node_id}")

    def insert_before(self, node_id, data, new_node_id=None):
        """Insert data immediately before the node with the given node_id."""
        current = self.head
        while current:
            if current.node_id == node_id:
                self._insert_before_node(current, data, node_id=new_node_id)
                return
            current = current.next
        raise ValueError(f"No node with id {node_id}")

    def search(self, data):
        """Return True if data is found, False otherwise."""
        return self.find(data) is not None

    def find(self, data):
        """Return (index, node_id) for the first matching node, or None if not found."""
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return (index, current.node_id)
            current = current.next
            index += 1
        return None

    def size(self):
        """Return the size of the list."""
        return self._size

    def display_forward(self):
        """Display all nodes in the list from head to tail."""
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

    def display_backward(self):
        """Display all nodes in the list from tail to head."""
        elements = []
        current = self.tail
        while current:
            elements.append(current.data)
            current = current.prev
        return elements

    def clear(self):
        """Remove all nodes from the list."""
        self.head = None
        self.tail = None
        self._size = 0
        self._next_node_id = 1

    def to_list(self):
        """Return all node values from head to tail."""
        return self.display_forward()

    def node_snapshots(self):
        """Return stable node metadata from head to tail."""
        snapshots = []
        current = self.head
        while current:
            snapshots.append(
                {
                    "node_id": current.node_id,
                    "node_label": f"node-{current.node_id}",
                    "data": current.data,
                    "prev_label": f"node-{current.prev.node_id}" if current.prev else "/",
                    "next_label": f"node-{current.next.node_id}" if current.next else "/",
                }
            )
            current = current.next
        return snapshots

    def restore_from_snapshots(self, snapshots):
        """Restore the list contents and node ids from snapshots."""
        self.clear()
        for snapshot in snapshots:
            self.insert(snapshot["data"], node_id=snapshot["node_id"])
    
