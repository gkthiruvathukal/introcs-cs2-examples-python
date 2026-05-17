from collections import deque


class DequeDemo:
    def __init__(self):
        """Initialize an empty deque"""
        self.dq = deque()

    def add_to_front(self, item):
        """Add an item to the front of the deque"""
        self.dq.appendleft(item)

    def add_to_back(self, item):
        """Add an item to the back of the deque"""
        self.dq.append(item)

    def remove_from_front(self):
        """Remove and return the item from the front"""
        if self.dq:
            return self.dq.popleft()
        raise IndexError("Cannot remove from empty deque")

    def remove_from_back(self):
        """Remove and return the item from the back"""
        if self.dq:
            return self.dq.pop()
        raise IndexError("Cannot remove from empty deque")

    def peek_front(self):
        """Retrieve the item at the front without removing it"""
        if self.dq:
            return self.dq[0]
        raise IndexError("Deque is empty")

    def peek_back(self):
        """Retrieve the item at the back without removing it"""
        if self.dq:
            return self.dq[-1]
        raise IndexError("Deque is empty")

    def update_front(self, new_item):
        """Update the item at the front"""
        if self.dq:
            self.dq[0] = new_item
        else:
            raise IndexError("Cannot update empty deque")

    def update_back(self, new_item):
        """Update the item at the back"""
        if self.dq:
            self.dq[-1] = new_item
        else:
            raise IndexError("Cannot update empty deque")

    def size(self):
        """Return the size of the deque"""
        return len(self.dq)

    def clear(self):
        """Remove all items from the deque."""
        self.dq.clear()

    def at(self, index):
        """Return the value at zero-based offset from the front."""
        if index < 0 or index >= len(self.dq):
            raise IndexError("Index out of range")
        return self.dq[index]

    def to_list(self):
        """Return the deque contents from front to back."""
        return list(self.dq)
    
