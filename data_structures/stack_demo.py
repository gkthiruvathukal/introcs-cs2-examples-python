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
    