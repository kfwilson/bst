""" Implementation of basic data structure 'node'"""

class Node:
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __bool__(self):
        """ node is true, regardless of whether it's empty"""
        return True

    def __repr__(self):
        return "Node(value={})".format(self.value)

