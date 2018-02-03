"""A python Red Black balanced binary search tree implementation."""
from typing import Iterable

from Tree import TreeNode
from Tree import Tree

RED = 'RED'
BLACK = 'BLACK'
NIL = 'NIL' # sentinel node color (black)

class RBTreeNode(TreeNode):
    """A node for use in binary search trees.

    Attributes
    ----------
    val : Any
        The data this node holds.
    red : True, False
        Whether this node is red or black
    """

    def __init__(self, val, color = RED, parent = None):
        if not hasattr(val, '__le__'):
            raise AttributeError('RBTreeNode values must be comparable.')
        super().__init__(val)
        self.color = color
        self._parent = parent

    @property
    def parent(self):
        """ A reference to the parent node, if one exists"""
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        """Sets the value of this node's parent pointer"""
        if isinstance(new_parent, AVLTreeNode) or new_parent is None:
            self._parent = new_parent
        else:
            raise TypeError("The{0}.parent must also be an instance of {0}".format(AVLTreeNode))

    def __str__(self):
        """ Returns the value of this node as a string """
        node_str = str(self.value)
        if self._left:
            node_str += ", L: " + str(self._left.value)
        if self._right:
            node_str += ", R: " + str(self._right.value)
        return node_str+", BF = "+str(self.balance)

    def __repr__(self):
        """ Official string rep of this node"""
        return ("AVLTreeNode(" + str(self.value) +
                ", P: " + self._str_node(self.parent) +
                ", (L: " + self._str_node(self.left) + ", R: " + self._str_node(self.right) +
                "), BF: " + str(self.balance)+")")

    def _str_node(self, node):
        if node:
            return str(node.value)
        else:
            return "None"

# move internal recursive functions that don't depend on external data outside as functions
class RBTree(Tree):
    """ A binary search tree """
    def __init__(self, values=()):
        """ Constructor for this bst
            Can take optional values (list, tuple, or set (all items must be same type)) to build initial tree
            ALLOWS DUPLICATES (simple implementation that always stores duplicates to the right)
        """
        super().__init__(values)

    def insert(self, new_val):
        """ Wrapper for insertNode that initiates the insertion by calling insertNode on root"""
        if self.root is None:
            self.root = RBTreeNode(new_val)
        else:
            self._insert(self.root, new_val)