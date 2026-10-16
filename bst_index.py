class Node:
    def __init__(self, line):
        self.line = line
        self.next = None


class LineQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, line):
        if self.tail is not None and self.tail.line == line:
            return
        node = Node(line)
        if self.head is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    def text(self):
        result = ""
        cur = self.head
        while cur is not None:
            if result != "":
                result = result + ", "
            result = result + str(cur.line)
            cur = cur.next
        return result


def get_words(line):
    for sep in ".,:;":
        line = line.replace(sep, " ")
    return line.split()


class BSTNode:
    def __init__(self, word):
        self.word = word
        self.lines = LineQueue()
        self.left = None
        self.right = None


def insert(root, word, num):
    if root is None:
        root = BSTNode(word)
    node = root
    while node.word != word:
        if word < node.word:
            if node.left is None:
                node.left = BSTNode(word)
            node = node.left
        else:
            if node.right is None:
                node.right = BSTNode(word)
            node = node.right
    node.lines.add(num)
    return root


def build(filename):
    root = None
    f = open(filename)
    num = 0
    for line in f:
        num = num + 1
        for word in get_words(line):
            root = insert(root, word, num)
    f.close()
    return root


def search(root, word):
    node = root
    while node is not None:
        if word == node.word:
            return node.lines
        if word < node.word:
            node = node.left
        else:
            node = node.right
    return None


def print_tree(node, out):
    if node is not None:
        print_tree(node.left, out)
        out.write(node.word + ": " + node.lines.text() + "\n")
        print_tree(node.right, out)


def write(root, outname):
    out = open(outname, "w")
    print_tree(root, out)
    out.close()


if __name__ == "__main__":
    inputfile = input("Input file name: ")
    outputfile = input("Output file name: ")
    write(build(inputfile), outputfile)
