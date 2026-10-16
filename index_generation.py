"""
Index Generation Project
Usage: python index_generation.py INPUT_FILE OUTPUT_FILE

Builds an alphabetical word index with the line numbers on which each word
occurs. Input is streamed line by line, and each line is listed once per word.
"""

import sys
import re
from dataclasses import dataclass, field
from typing import Optional

# The assignment defines these as separators. Whitespace includes line breaks.
SEPARATOR_PATTERN = re.compile(r"[\s.,:;]+")


def read_words_by_line(filename):
    """Yield (word, line_number) pairs without changing character case."""
    with open(filename, "r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            for word in SEPARATOR_PATTERN.split(line):
                if word:
                    yield word, line_number


@dataclass
class TrieNode:
    children: dict = field(default_factory=dict)
    line_numbers: list = field(default_factory=list)
    is_word: bool = False


class TrieIndex:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, line_number):
        node = self.root
        for character in word:
            if character not in node.children:
                node.children[character] = TrieNode()
            node = node.children[character]
        node.is_word = True
        if not node.line_numbers or node.line_numbers[-1] != line_number:
            node.line_numbers.append(line_number)

    def search(self, word):
        node = self.root
        for character in word:
            if character not in node.children:
                return None
            node = node.children[character]
        return node.line_numbers if node.is_word else None

    def items_sorted(self):
        """Pre-order character traversal gives ASCII-sorted words."""
        result = []
        stack = [(self.root, "")]
        while stack:
            node, prefix = stack.pop()
            # A complete prefix word comes before any longer word beginning
            # with that prefix (for example, "app" before "apple").
            if node.is_word:
                result.append((prefix, node.line_numbers))
            # Reverse push order because a stack pops the last item first.
            for character in sorted(node.children.keys(), reverse=True):
                stack.append((node.children[character], prefix + character))
        return result


@dataclass
class BSTNode:
    word: str
    line_numbers: list
    left: Optional["BSTNode"] = None
    right: Optional["BSTNode"] = None


class BSTIndex:
    def __init__(self):
        self.root = None

    def insert(self, word, line_number):
        if self.root is None:
            self.root = BSTNode(word, [line_number])
            return
        node = self.root
        while True:
            if word == node.word:
                if node.line_numbers[-1] != line_number:
                    node.line_numbers.append(line_number)
                return
            if word < node.word:
                if node.left is None:
                    node.left = BSTNode(word, [line_number])
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = BSTNode(word, [line_number])
                    return
                node = node.right

    def search(self, word):
        node = self.root
        while node is not None:
            if word == node.word:
                return node.line_numbers
            node = node.left if word < node.word else node.right
        return None

    def items_sorted(self):
        result = []
        stack = []
        node = self.root
        # Iterative in-order traversal produces ascending word order.
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            result.append((node.word, node.line_numbers))
            node = node.right
        return result


class DictionaryIndex:
    def __init__(self):
        self.data = {}

    def insert(self, word, line_number):
        line_numbers = self.data.get(word)
        if line_numbers is None:
            self.data[word] = [line_number]
        elif line_numbers[-1] != line_number:
            line_numbers.append(line_number)

    def search(self, word):
        return self.data.get(word)

    def items_sorted(self):
        return ((word, self.data[word]) for word in sorted(self.data))


def build_index(index_class, input_filename):
    """Read the file once and build one chosen index."""
    index = index_class()
    for word, line_number in read_words_by_line(input_filename):
        index.insert(word, line_number)
    return index


def write_index(output_file, title, items):
    """Write a named index section in a readable text format."""
    output_file.write(f"\n=== {title} ===\n")
    for word, line_numbers in items:
        numbers = ", ".join(map(str, line_numbers))
        output_file.write(f"{word} : {numbers}\n")


def main():
    if len(sys.argv) != 3:
        print("Usage: python index_generation.py INPUT_FILE OUTPUT_FILE")
        raise SystemExit(1)

    input_filename, output_filename = sys.argv[1], sys.argv[2]
    index = build_index(DictionaryIndex, input_filename)
    with open(output_filename, "w", encoding="utf-8", newline="\n") as output:
        write_index(output, "ALPHABETICAL WORD INDEX", index.items_sorted())
    print(f"Indexed {len(index.data)} distinct words")
    print(f"Index written to: {output_filename}")


if __name__ == "__main__":
    main()
