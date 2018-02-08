"""A python AVL balanced binary search tree implementation."""
from typing import Iterable

from Tree import TreeNode
from Tree import Tree

class AVLTreeNode(TreeNode):
    """A node for use in binary search trees.

    Attributes
    ----------
    val : Any
        The data this node holds.
    """

    def __init__(self, val, parent=None):
        super().__init__(val, parent)
        self.balance = 0 # difference between heights of left and right subtrees (h(left) - h(right))

    def __repr__(self):
        """ Official string rep of this node"""
        node_rep = "AVLTreeNode(value = {}".format(self.value)
        node_rep += ", left=AVLTreeNode({})".format(self.left.value) if self.left else ", left=None"
        node_rep += ", right=AVLTreeNode({})".format(self.right.value) if self.right else ", right=None"
        node_rep += ", parent=AVLTreeNode({})".format(self.parent.value) if self.parent else ", parent=None"
        node_rep += ", balance={})".format(self.balance)
        return node_rep

# move internal recursive functions that don't depend on external data outside as functions
class AVLTree(Tree):
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
            self.root = AVLTreeNode(new_val)
        else:
            self._insert(self.root, new_val)

    def _insert(self, current, new_val):
        """ Inserts a node storing the new_value into the BST"""
        if new_val < current.value:
            if current.left:
                self._insert(current.left, new_val)
            else:
                current.left = AVLTreeNode(new_val, parent=current)
                self._update_critical_balance(current.left)
        else:
            if current.right:
                self._insert(current.right, new_val)
            else:
                current.right = AVLTreeNode(new_val, parent=current)
                self._update_critical_balance(current.right)

    def _update_critical_balance(self, current):
        """ Travels up the tree recursively checking and updating the balance. when reaches critical unbalanced point, rebalances tree and stops"""
        if abs(current.balance) > 1: # reached unbalanced point
            self.rebalance(current)
            return
        if current.parent:
            if current is current.parent.left: # if current node is left child of parent
                current.parent.balance += 1
            elif current is current.parent.right: # if current is right child
                current.parent.balance -= 1
            if current.parent.balance != 0: # continue updating and rebalancing up tree
                self._update_critical_balance(current.parent)

    def delete(self, del_val):
        """Calls find to access the node to be deleted, passing it to _delete to do the actual removal"""
        del_node = self._find(self.root, del_val)
        print(del_node)
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

    def _replace(self, replacee_node, replacer_node):
        """ replaces recplacee_node with replacer_node, relinking around the now removed replacee_node. calls update path to trace back up teh tree, rebalancing"""
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
            self._update_path(replacee_node.parent) # update the balances back up the path to the root, rebalancing as you go

    def _update_path(self, current):
        if current is None:
            return
        current.balance = self._height(current.left) - self._height(current.right)
        if abs(current.balance) > 1:
            self.rebalance(current)
        self._update_path(current.parent)

    def rebalance(self, current):
        """ Rebalance a node that is unbalanced via a series of rotations"""
        if current.balance < -1: # current node right heavy
            if current.right.balance > 0: # right child left heavy
                self.rotate_right(current.right)
                self.rotate_left(current)
            else: # right child is left heavy or balanced
                self.rotate_left(current)
        elif current.balance > 1: # current node left heavy
            if current.left.balance < 0: # left child right heavy
                self.rotate_left(current.left)
                self.rotate_right(current)
            else:
                self.rotate_right(current)

    def rotate_left(self, og_root):
        """ Rotate the subtree with root og_root to the left so that right subtree of og_root replaces og_root"""
        new_root = og_root.right
        og_root.right = new_root.left
        if new_root.left:
            new_root.left.parent = og_root
        new_root.parent = og_root.parent
        if og_root is self.root:    # if our original root of the rotation is the tree root, replace tree root with new root
            self.root = new_root
        else:
            if og_root is og_root.parent.left:
                og_root.parent.left = new_root
            else:
                og_root.parent.right = new_root
        new_root.left = og_root
        og_root.parent = new_root
        og_root.balance = og_root.balance + 1 - min(new_root.balance, 0)
        new_root.balance = new_root.balance + 1 + max(og_root.balance, 0)

    def rotate_right(self, og_root):
        """Rotate the subtree with root og_root to the right so that left subtree of og_root replaces og_root"""
        new_root = og_root.left
        og_root.left = new_root.right
        if new_root.right:
            new_root.right.parent = og_root
        new_root.parent = og_root.parent
        if og_root.value == self.root.value: # og_root is tree root
            self.root = new_root
        else:
            if og_root is og_root.parent.right:
                og_root.parent.right = new_root
            else:
                og_root.parent.left = new_root
        new_root.right = og_root
        og_root.parent = new_root
        og_root.balance = og_root.balance - 1 - max(new_root.balance, 0)
        new_root.balance = new_root.balance - 1 + min(0, og_root.balance)

    def _balance(self, current):
        """Returns the balance factor of a node (the diff between heights of left and right subtrees"""
        if not current:
            return 0
        return (self._height(current.left)-self._height(current.right))

    def _print_level(self, node, level, height):
        if level < height:
            if node is None:
                print('\t' * level + "None")
            else:
                level_str = "{}({})".format(node.value, node.balance)
                print('\t' * level + level_str)
                self._print_level(node._left, level+1, height)
                self._print_level(node._right, level+1, height)

def sort(value_list):
    tree = AVLTree(value_list)
    return tree.to_list('in_order')

def main():
    s = input("Enter a list of numbers to build your own tree (Enter to use default list): ")
    if not s:
        lst = [10, 4, 15, 7, 12, 20, 6, 8, 18, 30]
        print("Using default list: " + str(lst))
    else:
        lst = [int(x) for x in s.split()]
    tree = AVLTree(lst)
    #tree.insert("test string")
    tree.print_tree()
    print(tree)
    print(tree.root)
    print("12 is in tree? " + str(tree.find(12)))
    print("Height: " + str(tree.height()))
    print("In-order: " + str(tree.to_list('in_order')))
    print("Pre-order: " + str(tree.to_list('pre_order')))
    print("Post-order: " + str(tree.to_list('post_order')))
    print("Breadth first (level-order): " + str(tree.to_list('level_order')))
    print()
    print()
    tree.delete(7)
    tree.delete(8)
    tree.delete(4)
    tree.print_tree()
    print(tree)
    print(sort(lst))

if __name__ == "__main__":
    main()