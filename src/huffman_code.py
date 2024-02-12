# -*- utf-8 -*-
"""Implentation of the Huffman algorithm on *.txt files.

In this module a specified .txt file is compressed using the lossless 
crompression; Huffman Algorithm. The compressed file is stored as a .bin file
with its corresponting Huffman codes stored in a json file. To decode the 
compressed file both files will be needed.
"""

with open("The Great Gatsby by F. Scott Fitzgerald.txt", "r")as input_file:
    string = input_file.read().replace("\n", " ")

print(len(string.encode("utf-8")))
    
#string = "abcd"

# Creating tree nodes 
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


# Main function implementing huffman coding
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d


# Calculating frequency
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

#dicitonary of chars and corresponding binString
print(huffmanCode)
print(len(huffmanCode))


print(' Char | Huffman code ')
print('----------------------')
for (char, frequency) in freq:
    print(' %-4r |%12s' % (char, huffmanCode[char]))



#Compress string using huffman code
compressed_string = ""
for char in string:
    compressed_string += huffmanCode[char]

#print(compressed_string)
def to_Bytes(data):
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

def write_compressed_file(filename: str) -> None:
    file = open("compressed.bin", "wb")
    file.write(to_Bytes(compressed_string))
    file.close()


#Write compressed string to bin file
file = open("compressed.bin", "wb")
file.write(to_Bytes(compressed_string))
file.close()

#decompress binString
huffmanCode_binStrings = dict([(value, key) for key, value in \
    huffmanCode.items()])

#print(huffmanCode_binStrings.keys()))

decompressed_string = ""
values = ""
for val in compressed_string:
    values += val
    if values in huffmanCode_binStrings.keys():
        decompressed_string += huffmanCode_binStrings[values]
        values = ""

byte_list = []
with open("decompressed.txt", 'w') as decompressed:
    decompressed.write(decompressed_string)
#print(decompressed_string)

with open("compressed.bin", "rb")as file:
    binString = "".join(bin(b)[2:] for b in file.read())
    print(type(binString))
