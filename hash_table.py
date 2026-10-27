class Contact:
    """Stores a single contact's name and phone number."""

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self) -> str:
        return f"{self.name}: {self.number}"


class Node:
    """A node in a linked list, used for separate chaining in the hash table."""

    def __init__(self, key, value):
        self.key = key        # the contact's name
        self.value = value    # the Contact object
        self.next = None      # next Node in the chain


class HashTable:
    """A fixed-size hash table that uses separate chaining (linked lists) for collisions."""

    def __init__(self, size):
        self.size = size
        self.data = [None] * size

    def hash_function(self, key):
        """Convert a string key into an array index by summing character codes."""
        total = 0
        for char in key:
            total += ord(char)
        return total % self.size

    def insert(self, key, value):
        """Add a contact, or update the number if the name already exists."""
        index = self.hash_function(key)
        new_contact = Contact(key, value)

        # Empty bucket: the new node becomes the head of the list
        if self.data[index] is None:
            self.data[index] = Node(key, new_contact)
            return

        # Walk the chain, updating the number if the name already exists
        current = self.data[index]
        while True:
            if current.key == key:
                current.value.number = value
                return
            if current.next is None:
                break
            current = current.next

        # Name not found: append a new node to the end of the chain
        current.next = Node(key, new_contact)

    def search(self, key):
        """Return the Contact with a matching name, or None if not found."""
        index = self.hash_function(key)
        current = self.data[index]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def print_table(self):
        """Display each index and the contact(s) stored there."""
        for index in range(self.size):
            current = self.data[index]
            if current is None:
                print(f"Index {index}: Empty")
            else:
                line = f"Index {index}:"
                while current is not None:
                    line += f" - {current.value}"
                    current = current.next
                print(line)


# ---------------------------------------------------------------
# Tests
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Contact class
    contact_1 = Contact("Riley", "123-456-7890")
    print(contact_1)  # Riley: 123-456-7890

    # Node class
    node_1 = Node(contact_1.name, contact_1)
    print(node_1.key)    # Riley
    print(node_1.value)  # Riley: 123-456-7890
    print(node_1.next)   # None

    # Empty table
    print()
    table = HashTable(10)
    table.print_table()

    # Add some values
    print()
    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")
    table.print_table()

    # Search for a value
    contact = table.search("John")
    print("\nSearch result:", contact)  # Search result: John: 909-876-1234

    # Edge Case #1 - Hash collisions ("Amy" and "May" have the same letters,
    # so their ord() sums are equal and they land in the same index)
    print()
    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")
    table.print_table()

    # Edge Case #2 - Duplicate keys (should update Rebecca's number)
    print()
    table.insert("Rebecca", "999-444-9999")
    table.print_table()

    # Edge Case #3 - Searching for a value not in the table
    print()
    print(table.search("Chris"))  # None


# ---------------------------------------------------------------
# Design Memo
# ---------------------------------------------------------------
"""
A hash table is the right structure for fast lookups because it turns a key
directly into an array index. Instead of scanning every contact one by one,
the hash function computes where a name should live, so the table can jump
straight to that spot. As long as the contacts are spread out reasonably well,
inserting, searching, and updating all take about constant time, O(1), no
matter how many contacts are stored.

I handled collisions with separate chaining. Each slot in the underlying array
holds either None or the head of a linked list made of Node objects. When two
names hash to the same index, like "Amy" and "May" (which have the same
letters and therefore the same sum of ord() values), the second contact is
added to the end of that slot's linked list instead of overwriting the first.
While walking the chain during an insert, I also check whether the name is
already there; if it is, I update the existing contact's number rather than
adding a duplicate. Searching follows the same chain and returns None if no
matching name is found.

An engineer might choose a hash table over a list when they need quick access
by a key, since finding an item in an unsorted list means checking each
element, which is O(n). A hash table is also a good choice over a tree when
the data does not need to be kept in sorted order. Trees, such as binary
search trees, are better when you need ordered traversal, range queries
(for example, all names from A to F), or guaranteed worst-case performance.
For fast inserts and exact-match lookups, a hash table is usually best.
"""