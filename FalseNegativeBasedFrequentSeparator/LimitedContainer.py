import unittest
import random


class LimitedContainer:
    def __init__(self, size_limit, comparator: lambda x, y: x > y):
        self.values = []
        self.size_limit = size_limit
        self.comparator = comparator
        self.min_value = -1
        self.min_index = -1

    def values_min(self):
        idx = 0
        min_value = self.values[0]
        for i in range(1, len(self.values)):
            if self.comparator(min_value, self.values[i]):
                idx = i
                min_value = self.values[i]
        return idx, min_value

    def push(self, new_value):
        length = len(self.values)
        if length == 0:
            self.values.append(new_value)
            self.min_value = new_value
            self.min_index = 0
        elif length < self.size_limit:
            self.values.append(new_value)
            if self.comparator(self.min_value, new_value):
                self.min_value = new_value
                self.min_index = length
        else:
            if self.comparator(new_value, self.min_value):
                self.values[self.min_index] = new_value
                self.min_index, self.min_value = self.values_min()

    def pop(self):
        return_value = self.values[-1]
        del self.values[-1]
        return return_value


class LimitedContainerTest(unittest.TestCase):
    def test_push(self):
        lc = LimitedContainer(5, lambda x, y: x > y)

        ar = [i for i in range(100)]
        random.shuffle(ar)
        for i in ar:
            lc.push(i)

        for i in range(5):
            print(lc.pop())

        print(lc.values)
