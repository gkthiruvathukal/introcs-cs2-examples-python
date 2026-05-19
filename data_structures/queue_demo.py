from collections import deque


class QueueDemo:
    def __init__(self):
        """Initialize an empty queue using deque."""
        self.queue = deque()

    def enqueue(self, item):
        """Add an item to the back of the queue."""
        self.queue.append(item)

    def dequeue(self):
        """Remove and return the item from the front of the queue."""
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        return self.queue.popleft()

    def peek(self):
        """Get the front item of the queue without removing it."""
        if self.is_empty():
            raise IndexError("Peek from an empty queue")
        return self.queue[0]

    def is_empty(self):
        """Return True if the queue is empty, otherwise False."""
        return len(self.queue) == 0

    def size(self):
        """Return the size of the queue."""
        return len(self.queue)

    def clear(self):
        """Remove all items from the queue."""
        self.queue.clear()

    def swap(self):
        """Swap the front two items in the queue."""
        if len(self.queue) < 2:
            raise IndexError("Swap requires at least two items")
        first = self.queue[0]
        second = self.queue[1]
        self.queue[0], self.queue[1] = second, first
        return self.queue[0], self.queue[1]

    def rotate(self):
        """Rotate the front three items so the third becomes the new front."""
        if len(self.queue) < 3:
            raise IndexError("Rotate requires at least three items")
        first = self.queue.popleft()
        second = self.queue.popleft()
        third = self.queue.popleft()
        self.queue.appendleft(second)
        self.queue.appendleft(first)
        self.queue.appendleft(third)
        return [self.queue[0], self.queue[1], self.queue[2]]

    def at(self, index):
        """Return the value at zero-based offset from the front."""
        if index < 0 or index >= len(self.queue):
            raise IndexError("Index out of range")
        return self.queue[index]

    def find(self, item):
        """Return the index (from front) of the first matching item, or None if not found."""
        for index, value in enumerate(self.queue):
            if value == item:
                return index
        return None

    def to_list(self):
        """Return the queue contents from front to back."""
        return list(self.queue)
    
