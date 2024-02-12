# -*- utf-8 -*-
"""Implentation of the Huffman algorithm on *.txt files.

In this module a specified .txt file is compressed using the lossless 
crompression; Huffman Algorithm. The compressed file is stored as a .bin file
with its corresponting Huffman codes stored in a json file. To decode the 
compressed file both files will be needed.
"""

import json


class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)


def huffman_code_tree(node, left=True, binString='') -> dict:
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d


def to_Bytes(data: str) -> bytes:
    """
    Converts the string of binary values into bytes

        Args:
            data (str): string of binary characters(0,1)
        
        Returns:
            bytes(b) (bytes): the binary string converted to 8 bytes
    """

    b = bytearray()
    for i in range(0, len(data), 8):
        b.append(int(data[i: i + 8], 2))
    return bytes(b)


def compress_file(filename: str):
    """
    <text>

        Args:

        Returns
    """
    with open(filename, "r")as input_file:
        string = input_file.read().replace("\n", " ")
    
    freq = {}
    for c in string:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    nodes = freq

    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))

        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    huffmanCode = huffman_code_tree(nodes[0][0])

    print(huffmanCode)

    huffmanCode_binStrings = dict([(value, key) for key, value in \
    huffmanCode.items()])

    with open("huffmancodes.json", "w")as jsonf:
        json.dump(huffmanCode_binStrings, jsonf)
    
    compressed_string = ""
    for char in string:
        compressed_string += huffmanCode[char]
    
    filename = filename.replace(".txt", "_compressed.bin")
    with open(filename, "wb")as compressedf:
        compressedf.write(to_Bytes(compressed_string))


    return 'Compression has been completed'


def decompress_file(json_file: str, compressed_file: str):
    """
    <text>

        Args:

        Returns
    """
    with open(json_file, "r")as binS:
        huffmanCode_binStrings = dict(json.load(binS))
    
    # Open and read binary file into is binstring value
    with open(compressed_file, "rb") as f:
        compressed_string = "".join(bin(b)[2:] for b in f.read())

    print(compressed_string)

    decompressed_string = ""
    values = ""
    for val in compressed_string:
        values += val
        if values in huffmanCode_binStrings.keys():
            decompressed_string += huffmanCode_binStrings[values]
            values = ""
    
    filename = compressed_file.replace(".bin", "_uncompressed.txt")
    with open(filename, "w") as uncompf:
        uncompf.write(decompressed_string)

    return 'file has been decompressed and stored in x directory'

if __name__ == "__main__":
    while True:
        usage = input("Are you compressing or decompressing a file:" \
            " enter c/d >")
            
        if usage == 'c':
            compf = input("Enter path of the file you wish to compress: ")
            compressed = compress_file(compf)

        elif usage == 'd':
            jsonf = input("Enter path of huffman code json file: ")
            decompf = input("Enter the path of the compressed .bin file: ")
            decompressed = decompress_file(jsonf, decompf)

