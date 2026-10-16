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


class TrieNode:
    def __init__(self):
        self.children = {}
        self.lines = None


def build(filename):
    root = TrieNode()
    f = open(filename)
    num = 0
    for line in f:
        num = num + 1
        for word in get_words(line):
            node = root
            for ch in word:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            if node.lines is None:
                node.lines = LineQueue()
            node.lines.add(num)
    f.close()
    return root


def search(root, word):
    node = root
    for ch in word:
        if ch not in node.children:
            return None
        node = node.children[ch]
    return node.lines


def print_node(node, prefix, out):
    if node.lines is not None:
        out.write(prefix + ": " + node.lines.text() + "\n")
    for ch in sorted(node.children):
        print_node(node.children[ch], prefix + ch, out)


def write(root, outname):
    out = open(outname, "w")
    print_node(root, "", out)
    out.close()


if __name__ == "__main__":
    infile = input("Input file name: ")
    outfile = input("Output file name: ")
    write(build(infile), outfile)
