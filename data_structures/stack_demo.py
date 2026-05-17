class StackDemo:
    def __init__(self):
        """Initialize an empty stack using a list."""
        self.stack = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self.stack.append(item)

    def pop(self):
        """Remove and return the top item from the stack."""
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        return self.stack.pop()

    def peek(self):
        """Get the top item of the stack without removing it."""
        if self.is_empty():
            raise IndexError("Peek from an empty stack")
        return self.stack[-1]

    def is_empty(self):
        """Return True if the stack is empty, otherwise False."""
        return len(self.stack) == 0

    def size(self):
        """Return the size of the stack."""
        return len(self.stack)

    def clear(self):
        """Remove all items from the stack."""
        self.stack.clear()

    def swap(self):
        """Swap the top two items on the stack."""
        if self.size() < 2:
            raise IndexError("Swap requires at least two items")
        top = self.stack[-1]
        next_item = self.stack[-2]
        self.stack[-2], self.stack[-1] = top, next_item
        return self.stack[-2], self.stack[-1]

    def rotate(self):
        """Rotate the top three items so the third item becomes the new top."""
        if self.size() < 3:
            raise IndexError("Rotate requires at least three items")
        third, second, top = self.stack[-3:]
        self.stack[-3:] = [second, top, third]
        return self.stack[-3:]

    def dup(self):
        """Duplicate the top item on the stack."""
        if self.is_empty():
            raise IndexError("Dup requires at least one item")
        item = self.peek()
        self.push(item)
        return item
