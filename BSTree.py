"""A python binary search tree implementation."""

from Tree import TreeNode
from Tree import Tree

"""Base binary tree class"""
from typing import Iterable
from node import Node

class BSTreeNode(TreeNode):
    """A node for use in binary search trees.

    Attributes
    ----------
    value : Any
        The data this node holds.
    """

    def __init__(self, val):
        super().__init__(val)
        self.height = 0

    def __repr__(self):
        """ Official string rep of this node"""
        node_rep = "BSTreeNode(value = {}".format(self.value)
        node_rep += ", left=BSTreeNode({})".format(self.left.value) if self.left else ", left=None"
        node_rep += ", right=BSTreeNode({})".format(self.right.value) if self.right else ", right=None"
        node_rep += ", parent=BSTreeNode({})".formate(self.parent.value) if self.parent else ", parent=None"
        node_rep += ", height={})".format(self.height)
        return node_rep

class BSTree(Tree):
    """ A binary search tree """
    def __init__(self, values=()):
        """ Constructor for this bst
            Can take optional values (list, tuple, or set (all items must be same type)) to build initial tree
            ALLOWS DUPLICATES (simple implementation that always stores duplicates to the left)
        """
        super().__init__(values)

    def insert(self, new_val):
        """ Wrapper for insertNode that initiates the insertion by calling insertNode on root"""
        if self.root is None:
            self.root = BSTreeNode(new_val)
        else:
            self._insert(self.root, new_val)

    def _insert(self, current, new_val):
        """ Inserts a node storing the new_value into the BST"""
        if new_val <= current.value:
            if current.left:
                self._insert(current.left, new_val)
            else:
                current.left = BSTreeNode(new_val)
        else:
            if current.right:
                self._insert(current.right, new_val)
            else:
                current.right = BSTreeNode(new_val)
        current.height = self._height(current)

    def delete(self, del_val):
        del_node = self._find(self.root, del_val)
        self._delete(self.root, del_node)

    def _delete(self, del_node):
        if del_node is None:
            return
        if del_node.left is None & del_node.right is None:
            if del_node is self.root:
                self.root = None
                return
            self._replace(del_node, None)
        elif del_node.left is not None & del_node.right is None:
            if del_node is self.root:
                self.root = del_node.left
                self.root.parent = None
            else:
                self._replace(del_node, del_node.left)

    def _replace(self, replacee_node, replacer_node):
        if replacee_node.parent:
            if replacee_node is replacee_node.parent.left:
                replacee_node.parent.left = replacer_node
            else:
                replacee_node.parent.right = replacer_node


    def _print_level(self, node, level, height):
        if level < height:
            if node is None:
                print('\t' * level + "None")
            else:
                level_str = "{}({})".format(node.value, node.height)
                print('\t' * level + level_str)
                self._print_level(node._left, level+1, height)
                self._print_level(node._right, level+1, height)

def main():
    s = input("Enter a list of numbers to build your own tree (Enter to use default list): ")
    if not s:
        lst = [10, 4, 15, 7, 12, 20, 6, 8, 18, 30]
        print("Using default list: " + str(lst))
    else:
        lst = [int(x) for x in s.split()]
    tree = BSTree(lst)
    #tree.insert("test string")
    tree.print_tree()
    print(tree)
    print(tree.root)
    print("12 is in tree? {}".format(tree.find(12)))
    print("100 is in tree? {}".format(tree.find(100)))
    print("Height: " + str(tree.height()))
    print("In-order: " + str(tree.to_list('in_order')))
    print("Pre-order: " + str(tree.to_list('pre_order')))
    print("Post-order: " + str(tree.to_list('post_order')))
    print("Breadth first (level-order): " + str(tree.to_list('level_order')))

if __name__ == "__main__":
    main()