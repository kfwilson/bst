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

    def __init__(self, val, color=RED, parent=None):
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
        return ((self.left != NIL) & (self.right != NIL))

    def __repr__(self):
        """ Official string rep of this node"""
        node_rep = "{} RBTreeNode(value = {}".format(self.color, self.value)
        node_rep += ", left=RBTreeNode({})".format(self.left.value) if self.left != NIL else ", left=NIL"
        node_rep += ", right=RBTreeNode({})".format(self.right.value) if self.right != NIL else ", right=NIL"
        node_rep += ", parent=RBTreeNode({}))".format(self.parent.value) if self.parent else "parent=None)"
        return node_rep

    def _str_node(self, node):
        if node:
            return str(node.value)
        else:
            return "None"

    def get_sibling(self):
        """ Returns the sibling node (left child of parent if self is right child,
        right child of parent if self is left). Returns None only if self is root of tree"""
        if self.parent is None:
            return None
        else:
            if self is self.parent.left:
                return self.parent.right
            else:
                return self.parent.left


class RBTree(Tree):
    """ A binary search tree """
    def __init__(self, values=()):
        """ Constructor for this bst
            Can take optional values (list, tuple, or set (all items must be same type)) to build initial tree
            ALLOWS DUPLICATES (simple implementation that always stores duplicates to the right)
        """
        super().__init__(values)
        if self.root is None:
            self.root = NIL

    def insert(self, new_val):
        """ Wrapper for _insert that initiates the insertion by calling _insert on root"""
        if self.root == NIL:
            self.root = RBTreeNode(new_val, color=BLACK)  # root has to be black
        else:
            self._insert(self.root, new_val)

    def _insert(self, current, new_val):
        """ Inserts a red node storing the new_value into the BST"""
        if new_val <= current.value:
            if current.left != NIL:
                self._insert(current.left, new_val)
            else:
                current.left = RBTreeNode(new_val, parent=current)  # new nodes are red by default
                self._fix_rb_prop(current.left)
        else:
            if current.right != NIL:
                self._insert(current.right, new_val)
            else:
                current.right = RBTreeNode(new_val, parent=current)  # new nodes are red by default
                self._fix_rb_prop(current.right)

    def _fix_rb_prop(self, current):
        """Fixes the rb properties of the tree after an insert of current node"""
        p_node = current.parent
        if p_node.color == BLACK:
            return  # if the parent of the current node (newly inserted) is black, no properties are violated
        gp_node = p_node.parent # grandparent of the newly inserted node (p_node will always have a parent because it's red so not root)
        # otherwise, we're in a double red situation
        sib_node = p_node.get_sibling()
        if sib_node.color == BLACK:  # sibling is black or NIL (have to have a sibling because current can't be root)
            if p_node is gp_node.left:
                if current is p_node.left:  # rotate p node right and recolor it black, color gp node red
                    self._rotate_right(gp_node)
                else:
                    self._rotate_left(p_node)
                    self._rotate_right(gp_node)
                max(current, p_node).color = BLACK
            else:
                if current is p_node.right:
                    self._rotate_left(gp_node)
                else:
                    self._rotate_right(p_node)
                    self._rotate_left(gp_node)
                min(current, p_node).color = BLACK
            gp_node.color = RED
        else: # sibling is red
            p_node.color = BLACK
            sib_node.color = BLACK
            if (gp_node.parent != None):  # as long as gp isn't the root, change color to red
                gp_node.color = RED
        self._fix_rb_prop(gp_node) # recolor might have created double-red between gp & gp's parent so recursively fix

    def _rotate_left(self, og_root):
        """ Rotate the subtree with root og_root to the left so that right subtree of og_root replaces og_root"""
        new_root = og_root.right
        og_root.right = new_root.left
        if new_root.left:
            new_root.left.parent = og_root
        new_root.parent = og_root.parent
        if og_root is self.root:  # if our original root of the rotation is the tree root, replace tree root with new root
            self.root = new_root
        else:
            if og_root is og_root.parent.left:
                og_root.parent.left = new_root
            else:
                og_root.parent.right = new_root
        new_root.left = og_root
        og_root.parent = new_root

    def _rotate_right(self, og_root):
        """Rotate the subtree with root og_root to the right so that left subtree of og_root replaces og_root"""
        new_root = og_root.left
        og_root.left = new_root.right
        if new_root.right:
            new_root.right.parent = og_root
        new_root.parent = og_root.parent
        if og_root.value == self.root.value:  # og_root is tree root
            self.root = new_root
        else:
            if og_root is og_root.parent.right:
                og_root.parent.right = new_root
            else:
                og_root.parent.left = new_root
        new_root.right = og_root
        og_root.parent = new_root

    def _print_level(self, node, level, height):
        if level < height:
            if node==NIL:
                print('\t' * level + "NIL")
            else:
                level_str = "{}({})".format(node.value, node.color)
                print('\t' * level + level_str)
                self._print_level(node._left, level + 1, height)
                self._print_level(node._right, level + 1, height)

def main():
    # s = input("Enter a list of numbers to build your own tree (Enter to use default list): ")
    # if not s:
    #     lst = [10, 4, 15, 7, 12, 20, 6, 8, 18, 30]
    #     print("Using default list: " + str(lst))
    # else:
    #     lst = [int(x) for x in s.split()]
    # tree = BSTree(lst)
    # #tree.insert("test string")
    # tree.print_tree()
    # print(tree)
    # print(tree.root)
    # print("12 is in tree? {}".format(tree.find(12)))
    # print("100 is in tree? {}".format(tree.find(100)))
    # print("Height: " + str(tree.height()))
    # print("In-order: " + str(tree.to_list('in_order')))
    # print("Pre-order: " + str(tree.to_list('pre_order')))
    # print("Post-order: " + str(tree.to_list('post_order')))
    # print("Breadth first (level-order): " + str(tree.to_list('level_order')))

    node_a = RBTreeNode(5)
    node_b = RBTreeNode(3)
    print("Minimum: {}".format(min(node_a, node_b)))

if __name__ == "__main__":
    main()