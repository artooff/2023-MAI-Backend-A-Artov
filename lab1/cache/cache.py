from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int = 10) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be greater then zero")
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> str:
        if key not in self.cache:
            return ""
        else:
            self.cache.move_to_end(key)
            return self.cache[key]

    def set(self, key: str, value: str) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def remove(self, key: str) -> None:
        del self.cache[key]


