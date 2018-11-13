import unittest
import random


class CapacityHeap:
    def __init__(self, capacity, comparator=lambda x, y: x > y):
        self.values = []
        self.capacity = capacity
        self.comparator = comparator
        self.min_value = None
        self.min_index = -1

    @staticmethod
    def parent(index):
        return int((index - 1) / 2)

    @staticmethod
    def left_child(index):
        return 2 * index + 1

    @staticmethod
    def right_child(index):
        return 2 * index + 2

    def update_min(self):
        start_value = int(len(self.values) / 2)
        min_value = self.values[start_value]
        min_index = start_value
        for i in range(start_value + 1, len(self.values)):
            if self.comparator(min_value, self.values[i]):
                min_value = self.values[i]
                min_index = i

        self.min_value = min_value
        self.min_index = min_index

    def sift_up(self, start_index):
        index = start_index
        while index != 0 and self.comparator(self.values[index], self.values[self.parent(index)]):
            self.values[index], self.values[self.parent(index)] = self.values[self.parent(index)], self.values[index]
            index = self.parent(index)

    def push(self, new_value):
        if len(self.values) < self.capacity:
            self.values.append(new_value)
            self.sift_up(len(self.values) - 1)
            if len(self.values) == self.capacity - 1:
                self.update_min()

        elif self.comparator(new_value, self.min_value):
            self.values[self.min_index] = new_value
            self.sift_up(self.min_index)
            self.update_min()

    def pop(self):
        if len(self.values) == 0:
            return None

        return_value = self.values[0]
        self.values[0] = self.values[-1]
        del self.values[-1]

        index = 0
        leaf_start_index = int(len(self.values) / 2)
        while index < leaf_start_index:
            left_child_index = self.left_child(index)
            right_child_index = self.right_child(index)
            selected_index = left_child_index
            if right_child_index < len(self.values) \
                    and self.comparator(self.values[right_child_index], self.values[left_child_index]):
                    selected_index = right_child_index
            if self.comparator(self.values[selected_index], self.values[index]):
                self.values[index], self.values[selected_index] = self.values[selected_index], self.values[index]
                index = selected_index
            else:
                break

        return return_value


class CapacityHeapTest(unittest.TestCase):
    def test_heap(self):
        heap = CapacityHeap(5)
        a = [i for i in range(1, 101)]
        random.shuffle(a)

        for data in a:
            heap.push(data)

        for i in range(10):
            print(heap.pop())
