from lab1.cache.node import Node
import string

class LRUCache:
    def __init__(self, capacity: int = 10) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be greater then zero")
        self.capacity = capacity
        self.cache = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: str) -> str:
        res: string

        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            res = node.value
        else:
            res = ""

        return res

    def set(self, key: str, value: str) -> None:
        if key in self.cache:
            self._remove(self.cache[key])

        node = Node(key, value)
        self.cache[key] = node
        self._add(node)

        if len(self.cache) > self.capacity:
            self.remove(self.head.next.key)

    def remove(self, key: str) -> None:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            del self.cache[key]


    def _add(self, node):
        prev = self.tail.prev
        prev.next = node
        node.prev = prev
        node.next = self.tail
        self.tail.prev = node

    def _remove(self, node):
        prev = node.prev
        next = node.next
        prev.next = next
        next.prev = prev