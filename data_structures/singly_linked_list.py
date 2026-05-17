class Node:
    def __init__(self, data=None, node_id=None):
        self.data = data
        self.node_id = node_id
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None
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
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def remove(self, data):
        """Remove a node by value."""
        current = self.head
        previous = None
        while current:
            if current.data == data:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                self._size -= 1
                return
            previous = current
            current = current.next
        raise ValueError("Value not found in the list")

    def search(self, data):
        """Search for a node by value."""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def size(self):
        """Return the size of the list."""
        return self._size

    def display(self):
        """Display all nodes in the list."""
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

    def clear(self):
        """Remove all nodes from the list."""
        self.head = None
        self._size = 0
        self._next_node_id = 1

    def to_list(self):
        """Return all node values from head to tail."""
        return self.display()

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
