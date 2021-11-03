"""Implement a function that takes two parameters:
- A small dataset (e.g., an array of strings) and
- a hashing method.

It should build and return an object that represents a Merkle tree.
The output can be textual.

Use only the Python 3 standard library."""

import hashlib
import math


def merkle_tree_function(dataset, hashing_method='md5'):
    # 1) Set the hashing method based on function parameter
    Node.set_hashing_method(hashing_method)
    # 2) Build an object representing a Merkle tree
    my_tree = MerkleTree(dataset)
    # 3) Return a textual output
    return my_tree.root.display()


class Node:
    """The Node class sets and performs the hashing method based on the function parameter
    instances of the Node class represent individual nodes within the Merkle Tree."""

    HASHING_METHODS = {'sha1': hashlib.sha1, 'sha224': hashlib.sha224, 'sha256': hashlib.sha256,
                       'sha384': hashlib.sha384, 'sha512': hashlib.sha512, 'blake2b': hashlib.blake2b,
                       'blake2s': hashlib.blake2s, 'md5': hashlib.md5}

    def __init__(self, hashed_value, data, left=None, right=None):
        self.hashed_value = self.apply_hashing_method(hashed_value)
        self.data = data
        self.left = left
        self.right = right
        self.children = [self.left, self.right]

    def __repr__(self):
        return self.data

    def display(self, level=0):
        print('\t' * level + self.data + ' ' + self.hashed_value)
        for child in self.children:
            if child:
                child.display(level + 1)

    @classmethod
    def set_hashing_method(cls, hashing_type):
        cls.selected_method = cls.HASHING_METHODS[hashing_type]

    @classmethod
    def apply_hashing_method(cls, data):
        crypt = cls.selected_method(data.encode('UTF-8'))
        return crypt.hexdigest()


class MerkleTree:
    """Initialisation of an instance of the MerkleTree class finds the root node by recursively
      calling the private method '__fill_tree'."""

    def __init__(self, dataset):
        self.root = self.__build_tree(dataset)

    def __build_tree(self, dataset):
        # If necessary extend the dataset with default values.
        while math.log2(len(dataset)).is_integer() is False:
            dataset.append(None)
        leaves = [Node(str(leaf), str(leaf)) for leaf in dataset]
        return self.__fill_tree(leaves)

    def __fill_tree(self, nodes):
        # If length of nodes is 2 you have reached the base case.
        if len(nodes) == 2:
            current_node = Node(nodes[0].hashed_value + nodes[1].hashed_value,
                                nodes[0].data + nodes[1].data, nodes[0], nodes[1])
            return current_node

        middle = len(nodes) // 2
        # Splits the list of nodes in half and recursively fills in the left side and right side.
        left, right = self.__fill_tree(nodes[:middle]), self.__fill_tree(nodes[middle:])
        hashed_value = Node.apply_hashing_method(left.hashed_value + right.hashed_value)
        data = left.data + right.data
        current_node = Node(hashed_value, data, left, right)
        return current_node


if __name__ == "__main__":
    dataset = ['here', 'is', 'some', 'example', 'data']
    hashing_method = 'blake2b'
    merkle_tree_function(dataset, hashing_method)
