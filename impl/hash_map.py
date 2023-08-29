from typing import Any, NamedTuple, Union

from interface.hash_map import HashMapInterface


class Pair(NamedTuple):
    key: Any
    value: Any


class HashMap(HashMapInterface):
    def __init__(self, size=8):
        if size < 1:
            raise ValueError("Size must be a positive number")
        self._slots = size * [None]

    def set(self, key, value):
        for index, pair in self._probe(key):
            if pair is None or pair.key == key:
                self._slots[index] = Pair(key, value)
                break
        else:
            self._resize_and_rehash()
            self.set(key, value)

    def get(self, key):
        for _, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair.key == key:
                return pair.value
        raise KeyError(key)

    def _resize_and_rehash(self):
        copy = HashMap(size=self.size * 2)
        for key, value in self._slots:
            copy.set(key, value)
        self._slots = copy._slots

    def _index(self, key) -> int:
        return hash(key) % len(self._slots)

    def _probe(self, key) -> Union[int, Pair]:
        index = self._index(key)
        for _ in range(self.size):
            yield index, self._slots[index]
            index = (index + 1) % self.size

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._slots = self.size * [None]

    @property
    def size(self):
        return len(self._slots)


if __name__ == "__main__":

    with HashMap(size=3) as hash_map:
        hash_map.set("planet", "Earth")
        hash_map.set("country", "Ukraine")
        hash_map.set("region", "Lvivska")
        hash_map.set("city", "Lviv")

        print(hash_map.get("country"))
        print(hash_map.get("city"))
        print(hash_map.get("region"))
        print(hash_map.get("city"))
