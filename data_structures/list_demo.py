class ListDemo:
    def __init__(self):
        """Initialize an empty list."""
        self.lst = []

    def add(self, item):
        """Add an item to the list."""
        self.lst.append(item)

    def insert(self, index, item):
        """Insert an item at the given index."""
        if 0 <= index <= len(self.lst):
            self.lst.insert(index, item)
        else:
            raise IndexError("Index out of range")

    def remove(self, item):
        """Remove an item from the list by value."""
        if item in self.lst:
            self.lst.remove(item)
        else:
            raise ValueError("Item not found in the list")

    def remove_at(self, index):
        """Remove an item by index."""
        if 0 <= index < len(self.lst):
            return self.lst.pop(index)
        else:
            raise IndexError("Index out of range")

    def get(self, index):
        """Get an item by index."""
        if 0 <= index < len(self.lst):
            return self.lst[index]
        else:
            raise IndexError("Index out of range")

    def update(self, index, new_value):
        """Update the item at the given index."""
        if 0 <= index < len(self.lst):
            self.lst[index] = new_value
        else:
            raise IndexError("Index out of range")

    def size(self):
        """Return the size of the list."""
        return len(self.lst)

    def clear(self):
        """Remove all items from the list."""
        self.lst.clear()

    def to_list(self):
        """Return a shallow copy of the list contents."""
        return list(self.lst)
    
