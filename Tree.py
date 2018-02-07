"""Base binary tree class"""
from typing import Iterable
from node import Node

class TreeNode(Node):
    """A node for use in binary search trees.

    Attributes
    ----------
    value : Any
        The data this node holds.
    """

    def __init__(self, val, parent=None):
        if not hasattr(val, '__le__'):
            raise AttributeError('TreeNode values must be comparable.')
        super().__init__(val)
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

    @left.setter
    def left(self, new_left):
        """ Sets the value of this node's left child pointer """
        if isinstance(new_left, TreeNode) or new_left is None:
            self._left = new_left
        else:
            raise TypeError("The{0}.left must also be an instance of {0}".format(TreeNode))

    @right.setter
    def right(self, new_right):
        """ Sets the value of this node's right child pointer """
        if isinstance(new_right, TreeNode) or new_right is None:
            self._right = new_right
        else:
            raise TypeError("The{0}.right must also be an instance of {0}".format(TreeNode))

    @property
    def parent(self):
        """ A reference to the parent node, if one exists"""
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        """Sets the value of this node's parent pointer"""
        if isinstance(new_parent, TreeNode) or new_parent is None:
            self._parent = new_parent
        else:
            raise TypeError("The{0}.parent must also be an instance of {0}".format(TreeNode))


    def __repr__(self):
        """ Official string rep of this node"""
        node_rep = "TreeNode(value = {}".format(self.value)
        node_rep += ", left=TreeNode({})".format(self.left.value) if self.left else ", left=None"
        node_rep += ", right=TreeNode({})".format(self.right.value) if self.right else ", right=None"
        node_rep += ", parent=TreeNode({}))".formate(self.parent.value) if self.parent else ", parent=None)"
        return node_rep

class Tree:
    def __init__(self, values=()):
        self.root = None

        if isinstance(values, Iterable) and values:
            values = list(values)
            for v in values:
                self.insert(v)
        elif isinstance(values, Iterable):
            pass # didn't get passed any values - construct empty BST
        else:
            raise TypeError("{} object is not iterable".format(values))

    def find(self, search_val):
        """ Wrapper for findNode that initiates the search by calling findNode starting at the root """
        return self._find(self.root, search_val) is not None

    def _find(self, current, search_val):
        """ Searches the BST for the passed search_val returning true if value found, false otherwise"""
        if current is None:
            return None
        elif search_val == current.value:
            return current
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
                level_str = "{}".format(node.value)
                print('\t' * level + level_str)
                self._print_level(node._left, level+1, height)
                self._print_level(node._right, level+1, height)

    def __repr__(self):
        '''From James Collins'''
        em_dash = '\u2014'
        max_depth = min(5, self.height())
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

