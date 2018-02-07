"""A python Red Black balanced binary search tree implementation."""
from typing import Iterable

from Tree import TreeNode
from Tree import Tree

RED = 'RED'
BLACK = 'BLACK'

class SentinelNode():
    def __init__(self):
        self.color = BLACK

    def __eq__(self, other):
        """All sentinel nodes are equal to each other"""
        return isinstance(other, SentinelNode)

    def __ne__(self, other):
        """Sentinel nodes are ONLY equal to other SentinelNodes"""
        return not isinstance(other, SentinelNode)

"""NIL is the sentinel leaf of tree"""
NIL = SentinelNode()

class RBTreeNode(TreeNode):
    """A node for use in binary search trees.

    Attributes
    ----------
    val : Any
        The data this node holds.
    color: {RED, BLACK}
        The color of this node: red or black
    """

    def __init__(self, val, color = RED, parent = None):
        if color not in (RED, BLACK):
            raise AttributeError("RBTreeNodes must be colored RED or BLACK")
        super().__init__(val)
        self._left = NIL
        self._right = NIL
        self.color = color
        self._parent = parent

    @property
    def parent(self):
        """ A reference to the parent node, if one exists"""
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        """Sets the value of this node's parent pointer"""
        if isinstance(new_parent, RBTreeNode) or new_parent is None:
            self._parent = new_parent
        else:
            raise TypeError("The{0}.parent must also be an instance of {0}".format(RBTreeNode))

    def has_children(self):
        """ Returns true if node has at least one non NIL child, False otherwise"""
        return ((self.left != NIL) & int(self.right != NIL))

    def __repr__(self):
        """ Official string rep of this node"""
        node_rep = "{} RBTreeNode(value = {}".format(self.color, self.value)
        node_rep += ", left=RBTreeNode({})".format(self.left.value) if self.left != NIL else "left=NIL"
        node_rep += ", right=RBTreeNode({})".format(self.right.value) if self.right != NIL else "right=NIL"
        node_rep += ", parent=RBTreeNode({}))".format(self.parent.value) if self.parent else "parent=None)"
        return node_rep

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
        """ Wrapper for _insert that initiates the insertion by calling _insert on root"""
        if self.root is None:
            self.root = RBTreeNode(new_val)
        else:
            self._insert(self.root, new_val)

    def _insert(self, current, new_val):
