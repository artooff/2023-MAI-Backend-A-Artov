import unittest

from lab1.cache.cache import LRUCache


class LRUCacheTest(unittest.TestCase):

    def setUp(self):
        self.cache = LRUCache(3)

    def test_set_element(self):
        self.cache.set("3", "three")
        self.assertEqual("three", self.cache.get("3"))

    def test_set_new_value(self):
        self.cache.set("5", "value")
        self.cache.set("5", "new value")
        self.assertEqual("new value", self.cache.get("5"))

    def test_get_not_existing(self):
        self.assertEqual("", self.cache.get("kkk"))

    def test_remove_element(self):
        self.cache.set("some key", "some value")
        self.cache.remove("some key")
        self.assertEqual("", self.cache.get("some key"))

    def test_remove_all(self):
        self.cache.set("1", "one")
        self.cache.set("2", "two")
        self.cache.set("3", "three")

        self.cache.remove("1")
        self.cache.remove("2")
        self.cache.remove("3")

        self.assertEqual("", self.cache.get("1"))
        self.assertEqual("", self.cache.get("2"))
        self.assertEqual("", self.cache.get("3"))

    def test_overflow(self):
        self.cache.set("1", "one")
        self.cache.set("2", "two")
        self.cache.set("3", "three")
        self.cache.set("4", "four")
        self.cache.set("5", "five")
        self.cache.set("6", "six")

        self.assertEqual("", self.cache.get("1"))
        self.assertEqual("", self.cache.get("2"))
        self.assertEqual("", self.cache.get("3"))
        self.assertEqual("four", self.cache.get("4"))
        self.assertEqual("five", self.cache.get("5"))
        self.assertEqual("six", self.cache.get("6"))




if __name__ == '__main__':
    unittest.main()