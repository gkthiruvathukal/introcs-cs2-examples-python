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

    def remove(self, data):
        """Remove a node by value."""
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                self._size -= 1
                return
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
    
