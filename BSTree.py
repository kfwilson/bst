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

    def __init__(self, val, parent=None):
        super().__init__(val, parent)
        self.height = 1

    def __repr__(self):
        """ Official string rep of this node"""
        node_rep = "BSTreeNode(value = {}".format(self.value)
        node_rep += ", left=BSTreeNode({})".format(self.left.value) if self.left else ", left=None"
        node_rep += ", right=BSTreeNode({})".format(self.right.value) if self.right else ", right=None"
        node_rep += ", parent=BSTreeNode({})".format(self.parent.value) if self.parent else ", parent=None"
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
                current.left = BSTreeNode(new_val, parent=current)
        else:
            if current.right:
                self._insert(current.right, new_val)
            else:
                current.right = BSTreeNode(new_val, parent=current)
        current.height = self._height(current)

    def delete(self, del_val):
        """Calls find to access the node to be deleted, passing it to _delete to do the actual removal"""
        del_node = self._find(self.root, del_val)
        self._delete(del_node)

    def _delete(self, del_node):
        """ Removes the passed del_node from the tree, relinking around the removed node"""
        if not del_node:
            return
        if (not del_node.left) & (not del_node.right):
            self._replace(del_node, None)
        elif (del_node.left is not None) & (not del_node.right):
            self._replace(del_node, del_node.left)
        elif (not del_node.left) & (del_node.right is not None):
            self._replace(del_node, del_node.right)
        else: # we have 2 children so replace del_node with predecessor (since dupes stored to left)
            pre_node = self._find_max(del_node.left)
            del_node.value = pre_node.value
            self._delete(pre_node)

    def _find_max(self, current):
        """ Returns the node storing the greatest value in the subtree rooted at current """
        if current.right is None:
            return current
        return self._find_max(current.right)

    def _update_heights(self, current):
        """Travels up tree from current node to root, correcting the height at each node it stops at"""
        if current is None:
            return
        current.height = self._height(current)
        self._update_heights(current.parent)

    def _replace(self, replacee_node, replacer_node):
        if replacee_node is self.root:
            self.root = replacer_node
            if self.root:
                self.root.parent = None
        else: #any non-root node has a parent
            if replacee_node is replacee_node.parent.left:
                replacee_node.parent.left = replacer_node
            else:
                replacee_node.parent.right = replacer_node
            if replacer_node is not None:
                replacer_node.parent = replacee_node.parent
            self._update_heights(replacee_node.parent) # update the heights back up the path to the root

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
    tree.delete(10)
    print(tree)
    tree.print_tree()
    print(tree.root)
    print("Height: " + str(tree.height()))
    print("In-order: " + str(tree.to_list('in_order')))
    print("Pre-order: " + str(tree.to_list('pre_order')))
    print("Post-order: " + str(tree.to_list('post_order')))
    print("Breadth first (level-order): " + str(tree.to_list('level_order')))

if __name__ == "__main__":
    main()