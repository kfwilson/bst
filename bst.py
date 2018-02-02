"""A python binary search tree implementation."""
from typing import Iterable

class TreeNode:
    """A node for use in binary search trees.

    Attributes
    ----------
    value : Any
        The data this node holds.
    """

    def __init__(self, val, parent = None):
        self.value = val
        self.balance = 0 # difference between heights of left and right subtrees (h(left) - h(right))
        self._left = None
        self._right = None
        self._parent = parent

    @property
    def left(self):
        """ A reference to the left child node, if one exists """
        return self._left

    @property
    def right(self):
        """ A reference to the right child node, if one exists """
        return self._right

    @property
    def parent(self):
        """ A reference to the parent node, if one exists"""
        return self._parent

    @left.setter
    def left(self, new_left):
        """ Sets the value of this node's left child pointer """
        self._left = new_left

    @right.setter
    def right(self, new_right):
        """ Sets the value of this node's right child pointer """
        self._right = new_right

    @parent.setter
    def parent(self, new_parent):
        """Sets the value of this node's parent pointer"""
        self._parent = new_parent

    def is_left(self):
        """ Returns true if the node is the left child of its parent"""
        if self.parent:
            if self.parent.left:
                return (self.value == self.parent.left.value)
        return False

    def is_right(self):
        """ Returns true if the node is the right child of its parent"""
        if self.parent:
            if self.parent.right:
                return (self.value == self.parent.right.value)
        return False

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
        if self.left:
            node_str += self.left.value
        else:
            node_str += "None"
        node_str += ", R: "
        if self._right:
            node_str += self.right.value
        else:
            node_str += "None"
        return (node_str+", BF: " + str(self.balance)+")")

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
            self._insert(self.root, new_val)

    def _insert(self, current, new_val):
        """ Inserts a node storing the new_value into the BST"""
        if new_val < current.value:
            if current.left:
                self._insert(current.left, new_val)
            else:
                current.left = TreeNode(new_val, parent = current)
                self._update_balance(current.left)
        else:
            if current.right:
                self._insert(current.right, new_val)
            else:
                current.right = TreeNode(new_val, parent = current)
                self._update_balance(current.right)

    def _update_balance(self, current):
        """ Check the balance of the current node and rebalance if necessary. call update_balance on parent recursively"""
        if abs(current.balance) > 1: # if node is unbalanced
            self.rebalance(current)
            return
        if current.parent:
            if current is current.parent.left: # if current node is left child of parent
                current.parent.balance += 1
            elif current is current.parent.right: # if current is right child
                current.parent.balance -= 1
            if current.parent.balance != 0: # continue updating and rebalancing up tree
                self._update_balance(current.parent)

    def rebalance(self, current):
        """ Rebalance a node that is unbalanced by a series of rotations"""
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
            if og_root.is_left():
                og_root.parent.left = new_root
            else:
                og_root.parent.right = new_root
        new_root.left = og_root
        og_root.parent = new_root
        og_root.balance = new_root.balance + 1 - min(new_root.balance, 0)
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
            if og_root.is_right():
                og_root.parent.right = new_root
            else:
                og_root.parent.left = new_root
        new_root.right = og_root
        og_root.parent = new_root
        og_root.balance = og_root.balance + 1 + max(new_root.balance, 0)
        new_root.balance = new_root.balance - 1 + min(0, og_root.balance)

    def _balance(self, current):
        """Returns the balance factor of a node (the diff between heights of left and right subtrees"""
        if not current:
            return 0
        return (self._height(current.left)-self._height(current.right))

    def find(self, search_val):
        """ Wrapper for findNode that initiates the search by calling findNode starting at the root """
        return self._find(self.root, search_val)

    def _find(self, current, search_val):
        """ Searches the BST for the passed search_val returning true if value found, false otherwise"""
        if current is None:
            return False
        elif search_val == current.value:
            return True
        elif search_val <= current.value:
            return self._find(current.left, search_val)
        return self._find(current.right, search_val)

    def height(self):
        """ Wrapper for heightNode that initiates the height calculation by calling heightNode on the root """
        return self._height(self.root)

    def _height(self, node):
        """ Calculates the height of the tree from the passed current node """
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

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
                print('\t' * level + str(node.value) + "(" + str(node.balance)+")")
                self._print_level(node._left, level+1, height)
                self._print_level(node._right, level+1, height)

    def __repr__(self):
        '''From James Collins'''
        em_dash = '\u2014'
        max_depth = min(5, self.height() - 1)  # replaced height with balance in node so changing this to tree height
        value_width = 3  # Must be odd.
        node_width = value_width + 2  # Add space for parentheses
        print_width = (node_width + 1) * 2 ** (max_depth - 1) - 1
        center = print_width // 2 + 1
        level = [self.root]
        blank_char = ' '
        out = ""
        for i in range(max_depth):
            next_level = []
            for n in level:
                if n:
                    next_level.extend([n.left, n.right])
                else:
                    next_level.extend([None, None])
            end_width = center // 2 ** i - (node_width // 2 + 1)
            end_space = blank_char * end_width
            interstitial_width = (print_width - 2 * end_width - node_width * len(level)) // (len(level) - 1) if len(
                level) > 1 else 0
            interstitial_space = blank_char * interstitial_width
            out += end_space
            out += interstitial_space.join(
                [f'({node.value: ^3})' if node else blank_char * node_width for node in level])
            out += end_space + '\n'

            out += end_space
            for n in level:
                if n:
                    if n.left:
                        out += blank_char * (node_width // 2 - 1) + '/' + blank_char
                    else:
                        out += blank_char * (node_width // 2 + 1)
                    if n.right:
                        out += '\\' + blank_char * (node_width // 2 - 1)
                    else:
                        out += blank_char * (node_width // 2)
                else:
                    out += blank_char * node_width
                out += interstitial_space
            out = out[:-interstitial_width] if interstitial_width else out
            out += end_space + '\n'

            if i == max_depth - 1:
                break

            next_end_width = center // 2 ** (i + 1) - (node_width // 2 + 1)
            dash_end_width = next_end_width + node_width // 2 + 1
            next_interstitial_width = (print_width - 2 * next_end_width - node_width * len(next_level)) // (
                        len(next_level) - 1)
            dash_width = (next_interstitial_width + 2 * (node_width // 2) - 3) // 2
            dash_interstitial_width = interstitial_width - 2 * (dash_width - node_width // 2 + 1)
            out += blank_char * dash_end_width
            for n in level:
                if n:
                    if n.left:
                        out += em_dash * dash_width + blank_char * 3
                    else:
                        out += blank_char * (3 + dash_width)
                    if n.right:
                        out += em_dash * dash_width
                    else:
                        out += blank_char * dash_width
                    out += blank_char * dash_interstitial_width
                else:
                    out += blank_char * (2 * dash_width + 3 + dash_interstitial_width)
            out = out[:-dash_interstitial_width] if interstitial_width else out
            out += blank_char * dash_end_width + '\n'

            out += blank_char * (next_end_width + node_width // 2)
            for n in level:
                if n:
                    out += '/' if n.left else blank_char
                    out += blank_char * (next_interstitial_width + 2 * (node_width // 2))
                    out += '\\' if n.right else blank_char
                    out += blank_char * (next_interstitial_width + 2 * (node_width // 2))
                else:
                    out += blank_char * 2 * (next_interstitial_width + 2 * (node_width // 2) + 1)
            out = out[:-(next_interstitial_width + 2 * (node_width // 2))]
            out += blank_char * (next_end_width + node_width // 2) + '\n'

            level = next_level

        return out[:-1]

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
    print("12 is in tree? " + str(tree.find(12)))
    print("Height: " + str(tree.height()))
    print("In-order: " + str(tree.to_list('in_order')))
    print("Pre-order: " + str(tree.to_list('pre_order')))
    print("Post-order: " + str(tree.to_list('post_order')))
    print("Breadth first (level-order): " + str(tree.to_list('level_order')))

if __name__ == "__main__":
    main()