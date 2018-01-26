"""A python binary search tree implementation."""
from typing import Iterable

class TreeNode:
    """A node for use in binary search trees.

    Attributes
    ----------
    value : Any
        The data this node holds.
    """

    def __init__(self, val):
        self.value = val
        self._left = None
        self._right = None

    @property
    def left(self):
        """ A reference to the left child node, if one exists """
        return self._left

    @property
    def right(self):
        """ A reference to the right child node, if one exists """
        return self._right

    @left.setter
    def left(self, new_left):
        """ Sets the value of this node's left child pointer """
        self._left = new_left

    @right.setter
    def right(self, new_right):
        """ Sets the value of this node's right child pointer """
        self._right = new_right

    def __str__(self):
        """ Returns the value of this node as a string """
        node_str = str(self.value)
        if self._left:
            node_str += ", L: " + self._left.value
        if self._right:
            node_str += ", R: " + self._right.value
        return node_str

    def __repr__(self):
        """ Official string rep of this node"""
        node_str = "TreeNode(" + str(self.value) + ", L: "
        if self._left:
            node_str += self._left.value
        else:
            node_str += "None"
        node_str += ", R: "
        if self._right:
            node_str += self._right.value
        else:
            node_str += "None"
        return (node_str+")")

# move internal recursive functions that don't depend on external data outside as functions
class BSTree:
    """ A binary search tree """
    def __init__(self, values=()):
        """ Constructor for this bst
            Can take optional values (list, tuple, or set (all items must be same type)) to build initial tree
            ALLOWS DUPLICATES (simple implementation that always stores duplicates to the right)
        """
        self._root = None

        if isinstance(values, Iterable) and values:
            values = list(values)
            for v in values:
                self.insert(v)
        elif isinstance(values, Iterable):
            pass # didn't get passed any values - construct empty BST
        else:
            raise TypeError("{} object is not iterable".format(values))

    @property
    def root(self):
        """ A reference to the root of this BST, if one exists """
        return self._root

    @root.setter
    def root(self, new_node):
        if isinstance(new_node, TreeNode) or new_node is None:
            self._root = new_node
        else:
            raise TypeError("The head value of a BST may only be a TreeNode or None")

    def insert(self, new_val):
        """ Wrapper for insertNode that initiates the insertion by calling insertNode on root"""
        if self.root is None:
            self.root = TreeNode(new_val)
        else:
            if type(self.root.value) != type(new_val):
                raise TypeError("You can only insert objects of type " + str(type(self.root.value)) + " into this BST.")
            self._insert_node(self.root, new_val)

    def _insert_node(self, current, new_val):
        """ Inserts a node storing the new_value into the BST"""
        if new_val < current.value:
            if current.left:
                self._insert_node(current.left, new_val)
            else:
                current.left = TreeNode(new_val)
        else:
            if current.right:
                self._insert_node(current.right, new_val)
            else:
                current.right = TreeNode(new_val)

    def find(self, search_val):
        """ Wrapper for findNode that initiates the search by calling findNode starting at the root """
        return self._find_node(self.root, search_val)

    def _find_node(self, current, search_val):
        """ Searches the BST for the passed search_val returning true if value found, false otherwise"""
        if current is None:
            return False
        elif search_val == current.value:
            return True
        elif search_val <= current.value:
            return self._find_node(current.left, search_val)
        return self._find_node(current.right, search_val)

    def height(self):
        """ Wrapper for heightNode that initiates the height calculation by calling heightNode on the root """
        return self._height_node(self.root)

    def _height_node(self, node):
        """ Calculates the height of the tree from the passed current node """
        if node is None:
            return 0;
        return 1 + max(self._height_node(node.left), self._height_node(node.right))

    def to_list(self, order):
        """ Returns a list representation of the tree with the specified order.
            Order must be one of: {'in_order', 'pre_order', 'post_order', 'level_order'}
        """
        if order == 'in_order':
            return self._in_order(self.root)
        elif order == 'pre_order':
            return self._pre_order(self.root)
        elif order == 'post_order':
            return self._post_order(self.root)
        elif order == 'level_order':
            return self._level_order()
        else:
            raise NotImplementedError() # is this the right error? just copied from ll

    def _in_order(self, node):
        """Returns in order list representation of tree"""
        if node is None:
            return []
        return self._in_order(node.left) + [node.value] + self._in_order(node.right)

    def _pre_order(self, node):
        """Returns pre order list representation of tree"""
        if node is None:
            return []
        return [node.value] + self._pre_order(node.left) + self._pre_order(node.right)

    def _post_order(self, node):
        """Returns post order list representation of tree"""
        if node is None:
            return []
        return self._post_order(node.left) + self._post_order(node.right) + [node.value]

    def _level_order(self):
        """Returns level order list representation of tree"""
        if self.root is None:
            return []
        tree_ls = []
        st = [self.root] # using list as a stack
        while st:
            curr = st[0] # get the first element off
            st = st[1:] # pop the first element off the 'stack'
            tree_ls.append(curr.value) # store the node value in our list of nodes
            if curr.left:   # put the left child onto the stack if exists
                st.append(curr.left)
            if curr.right: # put the right child onto the stack if exists
                st.append(curr.right)
        return tree_ls

    def print_tree(self):
        self._print_level(self.root, 0, self.height())

    def _print_level(self, node, level, height):
        if level < height:
            if node is None:
                print('\t' * level + "None")
            else:
                print('\t' * level + str(node.value))
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
    print("12 is in tree? " + str(tree.find(12)))
    print("Height: " + str(tree.height()))
    print("In-order: " + str(tree.to_list('in_order')))
    print("Pre-order: " + str(tree.to_list('pre_order')))
    print("Post-order: " + str(tree.to_list('post_order')))
    print("Breadth first (level-order): " + str(tree.to_list('level_order')))

if __name__ == "__main__":
    main()